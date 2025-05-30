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

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt
from typing import Any, ClassVar, Dict, List, Union
from typing import Optional, Set
from typing_extensions import Self

class TaxMetrics(BaseModel):
    """
    Tax metrics model.
    """ # noqa: E501
    pre_tax_irr: Union[StrictFloat, StrictInt] = Field(description="Pre-tax IRR")
    post_tax_irr: Union[StrictFloat, StrictInt] = Field(description="Post-tax IRR")
    pre_tax_npv: Union[StrictFloat, StrictInt] = Field(description="Pre-tax NPV")
    post_tax_npv: Union[StrictFloat, StrictInt] = Field(description="Post-tax NPV")
    total_tax_amount: Union[StrictFloat, StrictInt] = Field(description="Total tax amount")
    effective_tax_rate: Union[StrictFloat, StrictInt] = Field(description="Effective tax rate")
    __properties: ClassVar[List[str]] = ["pre_tax_irr", "post_tax_irr", "pre_tax_npv", "post_tax_npv", "total_tax_amount", "effective_tax_rate"]

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
        """Create an instance of TaxMetrics from a JSON string"""
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
        """Create an instance of TaxMetrics from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "pre_tax_irr": obj.get("pre_tax_irr"),
            "post_tax_irr": obj.get("post_tax_irr"),
            "pre_tax_npv": obj.get("pre_tax_npv"),
            "post_tax_npv": obj.get("post_tax_npv"),
            "total_tax_amount": obj.get("total_tax_amount"),
            "effective_tax_rate": obj.get("effective_tax_rate")
        })
        return _obj


