# coding: utf-8

"""
    EQU IHOME SIM ENGINE API

    API for running home equity investment fund simulations

    The version of the OpenAPI document: 0.1.0
    Contact: info@equihome.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from equihome_sim_sdk.models.simulation_result import SimulationResult

class TestSimulationResult(unittest.TestCase):
    """SimulationResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SimulationResult:
        """Test SimulationResult
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SimulationResult`
        """
        model = SimulationResult()
        if include_optional:
            return SimulationResult(
                simulation_id = '',
                status = '',
                created_at = '',
                completed_at = '',
                config = equihome_sim_sdk.models.config.Config(),
                metrics = equihome_sim_sdk.models.metrics.Metrics(),
                cashflows = [
                    None
                    ],
                capital_allocation = equihome_sim_sdk.models.capital_allocation.Capital Allocation(),
                loans = [
                    None
                    ],
                loan_portfolio = equihome_sim_sdk.models.loan_portfolio.Loan Portfolio(),
                execution_time = 1.337,
                guardrail_violations = [
                    None
                    ]
            )
        else:
            return SimulationResult(
                simulation_id = '',
                status = '',
                created_at = '',
                config = equihome_sim_sdk.models.config.Config(),
        )
        """

    def testSimulationResult(self):
        """Test SimulationResult"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
