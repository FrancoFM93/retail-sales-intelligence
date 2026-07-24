import unittest

import pandas as pd

from src.segmentation import _segment_customer


class SegmentationRuleTests(unittest.TestCase):
    def test_one_time_buyers_cannot_be_vip_or_loyal(self):
        # Even the best recency and monetary scores cannot override the
        # requirement that VIP and Loyal customers must have repeat orders.
        recent_high_value = pd.Series(
            {"frequency": 1, "R_score": 5, "M_score": 5}
        )

        self.assertEqual(_segment_customer(recent_high_value), "Regular")

    def test_repeat_buyers_follow_documented_rules(self):
        # These small Series isolate each business rule without needing to
        # load the full CSV dataset.
        vip = pd.Series({"frequency": 2, "R_score": 4, "M_score": 4})
        loyal = pd.Series({"frequency": 2, "R_score": 3, "M_score": 2})
        at_risk = pd.Series({"frequency": 3, "R_score": 2, "M_score": 5})

        self.assertEqual(_segment_customer(vip), "VIP")
        self.assertEqual(_segment_customer(loyal), "Loyal")
        self.assertEqual(_segment_customer(at_risk), "At Risk")


if __name__ == "__main__":
    unittest.main()
