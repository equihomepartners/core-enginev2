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
from typing import Any, ClassVar, Dict, List, Union
from equihome_sim_sdk.models.metric_value import MetricValue
from typing import Optional, Set
from typing_extensions import Self

class SuburbDetail(BaseModel):
    """
    Suburb detail model.
    """ # noqa: E501
    suburb_id: StrictStr = Field(description="Suburb ID")
    name: StrictStr = Field(description="Suburb name")
    state: StrictStr = Field(description="State")
    postcode: StrictStr = Field(description="Postcode")
    latitude: Union[StrictFloat, StrictInt] = Field(description="Latitude")
    longitude: Union[StrictFloat, StrictInt] = Field(description="Longitude")
    zone_category: StrictStr = Field(description="Zone category (green, orange, red)")
    overall_score: Union[StrictFloat, StrictInt] = Field(description="Overall score (0-100)")
    appreciation_score: Union[StrictFloat, StrictInt] = Field(description="Appreciation score (0-100)")
    risk_score: Union[StrictFloat, StrictInt] = Field(description="Risk score (0-100)")
    liquidity_score: Union[StrictFloat, StrictInt] = Field(description="Liquidity score (0-100)")
    appreciation_confidence: Union[StrictFloat, StrictInt] = Field(description="Appreciation confidence (0-1)")
    risk_confidence: Union[StrictFloat, StrictInt] = Field(description="Risk confidence (0-1)")
    liquidity_confidence: Union[StrictFloat, StrictInt] = Field(description="Liquidity confidence (0-1)")
    overall_confidence: Union[StrictFloat, StrictInt] = Field(description="Overall confidence (0-1)")
    metrics: Dict[str, MetricValue] = Field(description="Metrics")
    property_count: StrictInt = Field(description="Number of properties")
    __properties: ClassVar[List[str]] = ["suburb_id", "name", "state", "postcode", "latitude", "longitude", "zone_category", "overall_score", "appreciation_score", "risk_score", "liquidity_score", "appreciation_confidence", "risk_confidence", "liquidity_confidence", "overall_confidence", "metrics", "property_count"]

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
        """Create an instance of SuburbDetail from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each value in metrics (dict)
        _field_dict = {}
        if self.metrics:
            for _key_metrics in self.metrics:
                if self.metrics[_key_metrics]:
                    _field_dict[_key_metrics] = self.metrics[_key_metrics].to_dict()
            _dict['metrics'] = _field_dict
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SuburbDetail from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "suburb_id": obj.get("suburb_id"),
            "name": obj.get("name"),
            "state": obj.get("state"),
            "postcode": obj.get("postcode"),
            "latitude": obj.get("latitude"),
            "longitude": obj.get("longitude"),
            "zone_category": obj.get("zone_category"),
            "overall_score": obj.get("overall_score"),
            "appreciation_score": obj.get("appreciation_score"),
            "risk_score": obj.get("risk_score"),
            "liquidity_score": obj.get("liquidity_score"),
            "appreciation_confidence": obj.get("appreciation_confidence"),
            "risk_confidence": obj.get("risk_confidence"),
            "liquidity_confidence": obj.get("liquidity_confidence"),
            "overall_confidence": obj.get("overall_confidence"),
            "metrics": dict(
                (_k, MetricValue.from_dict(_v))
                for _k, _v in obj["metrics"].items()
            )
            if obj.get("metrics") is not None
            else None,
            "property_count": obj.get("property_count")
        })
        return _obj


