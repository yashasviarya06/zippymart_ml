"""
Zippy Mart Forensic Audit Configuration.
Encapsulates extracted ground-truth parameters, SLA targets, and recovery thresholds.
"""

# High-Level Unit Economics
TOTAL_CAMPAIGN_SPEND_CR = 12.00  # ₹12.0 Cr total spend[cite: 1]
REALIZED_CONTRIBUTION_CR = 0.34  # ₹0.34 Cr contribution realized[cite: 1]
UNRECOVERED_CAPITAL_CR = 11.53  # ₹11.53 Cr capital bleed[cite: 1]
HISTORICAL_AOV = 520.0  # ₹520 realized AOV (18.75% below plan)[cite: 1]
PLANNED_AOV = 640.0
HISTORICAL_MARGIN_PCT = 3.0  # 3% margin vs 12% target[cite: 1]
TARGET_MARGIN_PCT = 12.0

# Funnel Volumes
AD_REACH_CR = 5.0  # 5.0 Cr+ ad reach[cite: 1]
SITE_VISITS_LAKH = 37.0  # 37.00 Lakh visits[cite: 1]
APP_INSTALLS_LAKH = 6.30  # 6.30 Lakh installs (157.5% of target)[cite: 1]
CHECKOUT_INITIATED_LAKH = 5.60  # 5.60 Lakh initiated checkout[cite: 1]
PAYMENT_COMPLETED_LAKH = 2.20  # 2.20 Lakh converted[cite: 1]
CART_ABANDONMENT_RATE = 60.71  # 60.71% checkout drop-off[cite: 1]

# Operational SLA Benchmarks
DELIVERY_TIME_ACTUAL = 18.0  # 18 mins (+20% vs 15 min SLA)[cite: 1]
DELIVERY_TIME_SLA = 15.0
OOS_RATE_ACTUAL = 11.0  # 11% OOS vs 2% SLA[cite: 1]
OOS_RATE_SLA = 2.0
PARTNER_AVAILABILITY_ACTUAL = 83.0  # 83% vs 95% SLA[cite: 1]
PARTNER_AVAILABILITY_SLA = 95.0
ORDER_FULFILLMENT_ACTUAL = 92.0  # 92% vs 98% SLA[cite: 1]
ORDER_FULFILLMENT_SLA = 98.0

# NPS & Retention
NPS_ACTIVE_REPEAT = 41  # NPS +41 active repeat users[cite: 1]
NPS_FIRST_TIME = 12  # NPS +12 first-time users[cite: 1]
NPS_CHURNED = -18  # NPS -18 churned cohort[cite: 1]

COHORT_RETENTION_M1 = 38.0  # 38% Month 1[cite: 1]
COHORT_RETENTION_M2 = 27.0  # 27% Month 2 (-1,100 bps)[cite: 1]
COHORT_RETENTION_M3 = 19.0  # 19% Month 3 (-800 bps, 50% drop)[cite: 1]

# Geographic Tiers
TIER_METRICS = {
    "Tier-1": {"retention": 24.0, "cac": 720.0},  # Tier-1: 24% ret, ₹720 CAC[cite: 1]
    "Tier-2": {"retention": 36.0, "cac": 510.0},  # Tier-2: 36% ret, ₹510 CAC[cite: 1]
    "Tier-3": {"retention": 42.0, "cac": 420.0},  # Tier-3: 42% ret, ₹420 CAC[cite: 1]
}

# Media Portfolio Reallocation Matrix (₹12.0 Cr flat deployment)
PORTFOLIO_MATRIX = [
    {"channel": "Google Search", "initial_cr": 1.80, "revised_cr": 2.50, "net_cr": 0.70, "cac": 430, "share": 29.0},  #[cite: 1]
    {"channel": "Dynamic Retargeting", "initial_cr": 1.20, "revised_cr": 2.00, "net_cr": 0.80, "cac": 380, "share": 22.0},  #[cite: 1]
    {"channel": "Retention, CRM & Loyalty", "initial_cr": 0.00, "revised_cr": 2.50, "net_cr": 2.50, "cac": 0, "share": 0.0},  #[cite: 1]
    {"channel": "Instagram Reels", "initial_cr": 3.20, "revised_cr": 1.80, "net_cr": -1.40, "cac": 890, "share": 18.0},  #[cite: 1]
    {"channel": "Micro-Influencers", "initial_cr": 2.40, "revised_cr": 1.20, "net_cr": -1.20, "cac": 970, "share": 11.0},  #[cite: 1]
    {"channel": "YouTube Consideration", "initial_cr": 2.00, "revised_cr": 1.20, "net_cr": -0.80, "cac": 820, "share": 14.0},  #[cite: 1]
    {"channel": "Affiliate Networks", "initial_cr": 1.40, "revised_cr": 0.80, "net_cr": -0.60, "cac": 780, "share": 6.0},  #[cite: 1]
]

# Slide 6: Governance Recovery Benchmarks
RECOVERY_TARGETS = {
    "Checkout Conversion (%)": {"actual": 39.29, "m30": 48.0, "m60": 62.0, "steady": 68.0},  #[cite: 1]
    "Blended CAC (₹)": {"actual": 760.0, "m30": 580.0, "m60": 460.0, "steady": 400.0},  #[cite: 1]
    "Month-2 Retention (%)": {"actual": 27.0, "m30": 32.0, "m60": 38.0, "steady": 45.0},  #[cite: 1]
    "Month-3 Retention (%)": {"actual": 19.0, "m30": 24.0, "m60": 30.0, "steady": 35.0},  #[cite: 1]
    "Net Contribution Margin (%)": {"actual": 3.0, "m30": 5.5, "m60": 8.5, "steady": 12.0},  #[cite: 1]
    "Average Order Value (₹)": {"actual": 520.0, "m30": 560.0, "m60": 610.0, "steady": 650.0},  #[cite: 1]
    "Dark-Store OOS Rate (%)": {"actual": 11.0, "m30": 6.0, "m60": 3.5, "steady": 2.0},  #[cite: 1]
    "Average Delivery Time (mins)": {"actual": 18.0, "m30": 16.5, "m60": 15.0, "steady": 14.0},  #[cite: 1]
    "Partner Availability (%)": {"actual": 83.0, "m30": 88.0, "m60": 94.0, "steady": 96.0},  #[cite: 1]
    "Churned Cohort NPS": {"actual": -18.0, "m30": -5.0, "m60": 15.0, "steady": 35.0},  #[cite: 1]
}