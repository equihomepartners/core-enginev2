"""
Parameter registry module for the EQU IHOME SIM ENGINE v2.

This module provides a central registry for all simulation parameters with validation rules.
"""

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Callable, TypeVar, Generic, Set

import structlog

logger = structlog.get_logger(__name__)


class ParameterType(Enum):
    """Parameter types."""
    INTEGER = "integer"
    FLOAT = "float"
    STRING = "string"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"
    ENUM = "enum"


T = TypeVar("T")


@dataclass
class Parameter(Generic[T]):
    """
    Parameter definition.
    
    Attributes:
        name: Parameter name
        description: Parameter description
        type: Parameter type
        default: Default value
        required: Whether the parameter is required
        min_value: Minimum value (for numeric parameters)
        max_value: Maximum value (for numeric parameters)
        enum_values: Allowed values (for enum parameters)
        validation_func: Custom validation function
    """
    name: str
    description: str
    type: ParameterType
    default: Optional[T] = None
    required: bool = False
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    enum_values: Optional[List[str]] = None
    validation_func: Optional[Callable[[T], bool]] = None
    
    def validate(self, value: Any) -> bool:
        """
        Validate a parameter value.
        
        Args:
            value: Parameter value
            
        Returns:
            True if the value is valid, False otherwise
        """
        # Check type
        if self.type == ParameterType.INTEGER and not isinstance(value, int):
            logger.warning("Invalid parameter type", name=self.name, expected="integer", actual=type(value).__name__)
            return False
        
        if self.type == ParameterType.FLOAT and not isinstance(value, (int, float)):
            logger.warning("Invalid parameter type", name=self.name, expected="float", actual=type(value).__name__)
            return False
        
        if self.type == ParameterType.STRING and not isinstance(value, str):
            logger.warning("Invalid parameter type", name=self.name, expected="string", actual=type(value).__name__)
            return False
        
        if self.type == ParameterType.BOOLEAN and not isinstance(value, bool):
            logger.warning("Invalid parameter type", name=self.name, expected="boolean", actual=type(value).__name__)
            return False
        
        if self.type == ParameterType.OBJECT and not isinstance(value, dict):
            logger.warning("Invalid parameter type", name=self.name, expected="object", actual=type(value).__name__)
            return False
        
        if self.type == ParameterType.ARRAY and not isinstance(value, list):
            logger.warning("Invalid parameter type", name=self.name, expected="array", actual=type(value).__name__)
            return False
        
        # Check min/max values
        if self.min_value is not None and value < self.min_value:
            logger.warning("Parameter value below minimum", name=self.name, min=self.min_value, value=value)
            return False
        
        if self.max_value is not None and value > self.max_value:
            logger.warning("Parameter value above maximum", name=self.name, max=self.max_value, value=value)
            return False
        
        # Check enum values
        if self.type == ParameterType.ENUM and self.enum_values is not None and value not in self.enum_values:
            logger.warning("Invalid enum value", name=self.name, allowed=self.enum_values, value=value)
            return False
        
        # Run custom validation function
        if self.validation_func is not None and not self.validation_func(value):
            logger.warning("Custom validation failed", name=self.name, value=value)
            return False
        
        return True


