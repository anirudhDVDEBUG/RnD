"""Mock data for demonstrating the car-buying workflow without external APIs."""

MOCK_LISTINGS = [
    {
        "year": 2022, "make": "Honda", "model": "Civic", "trim": "EX",
        "mileage": 28400, "asking_price": 24500, "seller_type": "Dealer",
        "location": "Austin, TX", "listing_url": "https://example.com/listing/civic-ex-2022",
        "source": "CarGurus", "deal_rating": "Good Deal", "days_on_market": 18,
        "stock_number": "HCX2247",
    },
    {
        "year": 2021, "make": "Toyota", "model": "Corolla", "trim": "SE",
        "mileage": 35200, "asking_price": 21900, "seller_type": "Dealer",
        "location": "Houston, TX", "listing_url": "https://example.com/listing/corolla-se-2021",
        "source": "Autotrader", "deal_rating": "Great Deal", "days_on_market": 32,
        "stock_number": "TC9981",
    },
    {
        "year": 2022, "make": "Mazda", "model": "3", "trim": "Preferred",
        "mileage": 22100, "asking_price": 23800, "seller_type": "Dealer",
        "location": "San Antonio, TX", "listing_url": "https://example.com/listing/mazda3-pref-2022",
        "source": "Cars.com", "deal_rating": "Good Deal", "days_on_market": 11,
        "stock_number": "MZ3P0054",
    },
    {
        "year": 2020, "make": "Honda", "model": "Accord", "trim": "Sport",
        "mileage": 48300, "asking_price": 22700, "seller_type": "Private",
        "location": "Dallas, TX", "listing_url": "https://example.com/listing/accord-sport-2020",
        "source": "Facebook Marketplace", "deal_rating": "Fair Deal", "days_on_market": 7,
        "stock_number": None,
    },
    {
        "year": 2021, "make": "Hyundai", "model": "Elantra", "trim": "SEL",
        "mileage": 31800, "asking_price": 19500, "seller_type": "Dealer",
        "location": "Round Rock, TX", "listing_url": "https://example.com/listing/elantra-sel-2021",
        "source": "CarGurus", "deal_rating": "Great Deal", "days_on_market": 45,
        "stock_number": "HE2145",
    },
]

MOCK_CARFAX = {
    "vin": "2HGFE2F59NH012345",
    "vehicle": "2022 Honda Civic EX",
    "owners": 1,
    "accidents": 0,
    "title_status": "Clean",
    "service_records": 8,
    "last_service": "2025-11-15",
    "odometer_ok": True,
    "flood_damage": False,
    "frame_damage": False,
    "salvage_rebuild": False,
    "recalls_open": 0,
    "service_history": [
        {"date": "2022-03-10", "mileage": 12, "description": "New vehicle delivery inspection"},
        {"date": "2022-09-22", "mileage": 5012, "description": "Oil change, tire rotation"},
        {"date": "2023-03-15", "mileage": 10230, "description": "Oil change, cabin filter replaced"},
        {"date": "2023-09-08", "mileage": 15400, "description": "Oil change, tire rotation, brake inspection"},
        {"date": "2024-03-20", "mileage": 19800, "description": "Oil change, transmission fluid check"},
        {"date": "2024-09-11", "mileage": 23500, "description": "Oil change, tire rotation, new wiper blades"},
        {"date": "2025-03-05", "mileage": 26200, "description": "Oil change, alignment"},
        {"date": "2025-11-15", "mileage": 28400, "description": "Oil change, brake pads replaced (front)"},
    ],
}

MOCK_CARFAX_RISKY = {
    "vin": "1G1YY22G455109876",
    "vehicle": "2020 Honda Accord Sport",
    "owners": 3,
    "accidents": 1,
    "title_status": "Clean",
    "service_records": 3,
    "last_service": "2024-06-01",
    "odometer_ok": True,
    "flood_damage": False,
    "frame_damage": False,
    "salvage_rebuild": False,
    "recalls_open": 1,
    "service_history": [
        {"date": "2020-06-15", "mileage": 50, "description": "New vehicle delivery inspection"},
        {"date": "2021-12-01", "mileage": 22000, "description": "Oil change"},
        {"date": "2024-06-01", "mileage": 41000, "description": "Oil change, tire replacement"},
    ],
}

# Market value references (mock KBB/Edmunds/NADA)
MOCK_VALUATIONS = {
    "2022 Honda Civic EX": {"kbb_fair": 23200, "edmunds": 23500, "nada_clean": 24100},
    "2021 Toyota Corolla SE": {"kbb_fair": 20100, "edmunds": 20400, "nada_clean": 20800},
    "2022 Mazda 3 Preferred": {"kbb_fair": 22500, "edmunds": 22800, "nada_clean": 23400},
    "2020 Honda Accord Sport": {"kbb_fair": 21000, "edmunds": 21400, "nada_clean": 22100},
    "2021 Hyundai Elantra SEL": {"kbb_fair": 18200, "edmunds": 18500, "nada_clean": 19000},
}

BUYER_PROFILE = {
    "name": "Alex",
    "budget": 25000,
    "state": "TX",
    "preferences": "reliable sedan, under 40k miles, 2020+",
}
