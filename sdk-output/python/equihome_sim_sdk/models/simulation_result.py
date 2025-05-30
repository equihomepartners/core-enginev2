# coding: utf-8

"""
    EQU IHOME SIM ENGINE API

    API for running home equity investment fund simulations

    The version of the OpenAPI document: 0.1.0
    Contact: info@equihome.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set
from typing_extensions import Self

class SimulationResult(BaseModel):
    """
    Simulation result model.
    """ # noqa: E501
    simulation_id: StrictStr = Field(description="Simulation ID")
    status: StrictStr = Field(description="Simulation status")
    created_at: StrictStr = Field(description="Creation timestamp")
    completed_at: Optional[StrictStr] = Field(default=None, description="Completion timestamp")
    config: Dict[str, Any] = Field(description="Simulation configuration")
    metrics: Optional[Dict[str, Any]] = Field(default=None, description="Simulation metrics")
    cashflows: Optional[List[Dict[str, Any]]] = Field(default=None, description="Simulation cashflows")
    capital_allocation: Optional[Dict[str, Any]] = Field(default=None, description="Capital allocation")
    loans: Optional[List[Dict[str, Any]]] = Field(default=None, description="Generated loans")
    loan_portfolio: Optional[Dict[str, Any]] = Field(default=None, description="Loan portfolio")
    execution_time: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Execution time in seconds")
    guardrail_violations: Optional[List[Dict[str, Any]]] = Field(default=None, description="Guardrail violations")
    __properties: ClassVar[List[str]] = ["simulation_id", "status", "created_at", "completed_at", "config", "metrics", "cashflows", "capital_allocation", "loans", "loan_portfolio", "execution_time", "guardrail_violations"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of SimulationResult from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SimulationResult from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "simulation_id": obj.get("simulation_id"),
            "status": obj.get("status"),
            "created_at": obj.get("created_at"),
            "completed_at": obj.get("completed_at"),
            "config": obj.get("config"),
            "metrics": obj.get("metrics"),
            "cashflows": obj.get("cashflows"),
            "capital_allocation": obj.get("capital_allocation"),
            "loans": obj.get("loans"),
            "loan_portfolio": obj.get("loan_portfolio"),
            "execution_time": obj.get("execution_time"),
            "guardrail_violations": obj.get("guardrail_violations")
        })
        return _obj


