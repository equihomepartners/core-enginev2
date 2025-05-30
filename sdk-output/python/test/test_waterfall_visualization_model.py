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

from equihome_sim_sdk.models.waterfall_visualization_model import WaterfallVisualizationModel

class TestWaterfallVisualizationModel(unittest.TestCase):
    """WaterfallVisualizationModel unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> WaterfallVisualizationModel:
        """Test WaterfallVisualizationModel
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `WaterfallVisualizationModel`
        """
        model = WaterfallVisualizationModel()
        if include_optional:
            return WaterfallVisualizationModel(
                waterfall_chart = [
                    equihome_sim_sdk.models.waterfall_chart_model.WaterfallChartModel(
                        category = '', 
                        amount = 1.337, )
                    ],
                distribution_by_year_chart = [
                    equihome_sim_sdk.models.distribution_by_year_model.DistributionByYearModel(
                        year = 56, 
                        lp_return_of_capital = 1.337, 
                        lp_preferred_return = 1.337, 
                        lp_residual = 1.337, 
                        gp_catch_up = 1.337, 
                        gp_carried_interest = 1.337, 
                        total = 1.337, )
                    ],
                tier_allocation_chart = [
                    equihome_sim_sdk.models.waterfall_tier_model.WaterfallTierModel(
                        tier = '', 
                        amount = 1.337, 
                        percentage = 1.337, )
                    ],
                stakeholder_allocation_chart = [
                    equihome_sim_sdk.models.stakeholder_allocation_model.StakeholderAllocationModel(
                        stakeholder = '', 
                        amount = 1.337, 
                        percentage = 1.337, )
                    ]
            )
        else:
            return WaterfallVisualizationModel(
                waterfall_chart = [
                    equihome_sim_sdk.models.waterfall_chart_model.WaterfallChartModel(
                        category = '', 
                        amount = 1.337, )
                    ],
                distribution_by_year_chart = [
                    equihome_sim_sdk.models.distribution_by_year_model.DistributionByYearModel(
                        year = 56, 
                        lp_return_of_capital = 1.337, 
                        lp_preferred_return = 1.337, 
                        lp_residual = 1.337, 
                        gp_catch_up = 1.337, 
                        gp_carried_interest = 1.337, 
                        total = 1.337, )
                    ],
                tier_allocation_chart = [
                    equihome_sim_sdk.models.waterfall_tier_model.WaterfallTierModel(
                        tier = '', 
                        amount = 1.337, 
                        percentage = 1.337, )
                    ],
                stakeholder_allocation_chart = [
                    equihome_sim_sdk.models.stakeholder_allocation_model.StakeholderAllocationModel(
                        stakeholder = '', 
                        amount = 1.337, 
                        percentage = 1.337, )
                    ],
        )
        """

    def testWaterfallVisualizationModel(self):
        """Test WaterfallVisualizationModel"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
