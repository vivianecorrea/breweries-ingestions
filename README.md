# Breweries Ingestion

## 📌 Overview

This ingestion process retrieves brewery data from a public API:
🔗 Open Brewery DB API

## ⚙️ Orchestration
- Databricks Workflows

## 🚀 Project Decisions

We chose Databricks Workflows as the orchestration tool because it provides robust monitoring and observability features for ingestion.
	•	Data Extraction: Implemented using Python.
	•	Data Processing: All transformation layers are handled with PySpark.
	•	Modularization: Despite running within Databricks notebooks, the code is structured into reusable classes, making it easier to switch orchestration tools if needed.

## 🛠️ Technical Debt

Some best practices and requirements were omitted due to technical constraints in the development environment.
⚠️ This project was entirely developed on mobile devices, which imposed certain limitations.

🔄 Future Improvements:

- ✅ Unit and integration tests across all pipeline layers.
- ✅ Refactoring common functions (e.g., read/write operations) to avoid code duplication.
- ✅ CI/CD integration, enabling direct repository deployment to Databricks.
- ✅ Data quality monitoring and alerting using the Great Expectations framework.
