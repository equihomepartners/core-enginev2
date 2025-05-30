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

from equihome_sim_sdk.models.market_metrics import MarketMetrics

class TestMarketMetrics(unittest.TestCase):
    """MarketMetrics unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> MarketMetrics:
        """Test MarketMetrics
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `MarketMetrics`
        """
        model = MarketMetrics()
        if include_optional:
            return MarketMetrics(
                beta = 1.337,
                alpha = 1.337,
                tracking_error = 1.337,
                r_squared = 1.337,
                upside_capture = 1.337,
                downside_capture = 1.337,
                upside_potential = 1.337,
                downside_risk = 1.337
            )
        else:
            return MarketMetrics(
        )
        """

    def testMarketMetrics(self):
        """Test MarketMetrics"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
