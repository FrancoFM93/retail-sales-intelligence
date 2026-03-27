# 🛒 Retail Sales Intelligence

📊 Data analysis project focused on understanding revenue drivers and customer behavior in an e-commerce dataset.

---

## 🚀 Objective

Analyze how revenue is generated and identify opportunities to increase it using data-driven insights.

Focus on combining SQL and Python to perform end-to-end exploratory data analysis and customer segmentation.

---

## 🧰 Tech Stack

* 🐍 Python (Pandas, NumPy, Matplotlib)
* 🗄️ PostgreSQL
* 🔗 SQLAlchemy
* 📓 Jupyter Notebook
* 🔄 SQL + Python integration

---

## 📂 Project Structure

```
retail-sales-intelligence/
 ┣ 📁 notebooks/       # Main analysis
 ┣ 📁 data/            # Raw data (ignored in Git)
 ┣ 📁 sql/             # SQL queries
 ┣ 📁 src/             # Future modular code
 ┣ 📁 models/          # Future ML models
 ┣ 📁 app/             # Future app/dashboard
 ┣ 📜 requirements.txt
 ┣ 📜 .gitignore
 ┗ 📜 README.md
```

---

## 📦 Dataset

This project uses the Brazilian E-Commerce Public Dataset (Olist):

🔗 [Kaggle - Brazilian E-Commerce Dataset (Olist)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)


## 🔍 Key Insights

### 📈 Revenue

* Revenue grows strongly during 2017 and stabilizes in 2018.
* Final drop likely due to incomplete data.

### 👥 Customers (Pareto)

* ~49% of customers generate 80% of revenue.
* Revenue is less concentrated than the classic 80/20 distribution.

### 🛍️ Orders

* Most orders contain few items.
* Indicates opportunity to increase average basket size.
* Shipping cost is a relevant component of order value.

### 🧠 Segmentation (RFM)

* VIP and Loyal customers drive a large portion of revenue.
* At Risk customers represent potential revenue loss.


---

## 📊 Visualizations

* Monthly revenue aggregation (Python).
* Revenue trend over time (SQL + visualization).
* Pareto distribution of revenue.
* Items per order distribution.
* Customer segment distribution (RFM).
* Revenue by customer segment.

---

## ⚙️ Setup

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

### 4. How to use the dataset

1. Download the dataset from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
2. Extract into: data/raw/
3. Ensure files like:
- olist_customers_dataset.csv
- olist_orders_dataset.csv
- olist_order_items_dataset.csv
- olist_order_payments_dataset.csv

are available before running the notebook.
---

## 📌 Future Improvements

* Dashboard (Streamlit / Power BI)
* Automated ETL pipeline
* Customer churn prediction model
* Product-level analysis

---

## 📬 Author

FrancoFM

