# Retail Sales Intelligence

Retail Sales Intelligence is an interactive Streamlit application for analyzing revenue, customer behavior, and RFM segmentation using the Brazilian E-Commerce Public Dataset by Olist.

## Objective

Analyze revenue generation, customer behavior, purchase patterns, and RFM segmentation to identify business opportunities.

## Live Demo

Live demo: To be added after deployment.

## Application

The dashboard includes four pages:

- **Home** - Summary metrics for revenue, orders, customers, and average order value, plus revenue and segment overviews.
- **Revenue** - Monthly revenue trends with year filtering and a detailed monthly breakdown.
- **Customers** - Revenue concentration through Pareto analysis and the distribution of items per order.
- **Segmentation** - RFM customer segments, segment-level revenue and customer counts, a recency-versus-monetary view, and customer drill-down.

## Technology Stack

- Python
- Pandas
- Matplotlib
- Streamlit

## Dataset

The project uses the [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

For reproducibility and deployment, the repository includes the four Olist CSV files used by the application:

- `olist_customers_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_order_items_dataset.csv`
- `olist_order_payments_dataset.csv`

These files are stored in `data/raw/`.

## Project Structure

```text
retail-sales-intelligence/
|-- app/
|   |-- Home.py
|   `-- pages/
|       |-- 1_Revenue.py
|       |-- 2_Customers.py
|       `-- 3_Segmentation.py
|-- data/
|   `-- raw/
|       |-- olist_customers_dataset.csv
|       |-- olist_orders_dataset.csv
|       |-- olist_order_items_dataset.csv
|       `-- olist_order_payments_dataset.csv
|-- notebooks/
|   `-- 01_data_loading.ipynb
|-- src/
|   |-- __init__.py
|   |-- data_loader.py
|   |-- segmentation.py
|   `-- transforms.py
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Local Setup

From the repository root in Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
streamlit run app/Home.py
```

The application opens at `http://localhost:8501`.

## Key Insights

- Revenue increased strongly throughout 2017 and remained relatively stable during most of 2018.
- Approximately half of customers generated 80% of total revenue, showing less concentration than the traditional 80/20 pattern.
- Most orders contained a single item, suggesting an opportunity to improve average basket size.
- VIP and Loyal customers represented a significant share of revenue, while At Risk customers showed potential retention opportunities.

## Future Improvements

- Product and category-level analysis
- Automated data preparation
- Customer churn modeling
- Additional interactive filters

## Author

FrancoFM93

