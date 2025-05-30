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

from equihome_sim_sdk.models.property_value_response import PropertyValueResponse

class TestPropertyValueResponse(unittest.TestCase):
    """PropertyValueResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PropertyValueResponse:
        """Test PropertyValueResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PropertyValueResponse`
        """
        model = PropertyValueResponse()
        if include_optional:
            return PropertyValueResponse(
                property_id = '',
                initial_value = 1.337,
                current_value = 1.337,
                appreciation = 1.337,
                month = 56,
                year = 1.337
            )
        else:
            return PropertyValueResponse(
                property_id = '',
                initial_value = 1.337,
                current_value = 1.337,
                appreciation = 1.337,
                month = 56,
                year = 1.337,
        )
        """

    def testPropertyValueResponse(self):
        """Test PropertyValueResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
