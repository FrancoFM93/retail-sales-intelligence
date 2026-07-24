-- Retail Sales Intelligence
-- Revenue definition: payment value from delivered orders purchased before
-- September 1, 2018. This excludes the sparse, incomplete 2018-09/2018-10 tail.

-- 1. Monthly revenue
WITH eligible_orders AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_purchase_timestamp::timestamp AS purchased_at,
        SUM(p.payment_value) AS payment_value
    FROM orders AS o
    INNER JOIN payments AS p
        ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
      AND o.order_purchase_timestamp::timestamp < DATE '2018-09-01'
    GROUP BY
        o.order_id,
        o.customer_id,
        o.order_purchase_timestamp
)
SELECT
    DATE_TRUNC('month', purchased_at) AS month,
    SUM(payment_value) AS revenue
FROM eligible_orders
GROUP BY DATE_TRUNC('month', purchased_at)
ORDER BY month;


-- 2. Top customers by revenue
WITH eligible_orders AS (
    SELECT
        o.order_id,
        o.customer_id,
        SUM(p.payment_value) AS payment_value
    FROM orders AS o
    INNER JOIN payments AS p
        ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
      AND o.order_purchase_timestamp::timestamp < DATE '2018-09-01'
    GROUP BY o.order_id, o.customer_id
)
SELECT
    c.customer_unique_id,
    SUM(eo.payment_value) AS total_spent
FROM eligible_orders AS eo
INNER JOIN customers AS c
    ON eo.customer_id = c.customer_id
GROUP BY c.customer_unique_id
ORDER BY total_spent DESC
LIMIT 10;


-- 3. Customer revenue concentration (Pareto curve)
WITH eligible_orders AS (
    SELECT
        o.order_id,
        o.customer_id,
        SUM(p.payment_value) AS payment_value
    FROM orders AS o
    INNER JOIN payments AS p
        ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
      AND o.order_purchase_timestamp::timestamp < DATE '2018-09-01'
    GROUP BY o.order_id, o.customer_id
),
customer_revenue AS (
    SELECT
        c.customer_unique_id,
        SUM(eo.payment_value) AS revenue
    FROM eligible_orders AS eo
    INNER JOIN customers AS c
        ON eo.customer_id = c.customer_id
    GROUP BY c.customer_unique_id
)
SELECT
    customer_unique_id,
    revenue,
    100.0 * ROW_NUMBER() OVER (ORDER BY revenue DESC)
        / COUNT(*) OVER () AS customer_pct,
    100.0 * SUM(revenue) OVER (
        ORDER BY revenue DESC
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) / SUM(revenue) OVER () AS cumulative_revenue_pct
FROM customer_revenue
ORDER BY revenue DESC;


-- 4. RFM metrics
WITH eligible_orders AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_purchase_timestamp::timestamp AS purchased_at,
        SUM(p.payment_value) AS payment_value
    FROM orders AS o
    INNER JOIN payments AS p
        ON o.order_id = p.order_id
    WHERE o.order_status = 'delivered'
      AND o.order_purchase_timestamp::timestamp < DATE '2018-09-01'
    GROUP BY
        o.order_id,
        o.customer_id,
        o.order_purchase_timestamp
)
SELECT
    c.customer_unique_id,
    DATE '2018-09-01' - MAX(eo.purchased_at)::date AS recency_days,
    COUNT(DISTINCT eo.order_id) AS frequency,
    SUM(eo.payment_value) AS monetary
FROM eligible_orders AS eo
INNER JOIN customers AS c
    ON eo.customer_id = c.customer_id
GROUP BY c.customer_unique_id
ORDER BY monetary DESC;
