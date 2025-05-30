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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List
from equihome_sim_sdk.models.cash_reserve import CashReserve
from equihome_sim_sdk.models.src_api_routers_finance_liquidity_metrics import SrcApiRoutersFinanceLiquidityMetrics
from typing import Optional, Set
from typing_extensions import Self

class LiquidityAnalysis(BaseModel):
    """
    Liquidity analysis model.
    """ # noqa: E501
    cash_reserves: List[CashReserve] = Field(description="Cash reserves by year")
    liquidity_metrics: SrcApiRoutersFinanceLiquidityMetrics = Field(description="Liquidity metrics")
    __properties: ClassVar[List[str]] = ["cash_reserves", "liquidity_metrics"]

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
        """Create an instance of LiquidityAnalysis from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in cash_reserves (list)
        _items = []
        if self.cash_reserves:
            for _item_cash_reserves in self.cash_reserves:
                if _item_cash_reserves:
                    _items.append(_item_cash_reserves.to_dict())
            _dict['cash_reserves'] = _items
        # override the default output from pydantic by calling `to_dict()` of liquidity_metrics
        if self.liquidity_metrics:
            _dict['liquidity_metrics'] = self.liquidity_metrics.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of LiquidityAnalysis from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "cash_reserves": [CashReserve.from_dict(_item) for _item in obj["cash_reserves"]] if obj.get("cash_reserves") is not None else None,
            "liquidity_metrics": SrcApiRoutersFinanceLiquidityMetrics.from_dict(obj["liquidity_metrics"]) if obj.get("liquidity_metrics") is not None else None
        })
        return _obj


