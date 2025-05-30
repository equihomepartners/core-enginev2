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

from equihome_sim_sdk.models.reinvestment_event_response import ReinvestmentEventResponse

class TestReinvestmentEventResponse(unittest.TestCase):
    """ReinvestmentEventResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ReinvestmentEventResponse:
        """Test ReinvestmentEventResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ReinvestmentEventResponse`
        """
        model = ReinvestmentEventResponse()
        if include_optional:
            return ReinvestmentEventResponse(
                event_id = '',
                timestamp = 1.337,
                year = 1.337,
                month = 56,
                amount = 1.337,
                source = '',
                source_details = equihome_sim_sdk.models.source_details.Source Details(),
                strategy_used = '',
                target_allocations = {
                    'key' : 1.337
                    },
                actual_allocations = {
                    'key' : 1.337
                    },
                num_loans_generated = 56,
                loan_ids = [
                    ''
                    ],
                performance_adjustments = {
                    'key' : 1.337
                    },
                cash_reserve_before = 1.337,
                cash_reserve_after = 1.337
            )
        else:
            return ReinvestmentEventResponse(
                event_id = '',
                timestamp = 1.337,
                year = 1.337,
                month = 56,
                amount = 1.337,
                source = '',
                source_details = equihome_sim_sdk.models.source_details.Source Details(),
                strategy_used = '',
                target_allocations = {
                    'key' : 1.337
                    },
                actual_allocations = {
                    'key' : 1.337
                    },
                num_loans_generated = 56,
                loan_ids = [
                    ''
                    ],
        )
        """

    def testReinvestmentEventResponse(self):
        """Test ReinvestmentEventResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
