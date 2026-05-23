"""Realistic mock data for Amazon EC skill demos."""

LISTINGS = {
    "B0EXAMPLE01": {
        "asin": "B0EXAMPLE01",
        "title": "Water Bottle Stainless Steel 32oz Insulated",
        "bullets": [
            "Made of stainless steel material",
            "Keeps drinks cold for 24 hours",
            "32oz large capacity",
            "Comes with a lid",
            "Good for outdoor activities",
        ],
        "description": "This is a water bottle made of stainless steel. It can keep your drinks cold or hot. Good for gym, hiking, and daily use.",
        "backend_keywords": "water bottle steel insulated cold hot gym hiking outdoor sports",
        "price": 24.99,
        "category": "Sports & Outdoors",
        "marketplace": "US",
    },
    "B0EXAMPLE02": {
        "asin": "B0EXAMPLE02",
        "title": "Yoga Mat Non Slip Exercise Mat for Home Gym Workout",
        "bullets": [
            "Non-slip surface for safe practice",
            "6mm thick cushioning",
            "Lightweight and portable",
            "Easy to clean with damp cloth",
            "Includes carrying strap",
        ],
        "description": "Premium yoga mat with non-slip surface. Perfect for yoga, pilates, and floor exercises at home or gym.",
        "backend_keywords": "yoga mat exercise fitness pilates workout home gym non slip",
        "price": 29.99,
        "category": "Sports & Outdoors",
        "marketplace": "US",
    },
}

KEYWORDS = {
    "insulated water bottle": [
        {"keyword": "insulated water bottle", "volume": 135000, "competition": "high", "relevance": 0.98},
        {"keyword": "water bottle 32oz", "volume": 74000, "competition": "medium", "relevance": 0.95},
        {"keyword": "stainless steel water bottle", "volume": 110000, "competition": "high", "relevance": 0.97},
        {"keyword": "steel flask", "volume": 22000, "competition": "low", "relevance": 0.85},
        {"keyword": "vacuum insulated bottle", "volume": 31000, "competition": "medium", "relevance": 0.92},
        {"keyword": "cold water bottle 24 hours", "volume": 18000, "competition": "low", "relevance": 0.90},
        {"keyword": "gym water bottle large", "volume": 45000, "competition": "medium", "relevance": 0.82},
        {"keyword": "metal water bottle", "volume": 67000, "competition": "high", "relevance": 0.88},
        {"keyword": "BPA free water bottle", "volume": 52000, "competition": "medium", "relevance": 0.80},
        {"keyword": "leak proof water bottle", "volume": 41000, "competition": "medium", "relevance": 0.83},
        {"keyword": "thermos bottle", "volume": 28000, "competition": "high", "relevance": 0.75},
        {"keyword": "hiking water bottle", "volume": 19000, "competition": "low", "relevance": 0.87},
        {"keyword": "sports water bottle", "volume": 58000, "competition": "high", "relevance": 0.79},
        {"keyword": "double wall water bottle", "volume": 12000, "competition": "low", "relevance": 0.91},
        {"keyword": "insulated flask 32 oz", "volume": 8500, "competition": "low", "relevance": 0.94},
    ],
}

