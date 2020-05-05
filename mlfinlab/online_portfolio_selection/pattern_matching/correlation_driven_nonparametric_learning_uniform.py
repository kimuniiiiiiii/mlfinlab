# pylint: disable=missing-module-docstring
import numpy as np
from mlfinlab.online_portfolio_selection.universal_portfolio import UniversalPortfolio
from mlfinlab.online_portfolio_selection.pattern_matching.correlation_driven_nonparametric_learning import CorrelationDrivenNonparametricLearning


class CorrelationDrivenNonparametricLearningUniform(UniversalPortfolio):
    """
    This class implements the Correlation Driven Nonparametric Learning - Uniform strategy. It is
    reproduced with modification from the following paper:
    `Li, B., Hoi, S.C., & Gopalkrishnan, V. (2011). CORN: Correlation-driven nonparametric
    learning approach for portfolio selection. ACM TIST, 2,
    21:1-21:29.<https://dl.acm.org/doi/abs/10.1145/1961189.1961193>`_

    Correlation Driven Nonparametric Learning Uniform creates W experts that each follow the CORN
    strategy with the same rho value and different window values. After each period, the weights
    are evenly distributed among all the experts to follow the uniform weights allocation method
    for the universal portfolio strategy.
    """

    def __init__(self, window, rho):
        """
        Constructor.
        """
        self.window = window
        self.rho = rho
        self.number_of_experts = int(self.window)
        super().__init__(number_of_experts=self.number_of_experts, weighted='uniform')

    def _initialize(self, asset_prices, weights, resample_by):
        """
        Initializes the important variables for the object.

        :param asset_prices: (pd.DataFrame) Historical asset prices.
        :param weights: (list/np.array/pd.Dataframe) Initial weights set by the user.
        :param resample_by: (str) Specifies how to resample the prices.
        """
        # Check that window value is an integer.
        if not isinstance(self.window, int):
            raise ValueError("Window value must be an integer.")

        # Check that window value is at least 1.
        if self.window < 1:
            raise ValueError("Window value must be greater than or equal to 1.")

        # Check that rho is between -1 and 1.
        if self.rho < -1 or self.rho > 1:
            raise ValueError("Rho must be between -1 and 1.")

        super(CorrelationDrivenNonparametricLearningUniform, self)._initialize(asset_prices,
                                                                               weights,
                                                                               resample_by)

    def _generate_experts(self):
        """
        Generates W experts from window of 1 to w and same rho values.
        """
        # Initialize expert parameters.
        self.expert_params = np.zeros((self.number_of_experts, 2))
        # Assign number of windows to each experts.
        for n_window in range(self.window):
            self.expert_params[n_window-1] = [n_window + 1, self.rho]

        for exp in range(self.number_of_experts):
            param = self.expert_params[exp]
            self.experts.append(CorrelationDrivenNonparametricLearning(int(param[0]), param[1]))
