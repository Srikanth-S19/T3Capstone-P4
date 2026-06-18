import requests
import json

# Define local or container target endpoint address URL
BASE_URL = "http://127.0.0.1:8000"
BATCH_PREDICT_URL = f"{BASE_URL}/batch_predict"

# -----------------------------------------------------------------------------
# DEFINE MODULAR MOCK CUSTOMER TEMPLATES (Standardized Features Space)
# -----------------------------------------------------------------------------
secure_champion = {
    "recency_days": -0.85, "frequency_180d": 2.10, "monetary_180d": 1.95,
    "sessions_30d": 1.50, "product_views_30d": 1.20, "cart_adds_30d": 0.80,
    "wishlist_adds_30d": 0.50, "abandoned_carts_30d": 0.0, "last_visit_days_ago": -0.75,
    "days_since_signup": 1.10, "return_rate_180d": 0.0, "avg_discount_pct_180d": -0.20,
    "avg_rating_180d": 0.80, "category_diversity_180d": 1.50, "ticket_count_90d": 0.0,
    "negative_ticket_rate_90d": 0.0, "avg_resolution_hours_90d": 0.0, "email_opens_30d": 0.50,
    "campaign_clicks_30d": 0.20, "city_tier_Tier 1": 1.0, "loyalty_tier_Platinum": 1.0,
    "preferred_category_Skin Care": 1.0, "marketing_consent_Yes": 1.0
}

high_risk_slipped = {
    "recency_days": 1.85, "frequency_180d": -0.80, "monetary_180d": -0.65,
    "sessions_30d": -0.90, "product_views_30d": -0.85, "cart_adds_30d": -0.50,
    "wishlist_adds_30d": -0.40, "abandoned_carts_30d": 0.0, "last_visit_days_ago": 1.90,
    "days_since_signup": -0.50, "return_rate_180d": 0.80, "avg_discount_pct_180d": 1.10,
    "avg_rating_180d": -1.20, "category_diversity_180d": -0.80, "ticket_count_90d": 1.20,
    "negative_ticket_rate_90d": 1.50, "avg_resolution_hours_90d": 1.40, "email_opens_30d": -0.70,
    "campaign_clicks_30d": -0.50, "city_tier_Tier 3": 1.0, "loyalty_tier_None": 1.0,
    "preferred_category_Makeup": 1.0, "marketing_consent_Yes": 1.0
}

abandonment_paradox = {
    "recency_days": 0.95, "frequency_180d": -0.20, "monetary_180d": -0.10,
    "sessions_30d": 1.65, "product_views_30d": 1.90, "cart_adds_30d": 1.40,
    "wishlist_adds_30d": 0.90, "abandoned_carts_30d": 1.80, "last_visit_days_ago": -0.60,
    "days_since_signup": 0.20, "return_rate_180d": 0.0, "avg_discount_pct_180d": 0.30,
    "avg_rating_180d": 0.0, "category_diversity_180d": 0.50, "city_tier_Tier 2": 1.0,
    "loyalty_tier_Silver": 1.0, "preferred_category_Hair Care": 1.0, "marketing_consent_Yes": 1.0
}

# -----------------------------------------------------------------------------
# COMPILE BATCH TEST SUITES WITH 2, 4, AND 6 RECORDS
# -----------------------------------------------------------------------------
batches_to_test = {
    "Batch A (2 Customer Records)": [
        secure_champion, 
        high_risk_slipped
    ],
    
    "Batch B (4 Customer Records)": [
        secure_champion, 
        abandonment_paradox, 
        high_risk_slipped, 
        secure_champion
    ],
    
    "Batch C (6 Customer Records)": [
        high_risk_slipped, 
        high_risk_slipped, 
        abandonment_paradox, 
        secure_champion, 
        abandonment_paradox, 
        secure_champion
    ]
}

# -----------------------------------------------------------------------------
# EXECUTE EVALUATION RUNNER
# -----------------------------------------------------------------------------
def run_batch_inference_tests():
    print("================================================================")
    print("INITIALIZING INFRASTRUCTURE VERIFICATION")
    print("================================================================")
    
    # Verify app is alive via the monitoring endpoint
    try:
        health_check = requests.get(f"{BASE_URL}/health")
        if health_check.status_code == 200:
            print(f"FastAPI Server Status: ONLINE | Heartbeat: {health_check.json()}\n")
        else:
            print(f"Aborting Core Tests: Server responded with unhealthy code {health_check.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print(f"Critical Error: Connection refused at {BASE_URL}.")
        print("Please ensure your local FastAPI server script or Docker container is active.")
        return

    print("================================================================")
    print("STARTING POST EXECUTION STEPS FOR /BATCH_PREDICT")
    print("================================================================")

    # Process batches sequentially
    for name, payload in batches_to_test.items():
        record_count = len(payload)
        print(f"Dispatching Vector Array -> {name} [Payload Size: {record_count}]")
        
        # Execute POST request containing the list of validated features
        response = requests.post(
            BATCH_PREDICT_URL,
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        
        # Parse matrix outcomes
        if response.status_code == 200:
            result = response.json()
            print(f"  [Response Success - Status 200]")
            print(f"    -> Total Records Processed by API Model Layer: {result['total_records_processed']}")
            
            # Print a concise breakdown of the processed records
            for idx, pred in enumerate(result['predictions']):
                print(f"       * Record [{idx + 1}/{record_count}] -> Prob: {pred['churn_probability']} | Class: {pred['predicted_class']} | Reason: {pred['risk_explanation']}")
        else:
            print(f"  [Response Error - Status {response.status_code}]")
            print(f"    Details: {response.text}")
            
        print("-" * 64)
        
    print("\nBatch prediction test execution suite concluded.")

if __name__ == "__main__":
    run_batch_inference_tests()
