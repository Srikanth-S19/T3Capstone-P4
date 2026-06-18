###############################################################################
## Name : Srikanth S
## ID : IITP_AIML_2506387
## Capstone Project: D2C Customer Churn Intelligence & Retention API
## Part 4 - FastAPI Churn Scoring Service & Reproducible ML Workflow
###############################################################################

import os
import json
import pickle
import numpy as np
import pandas as pd
from typing import List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

# Initialize the FastAPI App instance
app = FastAPI(
    title="Customer Churn Inference Service",
    description="Production REST API service for real-time and batch customer churn risk assessment.",
    version="1.0.0"
)

# Global model artifact reference
MODEL_PATH = "model.pkl"
model = None

# Load Threshold value from metrics.json
with open("metrics.json", "r") as json_file:
    json_data = json.load(json_file)

threshold_list = json_data["threshold"]
first_row = threshold_list[0]
threshold = first_row["0"]
print (f"Loaded threshold value = {threshold}")


# Define the expected feature order to guarantee absolute alignment with the serialized model
FEATURE_NAMES = [
    'recency_days', 'frequency_180d', 'monetary_180d', 'return_rate_180d', 'avg_discount_pct_180d', 
    'avg_rating_180d', 'category_diversity_180d', 'ticket_count_90d', 'negative_ticket_rate_90d', 
    'avg_resolution_hours_90d', 'days_since_signup', 'sessions_30d', 'product_views_30d', 
    'cart_adds_30d', 'wishlist_adds_30d', 'abandoned_carts_30d', 'email_opens_30d', 
    'campaign_clicks_30d', 'last_visit_days_ago', 'city_tier_Tier 1', 'city_tier_Tier 2', 
    'city_tier_Tier 3', 'age_group_18-24', 'age_group_25-34', 'age_group_35-44', 'age_group_45+', 
    'acquisition_channel_Google Search', 'acquisition_channel_Influencer', 'acquisition_channel_Instagram', 
    'acquisition_channel_Marketplace', 'acquisition_channel_Organic', 'acquisition_channel_Referral', 
    'loyalty_tier_Gold', 'loyalty_tier_None', 'loyalty_tier_Platinum', 'loyalty_tier_Silver', 
    'preferred_category_Baby Care', 'preferred_category_Fragrance', 'preferred_category_Hair Care', 
    'preferred_category_Makeup', 'preferred_category_Skin Care', 'preferred_category_Wellness', 
    'marketing_consent_No', 'marketing_consent_Yes'
]

# -----------------------------------------------------------------------------
# 1. APPLICATION LIFECYCLE EVENT HANDLERS
# -----------------------------------------------------------------------------
@app.on_event("startup")
def load_serialized_model():
    """
    Loads the trained model file from the disk into memory upon application server startup.
    """
    global model
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Critical Error: Serialized model file '{MODEL_PATH}' was not found.")
    
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    print(f"Model successfully loaded from '{MODEL_PATH}'. Inference Engine Ready.")


