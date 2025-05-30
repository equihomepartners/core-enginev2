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

from equihome_sim_sdk.models.coverage_test_response import CoverageTestResponse

class TestCoverageTestResponse(unittest.TestCase):
    """CoverageTestResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CoverageTestResponse:
        """Test CoverageTestResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CoverageTestResponse`
        """
        model = CoverageTestResponse()
        if include_optional:
            return CoverageTestResponse(
                test_type = '',
                test_date = '',
                year = 1.337,
                month = 56,
                threshold = 1.337,
                actual_value = 1.337,
                passed = True,
                cure_deadline = '',
                cured = True
            )
        else:
            return CoverageTestResponse(
                test_type = '',
                test_date = '',
                year = 1.337,
                month = 56,
                threshold = 1.337,
                actual_value = 1.337,
                passed = True,
        )
        """

    def testCoverageTestResponse(self):
        """Test CoverageTestResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
