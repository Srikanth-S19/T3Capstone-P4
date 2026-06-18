# Test Results and Input Data

## 1. Health Check

### Input Data

* None

### Output

![](C:/Users/homeadm/AppData/Roaming/marktext/images/2026-06-18-19-56-32-image.png)



## 2. /predict for one customer

### Input Data

3 different customers :

1. Secure Core Champion (High Value, Very Recent)

`{
        "recency_days": -0.85,           # Highly standardized recent order
        "frequency_180d": 2.10,          # Multiple orders (well above average)
        "monetary_180d": 1.95,           # Large financial spend footprint
        "sessions_30d": 1.50,            # Frequently loading the platform
        "product_views_30d": 1.20,
        "cart_adds_30d": 0.80,
        "wishlist_adds_30d": 0.50,
        "abandoned_carts_30d": 0.0,
        "last_visit_days_ago": -0.75,     # Logged in within the past few days
        "days_since_signup": 1.10,        # Mature long-standing account
        "return_rate_180d": 0.0,
        "avg_discount_pct_180d": -0.20,  # Buys full price (not discount dependent)
        "avg_rating_180d": 0.80,         # Gives good reviews
        "category_diversity_180d": 1.50, # Buys across multiple verticals
        "ticket_count_90d": 0.0,
        "negative_ticket_rate_90d": 0.0,
        "avg_resolution_hours_90d": 0.0,
        "email_opens_30d": 0.50,
        "campaign_clicks_30d": 0.20,
        "city_tier_Tier 1": 1.0,
        "loyalty_tier_Platinum": 1.0,
        "preferred_category_Skin Care": 1.0,
        "marketing_consent_Yes": 1.0
    }`

2. High-Risk Slipped Account (One-Time Buyer, Silent 3 Months)

`{
        "recency_days": 1.85,            # Severe transactional silence gap
        "frequency_180d": -0.80,         # Minimum single order threshold
        "monetary_180d": -0.65,          # Low overall cash contribution
        "sessions_30d": -0.90,           # App has not been opened in a month
        "product_views_30d": -0.85,
        "cart_adds_30d": -0.50,
        "wishlist_adds_30d": -0.40,
        "abandoned_carts_30d": 0.0,
        "last_visit_days_ago": 1.90,     # Digital silence tracks transactional silence
        "days_since_signup": -0.50,       # Relatvely fresh/un-onboarded profile
        "return_rate_180d": 0.80,        # Has returned item causing frustration
        "avg_discount_pct_180d": 1.10,   # "Discount Addicted" baseline shopper
        "avg_rating_180d": -1.20,        # Disappointed feedback star score left
        "category_diversity_180d": -0.80,
        "ticket_count_90d": 1.20,        # Support ticket filed
        "negative_ticket_rate_90d": 1.50,# Case went poorly or is unresolved
        "avg_resolution_hours_90d": 1.40,# Delayed response timeframe
        "email_opens_30d": -0.70,
        "campaign_clicks_30d": -0.50,
        "city_tier_Tier 3": 1.0,
        "loyalty_tier_None": 1.0,
        "preferred_category_Makeup": 1.0,
        "marketing_consent_Yes": 1.0
    }`

3. The Cart Abandonment Paradox (Transaction Idle, High App Intent)

` {
        "recency_days": 0.95,            # No order placed in ~60-70 days
        "frequency_180d": -0.20,         # Low historical order numbers
        "monetary_180d": -0.10,
        "sessions_30d": 1.65,            # Active app sessions logged recently
        "product_views_30d": 1.90,       # Heavy catalog browsing intensity
        "cart_adds_30d": 1.40,           # High active basket compilation
        "wishlist_adds_30d": 0.90,
        "abandoned_carts_30d": 1.80,     # Paradox element: multiple abandonments
        "last_visit_days_ago": -0.60,    # Logged in very recently
        "days_since_signup": 0.20,
        "return_rate_180d": 0.0,
        "avg_discount_pct_180d": 0.30,
        "avg_rating_180d": 0.0,
        "category_diversity_180d": 0.50,
        "city_tier_Tier 2": 1.0,
        "loyalty_tier_Silver": 1.0,
        "preferred_category_Hair Care": 1.0,
        "marketing_consent_Yes": 1.0
    }`



### Output

![](C:/Users/homeadm/AppData/Roaming/marktext/images/2026-06-18-20-20-52-image.png)



## 3. /batch_predict for 3 different batch sizes : 2, 4, 6 customers

### Input

Run program `test_api_batch.py` :

    python test_api_batch.py

### Output

![](C:/Users/homeadm/AppData/Roaming/marktext/images/2026-06-18-20-31-23-image.png)
