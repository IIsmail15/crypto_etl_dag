# 🪙 Crypto ETL Pipeline with Apache Airflow

This project demonstrates a simple Extract-Transform-Load (ETL) pipeline for cryptocurrency market data using **Apache Airflow**, **Python**, and the **CoinGecko API**.

---

## 🚀 Features

- Extracts top 10 cryptocurrencies by market cap from CoinGecko
- Transforms JSON data into a clean CSV format
- Stores raw and transformed data in a local folder
- Runs on Airflow with Docker Compose
- Uses LocalExecutor with PostgreSQL as metadata DB

---

## 📁 Project Structure

```
├── dags/ # Airflow DAGs
│ └── crypto_etl_dag.py # Main ETL DAG
├── data/ # Saved raw + transformed data (mounted volume)
├── plugins/ # (Optional) custom operators/hooks
├── docker-compose.yml # Docker setup for Airflow + Postgres
├── .env.example # Environment variable template
├── .gitignore # Ignores real .env and logs
└── README.md # This file


```
---

## ⚙️ Setup Instructions

### 1. Clone this repository

```bash
git clone https://github.com/IIsmail15/crypto_etl_dag.git
cd crypto_etl_dag
```

 ### 2. Create your .env file
 

```
cp .env.example .env

```

### 3. Create necessary folders


```
mkdir -p dags logs plugins output

```

###  Build and run Airflow


```
docker compose up --build

```
Airflow UI will be available at: http://localhost:8080
Login using the credentials from your .env file.

## 📅 DAG Overview

- **DAG ID**: `crypto_etl_pipeline_etl_steps`
- **Schedule**: Daily (`@daily`)

### Tasks

1. **extract_crypto_data** – Fetches JSON from CoinGecko API  
2. **transform_crypto_data** – Converts to DataFrame and saves CSV  
3. **load_crypto_data** – Prints a confirmation (simulating a load step)

---

## 📂 Output Files

After the DAG runs successfully, you should see:

- `data/raw_crypto.json`
- `data/crypto_prices.csv`

---

## 📜 License

**MIT** — free to use, modify, and share.
