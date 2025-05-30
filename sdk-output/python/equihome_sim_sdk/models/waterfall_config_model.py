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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt
from typing import Any, ClassVar, Dict, List, Optional, Union
from equihome_sim_sdk.models.waterfall_structure_enum import WaterfallStructureEnum
from typing import Optional, Set
from typing_extensions import Self

class WaterfallConfigModel(BaseModel):
    """
    Model for waterfall configuration.
    """ # noqa: E501
    waterfall_structure: Optional[WaterfallStructureEnum] = Field(default=None, description="Waterfall structure type")
    hurdle_rate: Optional[Union[StrictFloat, StrictInt]] = Field(default=0.08, description="Hurdle rate (preferred return)")
    carried_interest_rate: Optional[Union[StrictFloat, StrictInt]] = Field(default=0.2, description="Carried interest rate")
    catch_up_rate: Optional[Union[StrictFloat, StrictInt]] = Field(default=0.0, description="GP catch-up rate")
    gp_commitment_percentage: Optional[Union[StrictFloat, StrictInt]] = Field(default=0.0, description="GP commitment percentage")
    multi_tier_enabled: Optional[StrictBool] = Field(default=False, description="Enable multi-tier waterfall")
    enable_clawback: Optional[StrictBool] = Field(default=True, description="Enable clawback")
    clawback_threshold: Optional[Union[StrictFloat, StrictInt]] = Field(default=0.0, description="Clawback threshold")
    __properties: ClassVar[List[str]] = ["waterfall_structure", "hurdle_rate", "carried_interest_rate", "catch_up_rate", "gp_commitment_percentage", "multi_tier_enabled", "enable_clawback", "clawback_threshold"]

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
        """Create an instance of WaterfallConfigModel from a JSON string"""
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
        """Create an instance of WaterfallConfigModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "waterfall_structure": obj.get("waterfall_structure"),
            "hurdle_rate": obj.get("hurdle_rate") if obj.get("hurdle_rate") is not None else 0.08,
            "carried_interest_rate": obj.get("carried_interest_rate") if obj.get("carried_interest_rate") is not None else 0.2,
            "catch_up_rate": obj.get("catch_up_rate") if obj.get("catch_up_rate") is not None else 0.0,
            "gp_commitment_percentage": obj.get("gp_commitment_percentage") if obj.get("gp_commitment_percentage") is not None else 0.0,
            "multi_tier_enabled": obj.get("multi_tier_enabled") if obj.get("multi_tier_enabled") is not None else False,
            "enable_clawback": obj.get("enable_clawback") if obj.get("enable_clawback") is not None else True,
            "clawback_threshold": obj.get("clawback_threshold") if obj.get("clawback_threshold") is not None else 0.0
        })
        return _obj