class ParameterRegistry:
    """
    Registry for simulation parameters.
    
    This class provides a central registry for all simulation parameters with validation rules.
    """
    
    def __init__(self) -> None:
        """Initialize the parameter registry."""
        self._parameters: Dict[str, Parameter] = {}
        self._groups: Dict[str, Set[str]] = {}
    
    def register_parameter(self, parameter: Parameter) -> None:
        """
        Register a parameter.
        
        Args:
            parameter: Parameter definition
        """
        self._parameters[parameter.name] = parameter
        logger.debug("Parameter registered", name=parameter.name)
    
    def register_parameters(self, parameters: List[Parameter]) -> None:
        """
        Register multiple parameters.
        
        Args:
            parameters: List of parameter definitions
        """
        for parameter in parameters:
            self.register_parameter(parameter)
    
    def get_parameter(self, name: str) -> Optional[Parameter]:
        """
        Get a parameter by name.
        
        Args:
            name: Parameter name
            
        Returns:
            Parameter definition, or None if not found
        """
        return self._parameters.get(name)
    
    def get_parameters(self) -> Dict[str, Parameter]:
        """
        Get all parameters.
        
        Returns:
            Dictionary of parameter definitions
        """
        return self._parameters.copy()
    
    def validate_parameter(self, name: str, value: Any) -> bool:
        """
        Validate a parameter value.
        
        Args:
            name: Parameter name
            value: Parameter value
            
        Returns:
            True if the value is valid, False otherwise
        """
        parameter = self.get_parameter(name)
        
        if parameter is None:
            logger.warning("Unknown parameter", name=name)
            return False
        
        return parameter.validate(value)
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate multiple parameter values.
        
        Args:
            parameters: Dictionary of parameter values
            
        Returns:
            True if all values are valid, False otherwise
        """
        for name, value in parameters.items():
            if not self.validate_parameter(name, value):
                return False
        
        # Check required parameters
        for name, parameter in self._parameters.items():
            if parameter.required and name not in parameters:
                logger.warning("Required parameter missing", name=name)
                return False
        
        return True
    
    def add_to_group(self, group_name: str, parameter_name: str) -> None:
        """
        Add a parameter to a group.
        
        Args:
            group_name: Group name
            parameter_name: Parameter name
        """
        if group_name not in self._groups:
            self._groups[group_name] = set()
        
        self._groups[group_name].add(parameter_name)
        logger.debug("Parameter added to group", group=group_name, parameter=parameter_name)
    
    def get_group(self, group_name: str) -> Set[str]:
        """
        Get all parameters in a group.
        
        Args:
            group_name: Group name
            
        Returns:
            Set of parameter names
        """
        return self._groups.get(group_name, set()).copy()
    
    def get_groups(self) -> Dict[str, Set[str]]:
        """
        Get all groups.
        
        Returns:
            Dictionary of group names to sets of parameter names
        """
        return {group: params.copy() for group, params in self._groups.items()}
    
    def load_from_schema(self, schema_path: str) -> None:
        """
        Load parameters from a JSON schema file.
        
        Args:
            schema_path: Path to the JSON schema file
        """
        logger.info("Loading parameters from schema", path=schema_path)
        
        try:
            with open(schema_path, "r") as f:
                schema = json.load(f)
            
            if "properties" not in schema:
                logger.error("Invalid schema: missing 'properties'", path=schema_path)
                return
            
            for name, prop in schema["properties"].items():
                param_type = self._get_param_type(prop.get("type", "string"))
                
                parameter = Parameter(
                    name=name,
                    description=prop.get("description", ""),
                    type=param_type,
                    default=prop.get("default"),
                    required=name in schema.get("required", []),
                    min_value=prop.get("minimum"),
                    max_value=prop.get("maximum"),
                    enum_values=prop.get("enum"),
                )
                
                self.register_parameter(parameter)
                
                # Add to group based on property path
                if "." in name:
                    group, _ = name.split(".", 1)
                    self.add_to_group(group, name)
            
            logger.info("Parameters loaded from schema", count=len(self._parameters))
        
        except Exception as e:
            logger.error("Failed to load parameters from schema", path=schema_path, error=str(e))
    
    def _get_param_type(self, json_type: str) -> ParameterType:
        """
        Convert JSON schema type to parameter type.
        
        Args:
            json_type: JSON schema type
            
        Returns:
            Parameter type
        """
        if json_type == "integer":
            return ParameterType.INTEGER
        elif json_type == "number":
            return ParameterType.FLOAT
        elif json_type == "string":
            return ParameterType.STRING
        elif json_type == "boolean":
            return ParameterType.BOOLEAN
        elif json_type == "object":
            return ParameterType.OBJECT
        elif json_type == "array":
            return ParameterType.ARRAY
        else:
            return ParameterType.STRING


# Global parameter registry instance
_global_registry: Optional[ParameterRegistry] = None


def get_registry() -> ParameterRegistry:
    """
    Get the global parameter registry instance.
    
    Returns:
        The global parameter registry instance
    """
    global _global_registry
    
    if _global_registry is None:
        _global_registry = ParameterRegistry()
        
        # Load parameters from schema
        schema_path = Path(__file__).parent.parent.parent / "schemas" / "simulation_config_schema.json"
        if schema_path.exists():
            _global_registry.load_from_schema(str(schema_path))
    
    return _global_registry
