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

class SrcApiRoutersReinvestmentRiskMetricsResponse(BaseModel):
    """
    Risk metrics response model.
    """ # noqa: E501
    zone_distribution_change: Dict[str, Union[StrictFloat, StrictInt]] = Field(description="Change in zone distribution")
    avg_ltv_change: Union[StrictFloat, StrictInt] = Field(description="Change in average LTV")
    concentration_risk_change: Dict[str, Union[StrictFloat, StrictInt]] = Field(description="Change in concentration risk metrics")
    risk_score_before: Union[StrictFloat, StrictInt] = Field(description="Risk score before reinvestment")
    risk_score_after: Union[StrictFloat, StrictInt] = Field(description="Risk score after reinvestment")
    risk_score_change: Union[StrictFloat, StrictInt] = Field(description="Change in risk score")
    diversification_impact: Union[StrictFloat, StrictInt] = Field(description="Impact on portfolio diversification")
    risk_adjusted_return_impact: Union[StrictFloat, StrictInt] = Field(description="Impact on risk-adjusted return")
    __properties: ClassVar[List[str]] = ["zone_distribution_change", "avg_ltv_change", "concentration_risk_change", "risk_score_before", "risk_score_after", "risk_score_change", "diversification_impact", "risk_adjusted_return_impact"]

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
        """Create an instance of SrcApiRoutersReinvestmentRiskMetricsResponse from a JSON string"""
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
        """Create an instance of SrcApiRoutersReinvestmentRiskMetricsResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "zone_distribution_change": obj.get("zone_distribution_change"),
            "avg_ltv_change": obj.get("avg_ltv_change"),
            "concentration_risk_change": obj.get("concentration_risk_change"),
            "risk_score_before": obj.get("risk_score_before"),
            "risk_score_after": obj.get("risk_score_after"),
            "risk_score_change": obj.get("risk_score_change"),
            "diversification_impact": obj.get("diversification_impact"),
            "risk_adjusted_return_impact": obj.get("risk_adjusted_return_impact")
        })
        return _obj


