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

from equihome_sim_sdk.models.tranche_allocation_response import TrancheAllocationResponse

class TestTrancheAllocationResponse(unittest.TestCase):
    """TrancheAllocationResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TrancheAllocationResponse:
        """Test TrancheAllocationResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TrancheAllocationResponse`
        """
        model = TrancheAllocationResponse()
        if include_optional:
            return TrancheAllocationResponse(
                loan_id = '',
                allocation_percentage = 1.337,
                allocation_amount = 1.337,
                zone = '',
                ltv = 1.337
            )
        else:
            return TrancheAllocationResponse(
                loan_id = '',
                allocation_percentage = 1.337,
                allocation_amount = 1.337,
                zone = '',
                ltv = 1.337,
        )
        """

    def testTrancheAllocationResponse(self):
        """Test TrancheAllocationResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