# -----------------------------------------------------------------------------
# 2. PYDANTIC INPUT DATA STRUCTURES FOR VALIDATION
# -----------------------------------------------------------------------------
class CustomerFeatures(BaseModel):
    """
    Validates input payloads to match the structured feature space required by the model.
    """
    recency_days: float = Field(..., description="Standardized value for days since last purchase.")
    frequency_180d: float = Field(..., description="Standardized value for total orders placed in past 180 days.")
    monetary_180d: float = Field(..., description="Standardized value for net spend amount in past 180 days.")
    return_rate_180d: float = Field(0.0, description="Standardized product return rate.")
    avg_discount_pct_180d: float = Field(0.0, description="Standardized average discount consumed.")
    avg_rating_180d: float = Field(0.0, description="Standardized product feedback score.")
    category_diversity_180d: float = Field(0.0, description="Standardized number of unique categories purchased.")
    ticket_count_90d: float = Field(0.0, description="Standardized count of support tickets.")
    negative_ticket_rate_90d: float = Field(0.0, description="Standardized rate of poorly resolved cases.")
    avg_resolution_hours_90d: float = Field(0.0, description="Standardized ticket resolution times.")
    days_since_signup: float = Field(..., description="Standardized customer lifespan tenure in days.")
    sessions_30d: float = Field(0.0, description="Standardized user platform logins in past 30 days.")
    product_views_30d: float = Field(0.0, description="Standardized product page views.")
    cart_adds_30d: float = Field(0.0, description="Standardized cart addition increments.")
    wishlist_adds_30d: float = Field(0.0, description="Standardized wishlist saves.")
    abandoned_carts_30d: float = Field(0.0, description="Standardized uncompleted checkout instances.")
    email_opens_30d: float = Field(0.0, description="Standardized marketing email open count.")
    campaign_clicks_30d: float = Field(0.0, description="Standardized outbound marketing clicks.")
    last_visit_days_ago: float = Field(..., description="Standardized days since last web/app login.")
    
    # One-Hot Encoded flags (Defaulting to 0.0 for ease of payload submission)
    city_tier_Tier_1: float = Field(0.0, alias="city_tier_Tier 1")
    city_tier_Tier_2: float = Field(0.0, alias="city_tier_Tier 2")
    city_tier_Tier_3: float = Field(0.0, alias="city_tier_Tier 3")
    age_group_18_24: float = Field(0.0, alias="age_group_18-24")
    age_group_25_34: float = Field(0.0, alias="age_group_25-34")
    age_group_35_44: float = Field(0.0, alias="age_group_35-44")
    age_group_45_plus: float = Field(0.0, alias="age_group_45+")
    acquisition_channel_Google_Search: float = Field(0.0, alias="acquisition_channel_Google Search")
    acquisition_channel_Influencer: float = Field(0.0, alias="acquisition_channel_Influencer")
    acquisition_channel_Instagram: float = Field(0.0, alias="acquisition_channel_Instagram")
    acquisition_channel_Marketplace: float = Field(0.0, alias="acquisition_channel_Marketplace")
    acquisition_channel_Organic: float = Field(0.0, alias="acquisition_channel_Organic")
    acquisition_channel_Referral: float = Field(0.0, alias="acquisition_channel_Referral")
    loyalty_tier_Gold: float = Field(0.0, alias="loyalty_tier_Gold")
    loyalty_tier_None: float = Field(0.0, alias="loyalty_tier_None")
    loyalty_tier_Platinum: float = Field(0.0, alias="loyalty_tier_Platinum")
    loyalty_tier_Silver: float = Field(0.0, alias="loyalty_tier_Silver")
    preferred_category_Baby_Care: float = Field(0.0, alias="preferred_category_Baby Care")
    preferred_category_Fragrance: float = Field(0.0, alias="preferred_category_Fragrance")
    preferred_category_Hair_Care: float = Field(0.0, alias="preferred_category_Hair Care")
    preferred_category_Makeup: float = Field(0.0, alias="preferred_category_Makeup")
    preferred_category_Skin_Care: float = Field(0.0, alias="preferred_category_Skin Care")
    preferred_category_Wellness: float = Field(0.0, alias="preferred_category_Wellness")
    marketing_consent_No: float = Field(0.0, alias="marketing_consent_No")
    marketing_consent_Yes: float = Field(0.0, alias="marketing_consent_Yes")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "recency_days": -0.5, "frequency_180d": 1.2, "monetary_180d": 0.8,
                "days_since_signup": 0.3, "last_visit_days_ago": -0.6,
                "city_tier_Tier 1": 1.0, "loyalty_tier_Platinum": 1.0, "preferred_category_Skin Care": 1.0
            }
        }
    }


# -----------------------------------------------------------------------------
# 3. OUTPUT RESPONSE STRUCTURES
# -----------------------------------------------------------------------------
class SingleChurnPrediction(BaseModel):
    churn_probability: float = Field(..., description="Probability of churn bounded between 0.0 and 1.0.")
    predicted_class: int = Field(..., description="Binary churn prediction: 1 = Churned, 0 = Retained.")
    risk_explanation: str = Field(..., description="Automated qualitative explanation detailing primary risk drivers.")

class BatchChurnPrediction(BaseModel):
    total_records_processed: int
    predictions: List[SingleChurnPrediction]


