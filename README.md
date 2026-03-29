# Retail Sales Intelligence

Data analysis project focused on understanding revenue drivers and customer behavior in an e-commerce dataset, with an interactive Streamlit dashboard.

---

## Objective

Analyze how revenue is generated and identify opportunities to increase it using data-driven insights.

Combines SQL and Python to perform end-to-end exploratory data analysis, customer segmentation, and interactive visualization.

---

## Tech Stack

* Python (Pandas, NumPy, Matplotlib, Seaborn)
* Streamlit
* PostgreSQL
* SQLAlchemy
* Jupyter Notebook

---

## Project Structure

```
retail-sales-intelligence/
 ┣ app/
 ┃ ┣ Home.py                  # Dashboard home — KPIs + overview charts
 ┃ ┗ pages/
 ┃   ┣ 1_Revenue.py           # Monthly revenue trend with year filter
 ┃   ┣ 2_Customers.py         # Pareto analysis + items per order
 ┃   ┗ 3_Segmentation.py      # RFM segmentation explorer
 ┣ src/
 ┃ ┣ data_loader.py           # CSV loaders for all Olist tables
 ┃ ┣ transforms.py            # Revenue aggregations, Pareto, merges
 ┃ ┗ segmentation.py          # RFM scoring and customer segmentation
 ┣ notebooks/
 ┃ ┗ 01_data_loading.ipynb    # Original EDA and analysis
 ┣ data/                      # Raw data (ignored in Git)
 ┣ sql/                       # SQL queries
 ┣ models/                    # Future ML models
 ┣ requirements.txt
 ┗ README.md
```

---

## Dataset

This project uses the Brazilian E-Commerce Public Dataset (Olist):

[Kaggle - Brazilian E-Commerce Dataset (Olist)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

---

## Setup

### 1. Clone repository

```bash
git clone https://github.com/FrancoFM93/retail-sales-intelligence
cd retail-sales-intelligence
```

### 2. Create environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add the dataset

1. Download from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
2. Extract into `data/raw/` — the following files are required:
   - `olist_customers_dataset.csv`
   - `olist_orders_dataset.csv`
   - `olist_order_items_dataset.csv`
   - `olist_order_payments_dataset.csv`

### 5. Run the dashboard

```bash
streamlit run app/Home.py
```

Opens at **http://localhost:8501**

---

## Dashboard Pages

### Home
Overview of the full dataset: total revenue, orders, customers, average order value, revenue trend, and revenue by RFM segment.

### Revenue
Monthly revenue time-series with year filter and expandable breakdown table.

### Customers
- **Pareto curve** — interactive slider to see what % of customers drives a chosen % of revenue
- **Items per order** — distribution histogram with configurable cap

### Segmentation
- Per-segment KPIs (customer count + revenue)
- Bar charts for customer distribution and revenue by segment
- Scatter plot: Recency vs Monetary, colored by segment
- Drill-down table to explore individual customers within a segment

---

## Key Insights

### Revenue
* Revenue grows strongly during 2017 and stabilizes in 2018.
* Final drop likely due to incomplete data.

### Customers (Pareto)
* ~49% of customers generate 80% of revenue.
* Revenue is less concentrated than the classic 80/20 rule.

### Orders
* Most orders contain a single item — opportunity to increase average basket size.
* Shipping cost is a relevant component of order value.

### Segmentation (RFM)
* VIP and Loyal customers drive the majority of revenue.
* At Risk customers (~24% of the base) represent significant potential revenue loss.

---

## Roadmap

* Automated ETL pipeline
* Customer churn prediction model
* Product-level analysis

---

## Author

FrancoFM
