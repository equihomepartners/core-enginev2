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

from equihome_sim_sdk.models.cashflow_heatmap_item import CashflowHeatmapItem

class TestCashflowHeatmapItem(unittest.TestCase):
    """CashflowHeatmapItem unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CashflowHeatmapItem:
        """Test CashflowHeatmapItem
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CashflowHeatmapItem`
        """
        model = CashflowHeatmapItem()
        if include_optional:
            return CashflowHeatmapItem(
                year = 56,
                month = 56,
                category = '',
                amount = 1.337
            )
        else:
            return CashflowHeatmapItem(
                year = 56,
                month = 56,
                category = '',
                amount = 1.337,
        )
        """

    def testCashflowHeatmapItem(self):
        """Test CashflowHeatmapItem"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
