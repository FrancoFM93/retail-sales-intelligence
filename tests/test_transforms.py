import unittest

import pandas as pd

from src.transforms import (
    build_full_df,
    get_items_per_order,
    get_monthly_revenue,
    get_pareto,
)


class RevenueTests(unittest.TestCase):
    def setUp(self):
        # Arrange a small dataset containing one valid order, one canceled
        # order, and one order exactly on the excluded cutoff date.
        self.orders = pd.DataFrame(
            {
                "order_id": ["delivered", "canceled", "incomplete_month"],
                "customer_id": ["c1", "c2", "c3"],
                "order_status": ["delivered", "canceled", "delivered"],
                "order_purchase_timestamp": pd.to_datetime(
                    ["2018-08-15", "2018-08-16", "2018-09-01"]
                ),
            }
        )
        self.payments = pd.DataFrame(
            {
                # Two payment rows for the valid order also protect the rule
                # that revenue sums payments without double-counting orders.
                "order_id": ["delivered", "delivered", "canceled", "incomplete_month"],
                "payment_value": [60.0, 40.0, 500.0, 900.0],
            }
        )
        self.customers = pd.DataFrame(
            {
                "customer_id": ["c1", "c2", "c3"],
                "customer_unique_id": ["u1", "u2", "u3"],
            }
        )

    def test_revenue_uses_delivered_orders_before_cutoff(self):
        # Act: run the same join and monthly aggregation used by the dashboard.
        result = build_full_df(self.orders, self.payments, self.customers)

        # Assert: only the valid order remains, but both of its payments count.
        self.assertEqual(result["order_id"].unique().tolist(), ["delivered"])
        self.assertEqual(result["payment_value"].sum(), 100.0)

        monthly = get_monthly_revenue(result)
        self.assertEqual(monthly["payment_value"].tolist(), [100.0])
        self.assertEqual(monthly["month"].dt.strftime("%Y-%m").tolist(), ["2018-08"])


class ParetoTests(unittest.TestCase):
    def test_pareto_calculates_customer_and_cumulative_percentages(self):
        # Values are already sorted, matching get_customer_revenue's contract.
        customer_revenue = pd.DataFrame(
            {
                "customer_unique_id": ["a", "b", "c"],
                "payment_value": [60.0, 30.0, 10.0],
            }
        )

        result = get_pareto(customer_revenue)

        # The second of three customers represents 66.67% of customers and
        # brings cumulative revenue from 60% to 90%.
        self.assertEqual(result["cumulative_pct"].tolist(), [60.0, 90.0, 100.0])
        self.assertAlmostEqual(result.loc[1, "customer_pct"], 200 / 3)


class ItemsPerOrderTests(unittest.TestCase):
    def test_counts_items_only_for_valid_orders(self):
        order_items = pd.DataFrame(
            {
                "order_id": [
                    "multi_item",
                    "multi_item",
                    "multi_item",
                    "single_item",
                    "canceled",
                    "unavailable",
                ],
                "order_item_id": [1, 2, 3, 1, 1, 1],
            }
        )
        valid_order_ids = pd.Series(["multi_item", "single_item"])

        result = get_items_per_order(order_items, valid_order_ids)

        expected = pd.DataFrame(
            {
                "order_id": ["multi_item", "single_item"],
                "item_count": [3, 1],
            }
        )
        pd.testing.assert_frame_equal(result, expected)


if __name__ == "__main__":
    unittest.main()
