# Capstone Project: D2C Customer Churn Intelligence & Retention API

## Part 4 — FastAPI Churn Scoring Service & Reproducible ML Workflow

### Objective

The company wants a simple internal service that can return churn-risk predictions to a CRM system. In this part, you must create a FastAPI application that loads a churn model and exposes prediction endpoints.

### Tasks

1. Create a FastAPI app with at least the following endpoints:
   •    GET /health
   •    POST /predict for one customer feature payload
   •    POST /batch_predict for multiple customer payloads
2. Load the saved model and return 
   •    churn probability, 
   •    predicted class, 
   •    a short risk explanation.
3. Add input validation using Pydantic models.
4. Add at least 3 test cases for the API.
5. Add a reproducibility setup using requirements.txt; Docker is optional but will receive credit if working.
6. Add a short monitoring plan explaining what should be tracked after deployment, including: 
   •    data drift,
   •    prediction distribution,
   •    business outcomes,
   •    API errors,
   •    retraining triggers.
7. Include a short note on responsible use: how the API output should and should not be used by the retention team.

### Execution Pre-Requisites :

1. Install Docker, Python to read & execute ".py" files

2. Install additional python modules as given in "requirements.txt"

3. Build Docker image using below command :
   
   1. `docker build -t churn-api:v1.0.0 .`

4. ### Input Files

| File Name          | Description                                                      |
| ------------------ | ---------------------------------------------------------------- |
| `model.pkl`        | Trained model, prepared in Part 4                                |
| `metrics.json`     | File prepared in Part 3 with Threshold value used for processing |
| `requirements.txt` | List of Python modules required                                  |
| `Dockerfile`       | File used to build     Docker container                          |
| `main.py`          | Python program to run the services                               |

### Program Execution

```
1. Program is run within the Docker image. Run Docker image 
using below command :
  
  `docker run -d --name churn_service -p 8000:8000 churn-api:v1.0.0`
```

### Output Data Files (Under "data" folder)

| File Name                                                                   | Description                                                                                                                                                                            |
| --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model.pkl`                                                                 | Trained model, saved for Part 4                                                                                                                                                        |
| `metrics.json`                                                              | file with <br/>a) key model metrics - accuracy, precision, recall, F1-score, ROC-AUC<br/>b) Confusion matrix values - at 0.5 (default) and threshold value<br/>c) Threshold value<br/> |
| X_train_prepared.csv    <br/>X_test_prepared.csv    <br/>X_val_prepared.csv | Stored Train, Test and Validation data - generated on every run                                                                                                                        |
| y_train_prepared.csv<br/>y_test_prepared.csv<br/>y_val_prepared.csv         | Stored Train, Test and Validation data - generated on every run                                                                                                                        |





### Documents

| File Name             | Description                                 |
| --------------------- | ------------------------------------------- |
| `monitoring_plan.md`  | Monitoring plan for service                 |
| `usage_guidelines.md` | How the model should and should not be used |