# -----------------------------------------------------------------------------
# 4. EXPLANATION GENERATOR HEURISTIC UTILITY
# -----------------------------------------------------------------------------
def generate_risk_explanation(features: CustomerFeatures, prob: float) -> str:
    """
    Generates a concise risk explanation based on key behavioral drivers.
    """
    if prob < 0.35:
        return "Customer profile is secure. Strong recent transactional and app engagement patterns observed."
    
    reasons = []
    # If standard inputs are greater than zero, it implies a value above the dataset mean
    if features.recency_days > 0:
        reasons.append("extended transactional silence (high purchase recency)")
    if features.last_visit_days_ago > 0:
        reasons.append("prolonged app/web digital lookback absence")
    if features.monetary_180d < 0:
        reasons.append("low relative customer spend value (monetary contribution)")
    if features.return_rate_180d > 0:
        reasons.append("elevated product return rates creating transactional friction")
        
    if not reasons:
        reasons.append("unfavorable combination of underlying platform tenure and transactional history")
        
    return f"Elevated churn risk detected due to: {', '.join(reasons)}."


# -----------------------------------------------------------------------------
# 5. REST SERVICE API ENDPOINTS
# -----------------------------------------------------------------------------
@app.get("/health", status_code=status.HTTP_200_OK, tags=["Monitoring"])
async def health_check():
    """
    Returns a service status heartbeat along with the state of the model artifact.
    """
    return {
        "status": "healthy" if model is not None else "degraded",
        "model_loaded": model is not None,
        "api_version": "1.0.0"
    }

@app.post("/predict", response_model=SingleChurnPrediction, status_code=status.HTTP_200_OK, tags=["Inference"])
async def predict_single(payload: CustomerFeatures):
    """
    Calculates churn risk for a single customer profile against an optimized threshold 
    """
    if model is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model artifact is not loaded.")
    
    try:
        # Convert incoming payload values to match the exact feature name dictionary structure
        payload_dict = payload.model_dump(by_alias=True)
        ordered_row = [payload_dict.get(feat, 0.0) for feat in FEATURE_NAMES]
        
        # Structure as a 2D array for the scikit-learn model input
        input_array = np.array([ordered_row])
        
        # Extract the probability score for the positive class (churn = 1)
        prob_score = float(model.predict_proba(input_array)[0, 1])
        
        # Implement our business-optimized decision threshold boundary
        predicted_flag = 1 if prob_score >= 0.20 else 0
        explanation = generate_risk_explanation(payload, prob_score)
        
        return SingleChurnPrediction(
            churn_probability=round(prob_score, 4),
            predicted_class=predicted_flag,
            risk_explanation=explanation
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Prediction error: {str(e)}")

@app.post("/batch_predict", response_model=BatchChurnPrediction, status_code=status.HTTP_200_OK, tags=["Inference"])
async def predict_batch(payload_list: List[CustomerFeatures]):
    """
    Processes batches of customer profiles for scheduled workflows or bulk marketing campaigns.
    """
    if model is None:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Model artifact is not loaded.")
    if not payload_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Input payload list cannot be empty.")
        
    try:
        batch_rows = []
        for p in payload_list:
            p_dict = p.model_dump(by_alias=True)
            batch_rows.append([p_dict.get(feat, 0.0) for feat in FEATURE_NAMES])
            
        # Structure as a 2D matrix
        input_matrix = np.array(batch_rows)
        
        # Batch predict all probability vectors simultaneously
        prob_scores = model.predict_proba(input_matrix)[:, 1]
        
        compiled_predictions = []
        for i, prob_score in enumerate(prob_scores):
            prob_val = float(prob_score)
            predicted_flag = 1 if prob_val >= 0.20 else 0
            explanation = generate_risk_explanation(payload_list[i], prob_val)
            
            compiled_predictions.append(
                SingleChurnPrediction(
                    churn_probability=round(prob_val, 4),
                    predicted_class=predicted_flag,
                    risk_explanation=explanation
                )
            )
            
        return BatchChurnPrediction(
            total_records_processed=len(compiled_predictions),
            predictions=compiled_predictions
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Batch prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    # Start server using uvicorn on port 8000
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