PPC_CAMPAIGNS = {
    "demo_campaign": {
        "name": "Water Bottle - Broad Match",
        "daily_budget": 50.0,
        "status": "active",
        "days_running": 30,
        "total_spend": 1247.80,
        "total_sales": 3899.01,
        "total_orders": 156,
        "impressions": 89420,
        "clicks": 2180,
        "search_terms": [
            {"term": "insulated water bottle", "impressions": 12400, "clicks": 380, "spend": 190.0, "sales": 712.50, "orders": 28},
            {"term": "water bottle 32oz", "impressions": 8900, "clicks": 290, "spend": 145.0, "sales": 524.79, "orders": 21},
            {"term": "steel flask", "impressions": 6200, "clicks": 210, "spend": 105.0, "sales": 449.82, "orders": 18},
            {"term": "water bottle for gym", "impressions": 9800, "clicks": 195, "spend": 97.5, "sales": 274.89, "orders": 11},
            {"term": "cold water bottle", "impressions": 7100, "clicks": 180, "spend": 90.0, "sales": 299.88, "orders": 12},
            {"term": "bottle stainless", "impressions": 5400, "clicks": 145, "spend": 72.5, "sales": 199.92, "orders": 8},
            {"term": "big water bottle", "impressions": 8200, "clicks": 160, "spend": 80.0, "sales": 149.94, "orders": 6},
            {"term": "thermos flask", "impressions": 4300, "clicks": 95, "spend": 47.5, "sales": 74.97, "orders": 3},
            {"term": "water container", "impressions": 6800, "clicks": 130, "spend": 65.0, "sales": 49.98, "orders": 2},
            {"term": "drink bottle kids", "impressions": 5200, "clicks": 110, "spend": 55.0, "sales": 24.99, "orders": 1},
            {"term": "cup holder bottle", "impressions": 4100, "clicks": 85, "spend": 42.5, "sales": 0.0, "orders": 0},
            {"term": "plastic jug", "impressions": 3800, "clicks": 72, "spend": 36.0, "sales": 0.0, "orders": 0},
            {"term": "water dispenser", "impressions": 3200, "clicks": 68, "spend": 34.0, "sales": 0.0, "orders": 0},
            {"term": "bottle cap replacement", "impressions": 2100, "clicks": 42, "spend": 21.0, "sales": 0.0, "orders": 0},
            {"term": "baby bottle warmer", "impressions": 1900, "clicks": 18, "spend": 9.0, "sales": 0.0, "orders": 0},
        ],
    },
}

SUPPLIERS_1688 = {
    "stainless steel bottle": [
        {
            "name": "义乌市优品不锈钢制品有限公司",
            "name_en": "Yiwu Youpin Stainless Steel Co.",
            "price_rmb": 18.5,
            "moq": 500,
            "rating": 4.8,
            "years": 8,
            "response_rate": 0.95,
            "certifications": ["ISO9001", "FDA", "LFGB"],
            "production_days": 15,
            "location": "义乌",
            "customization": True,
        },
        {
            "name": "永康市恒达杯业有限公司",
            "name_en": "Yongkang Hengda Cup Co.",
            "price_rmb": 15.2,
            "moq": 1000,
            "rating": 4.5,
            "years": 12,
            "response_rate": 0.88,
            "certifications": ["ISO9001", "FDA"],
            "production_days": 12,
            "location": "永康",
            "customization": True,
        },
        {
            "name": "广州锐捷保温制品厂",
            "name_en": "Guangzhou Ruijie Insulation Products",
            "price_rmb": 22.0,
            "moq": 200,
            "rating": 4.9,
            "years": 5,
            "response_rate": 0.97,
            "certifications": ["ISO9001", "FDA", "LFGB", "CE"],
            "production_days": 10,
            "location": "广州",
            "customization": True,
        },
        {
            "name": "金华市鑫源不锈钢杯厂",
            "name_en": "Jinhua Xinyuan Stainless Cup Factory",
            "price_rmb": 13.8,
            "moq": 2000,
            "rating": 4.2,
            "years": 15,
            "response_rate": 0.80,
            "certifications": ["ISO9001"],
            "production_days": 20,
            "location": "金华",
            "customization": False,
        },
    ],
}

SHIPPING_RATES = {
    "sea_freight_per_kg": 3.5,   # USD per kg to US (sea)
    "air_freight_per_kg": 12.0,  # USD per kg to US (air)
    "fba_fee_standard": 5.40,    # FBA fulfillment fee (standard size)
    "fba_storage_monthly": 0.83, # per cubic foot per month
    "referral_pct": 0.15,        # Amazon referral fee percentage
    "import_duty_pct": 0.065,    # US import duty on steel bottles
    "product_weight_kg": 0.45,   # per unit
    "rmb_to_usd": 0.138,         # exchange rate
}
