# Monitoring Plan

### **1. Data Drift Monitoring**

Data drift occurs when the statistical properties of the input features change over time compared to the training baseline, leading to silent model degradation.

- **What to Track:** Focus closely on the top features driving model predictions:
  
  - `recency_days` and `last_visit_days_ago` (which account for over 43% of model importance).
  
  - `monetary_180d` and `frequency_180d` (the core customer value indicators).
  
  - Categorical feature distributions such as `preferred_category` and `acquisition_channel`.

- **Metrics & Tools:** Compute the **Population Stability Index (PSI)** weekly comparing the distribution of incoming inference payloads against the `X_train_prepared.csv` training distribution baseline.

- **Alert Threshold:** A `PSI > 0.1` flags moderate drift (trigger an internal warning), while a `PSI > 0.25` indicates significant drift requiring immediate diagnostic review.

### **2. Prediction Distribution Monitoring**

Tracking the raw probabilities outputted by the model helps identify shifts in model behavior before actual downstream business outcomes can be calculated.

- **What to Track:** Monitor the continuous probability scores (`churn_probability`) and the resulting binary predictions (`predicted_class`).

- **Metrics & Tools:** Plot a daily histogram of predicted probabilities and track the daily **positive rate** (percentage of incoming customers flagged as "At-Risk" at our $\pi = 0.2$ threshold).

- **Alert Threshold:** If the daily percentage of users flagged for churn suddenly spikes or drops by more than $\pm 15\%$ compared to the moving 30-day average, alert the data engineering team to investigate upstream pipeline changes or payload formatting bugs.

### **3. Business Outcome Monitoring**

This connects machine learning metrics back to financial realities, verifying if the retention campaigns are successful.

- **What to Track:** Because our ground-truth labels take 60 days to mature, business outcomes are tracked on a rolling 60-day lag.

- **Metrics & Tools:** * **True Retention Lift:** Compare the actual survival rate of at-risk users who received a campaign intervention versus the control group.
  
  - **Budget Burn Rate:** Track cumulative outreach spend against our strict **Rs.15,000** cap.
  
  - **Financial ROI:** Calculate the total net revenue saved by successful interventions versus the direct promotional margin dilution from False Positives.

### **4. API Performance and Error Monitoring**

Standard software reliability engineering (SRE) metrics are required to guarantee that the FastAPI application satisfies server uptime agreements.

- **What to Track:** The standard **RED method** metrics:
  
  - **Rate:** Total requests per second handled by the `/predict` and `/batch_predict` endpoints.
  
  - **Errors:** Frequency of non-200 HTTP status codes (specifically `422 Unprocessable Entity` for schema validation failures and `500 Internal Server Error`).
  
  - **Duration:** API endpoint latency (p50, p95, and p99 response times).

- **Metrics & Tools:** Use **Prometheus** to scrape FastAPI metrics and visualize them on a **Grafana** dashboard, setting up alerts via Slack or PagerDuty for any sustained availability drops.

- **Alert Threshold:** Trigger critical alerts if latency p99 exceeds **200ms** or if the error rate exceeds **1%** of total traffic over a 5-minute rolling window.

### **5. Retraining Triggers**

Model performance inevitably degrades over time due to shifting macroeconomic conditions, changes in customer behavior, or marketing campaign effects. The model must be automatically scheduled for retraining when specific conditions are met.

- **Performance Trigger:** Retrain if the out-of-sample evaluation **F1-Score** drops below **$75\%$** (baseline test was $80.12\%$) or if the **ROC-AUC** falls below **0.82** over a mature 60-day evaluation cohort.

- **Data Drift Trigger:** Retrain if the average feature-level **PSI remains above 0.25** for three consecutive weekly tracking cycles, confirming a permanent structural shift in consumer behavior.

- **Temporal Trigger:** Independent of performance metrics, enforce a **mandatory semi-annual (6-month) scheduled retrain** to ensure the core tree-ensemble architectures capture recent product line additions and newer user cohorts natively.
