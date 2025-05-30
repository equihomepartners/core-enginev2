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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from equihome_sim_sdk.models.cashflow_metrics import CashflowMetrics
from equihome_sim_sdk.models.cashflow_visualization import CashflowVisualization
from equihome_sim_sdk.models.fund_level_cashflow import FundLevelCashflow
from equihome_sim_sdk.models.liquidity_analysis import LiquidityAnalysis
from equihome_sim_sdk.models.loan_level_cashflow import LoanLevelCashflow
from equihome_sim_sdk.models.scenario_analysis import ScenarioAnalysis
from equihome_sim_sdk.models.sensitivity_analysis import SensitivityAnalysis
from equihome_sim_sdk.models.tax_impact_analysis import TaxImpactAnalysis
from typing import Optional, Set
from typing_extensions import Self

class CashflowCalculationResponse(BaseModel):
    """
    Response model for cashflow calculation.
    """ # noqa: E501
    simulation_id: StrictStr = Field(description="Simulation ID")
    loan_level_cashflows: Optional[List[LoanLevelCashflow]] = Field(default=None, description="Loan-level cashflows")
    fund_level_cashflows: List[FundLevelCashflow] = Field(description="Fund-level cashflows")
    stakeholder_cashflows: Dict[str, List[Any]] = Field(description="Stakeholder cashflows")
    visualization: CashflowVisualization = Field(description="Visualization data")
    metrics: Optional[CashflowMetrics] = Field(default=None, description="Cashflow metrics")
    sensitivity_analysis: Optional[SensitivityAnalysis] = Field(default=None, description="Sensitivity analysis results")
    scenario_analysis: Optional[ScenarioAnalysis] = Field(default=None, description="Scenario analysis results")
    tax_impact: Optional[TaxImpactAnalysis] = Field(default=None, description="Tax impact analysis results")
    liquidity_analysis: Optional[LiquidityAnalysis] = Field(default=None, description="Liquidity analysis results")
    __properties: ClassVar[List[str]] = ["simulation_id", "loan_level_cashflows", "fund_level_cashflows", "stakeholder_cashflows", "visualization", "metrics", "sensitivity_analysis", "scenario_analysis", "tax_impact", "liquidity_analysis"]

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
        """Create an instance of CashflowCalculationResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in loan_level_cashflows (list)
        _items = []
        if self.loan_level_cashflows:
            for _item_loan_level_cashflows in self.loan_level_cashflows:
                if _item_loan_level_cashflows:
                    _items.append(_item_loan_level_cashflows.to_dict())
            _dict['loan_level_cashflows'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in fund_level_cashflows (list)
        _items = []
        if self.fund_level_cashflows:
            for _item_fund_level_cashflows in self.fund_level_cashflows:
                if _item_fund_level_cashflows:
                    _items.append(_item_fund_level_cashflows.to_dict())
            _dict['fund_level_cashflows'] = _items
        # override the default output from pydantic by calling `to_dict()` of visualization
        if self.visualization:
            _dict['visualization'] = self.visualization.to_dict()
        # override the default output from pydantic by calling `to_dict()` of metrics
        if self.metrics:
            _dict['metrics'] = self.metrics.to_dict()
        # override the default output from pydantic by calling `to_dict()` of sensitivity_analysis
        if self.sensitivity_analysis:
            _dict['sensitivity_analysis'] = self.sensitivity_analysis.to_dict()
        # override the default output from pydantic by calling `to_dict()` of scenario_analysis
        if self.scenario_analysis:
            _dict['scenario_analysis'] = self.scenario_analysis.to_dict()
        # override the default output from pydantic by calling `to_dict()` of tax_impact
        if self.tax_impact:
            _dict['tax_impact'] = self.tax_impact.to_dict()
        # override the default output from pydantic by calling `to_dict()` of liquidity_analysis
        if self.liquidity_analysis:
            _dict['liquidity_analysis'] = self.liquidity_analysis.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CashflowCalculationResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "simulation_id": obj.get("simulation_id"),
            "loan_level_cashflows": [LoanLevelCashflow.from_dict(_item) for _item in obj["loan_level_cashflows"]] if obj.get("loan_level_cashflows") is not None else None,
            "fund_level_cashflows": [FundLevelCashflow.from_dict(_item) for _item in obj["fund_level_cashflows"]] if obj.get("fund_level_cashflows") is not None else None,
            "stakeholder_cashflows": obj.get("stakeholder_cashflows"),
            "visualization": CashflowVisualization.from_dict(obj["visualization"]) if obj.get("visualization") is not None else None,
            "metrics": CashflowMetrics.from_dict(obj["metrics"]) if obj.get("metrics") is not None else None,
            "sensitivity_analysis": SensitivityAnalysis.from_dict(obj["sensitivity_analysis"]) if obj.get("sensitivity_analysis") is not None else None,
            "scenario_analysis": ScenarioAnalysis.from_dict(obj["scenario_analysis"]) if obj.get("scenario_analysis") is not None else None,
            "tax_impact": TaxImpactAnalysis.from_dict(obj["tax_impact"]) if obj.get("tax_impact") is not None else None,
            "liquidity_analysis": LiquidityAnalysis.from_dict(obj["liquidity_analysis"]) if obj.get("liquidity_analysis") is not None else None
        })
        return _obj


