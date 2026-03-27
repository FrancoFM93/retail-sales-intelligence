# 🛒 Retail Sales Intelligence

📊 Data analysis project focused on understanding revenue drivers and customer behavior in an e-commerce dataset.

---

## 🚀 Objective

Analyze how revenue is generated and identify opportunities to increase it using data-driven insights.

---

## 🧰 Tech Stack

* 🐍 Python (Pandas, NumPy)
* 🗄️ PostgreSQL
* 🔗 SQLAlchemy
* 📈 Matplotlib
* 📓 Jupyter Notebook

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

This project uses the Brazilian E-Commerce Public Dataset (Olist).

🔗 https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

### How to use

1. Download the dataset from Kaggle
2. Extract into: data/raw/
3. Ensure files like:
- olist_customers_dataset.csv
- olist_orders_dataset.csv
- olist_order_items_dataset.csv
- olist_order_payments_dataset.csv

are available before running the notebook.

## 🔍 Key Analysis

### 📈 Revenue Analysis

* Monthly revenue trend using SQL + Python
* Strong growth in 2017, stabilization in 2018
* Final drop likely due to incomplete data

---

### 👥 Customer Analysis (Pareto)

* ~49% of customers generate 80% of revenue
* Revenue is **more evenly distributed** than classic 80/20

---

### 🛍️ Order Behavior

* Most orders contain few items
* Opportunity to increase basket size
* Shipping costs impact profitability

---

### 🧠 RFM Segmentation

Customers segmented into:

* 🟣 VIP
* 🔵 Loyal
* 🟡 Regular
* 🔴 At Risk

Used to:

* Improve retention
* Target marketing strategies
* Increase customer lifetime value

---

## 📊 Visualizations

* Revenue trend over time
* Pareto distribution
* Customer segment distribution
* Revenue by segment

---

## ⚙️ Setup

### 1. Clone repository

```bash
git clone https://github.com/your-username/retail-sales-intelligence.git
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

---

## 🧠 How to Explain This Project (Interview)

* Built an end-to-end data analysis pipeline using Python and PostgreSQL
* Designed SQL queries to answer business questions
* Identified revenue concentration and customer segments
* Applied RFM analysis for customer segmentation
* Generated actionable business insights from raw data

---

## 📌 Future Improvements

* Dashboard (Streamlit / Power BI)
* Automated ETL pipeline
* Customer churn prediction model
* Product-level analysis

---

## 📬 Author

FrancoFM

