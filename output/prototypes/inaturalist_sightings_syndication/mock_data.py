"""Sample iNaturalist observation data for demo purposes."""

MOCK_OBSERVATIONS = [
    {
        "id": 100001,
        "observed_on": "2026-04-28",
        "time_observed_at": "2026-04-28T08:15:00-07:00",
        "uri": "https://www.inaturalist.org/observations/100001",
        "place_guess": "Golden Gate Park, San Francisco, CA",
        "license_code": "cc-by-nc",
        "taxon": {
            "name": "Ardea herodias",
            "preferred_common_name": "Great Blue Heron",
        },
        "photos": [
            {"url": "https://inaturalist-open-data.s3.amazonaws.com/photos/1/square.jpg"}
        ],
    },
    {
        "id": 100002,
        "observed_on": "2026-04-28",
        "time_observed_at": "2026-04-28T08:22:00-07:00",
        "uri": "https://www.inaturalist.org/observations/100002",
        "place_guess": "Golden Gate Park, San Francisco, CA",
        "license_code": "cc-by-nc",
        "taxon": {
            "name": "Butorides virescens",
            "preferred_common_name": "Green Heron",
        },
        "photos": [
            {"url": "https://inaturalist-open-data.s3.amazonaws.com/photos/2/square.jpg"}
        ],
    },
    {
        "id": 100003,
        "observed_on": "2026-04-28",
        "time_observed_at": "2026-04-28T09:05:00-07:00",
        "uri": "https://www.inaturalist.org/observations/100003",
        "place_guess": "Golden Gate Park, San Francisco, CA",
        "license_code": "cc-by",
        "taxon": {
            "name": "Calypte anna",
            "preferred_common_name": "Anna's Hummingbird",
        },
        "photos": [
            {"url": "https://inaturalist-open-data.s3.amazonaws.com/photos/3/square.jpg"}
        ],
    },
    {
        "id": 100004,
        "observed_on": "2026-04-25",
        "time_observed_at": "2026-04-25T07:30:00-07:00",
        "uri": "https://www.inaturalist.org/observations/100004",
        "place_guess": "Muir Woods, Mill Valley, CA",
        "license_code": "cc-by-nc",
        "taxon": {
            "name": "Strix occidentalis",
            "preferred_common_name": "Spotted Owl",
        },
        "photos": [
            {"url": "https://inaturalist-open-data.s3.amazonaws.com/photos/4/square.jpg"}
        ],
    },
    {
        "id": 100005,
        "observed_on": "2026-04-25",
        "time_observed_at": "2026-04-25T07:45:00-07:00",
        "uri": "https://www.inaturalist.org/observations/100005",
        "place_guess": "Muir Woods, Mill Valley, CA",
        "license_code": "cc-by",
        "taxon": {
            "name": "Odocoileus hemionus",
            "preferred_common_name": "Mule Deer",
        },
        "photos": [
            {"url": "https://inaturalist-open-data.s3.amazonaws.com/photos/5/square.jpg"}
        ],
    },
    {
        "id": 100006,
        "observed_on": "2026-04-22",
        "time_observed_at": "2026-04-22T16:00:00-07:00",
        "uri": "https://www.inaturalist.org/observations/100006",
        "place_guess": "Point Reyes, CA",
        "license_code": "cc-by-nc",
        "taxon": {
            "name": "Mirounga angustirostris",
            "preferred_common_name": "Northern Elephant Seal",
        },
        "photos": [
            {"url": "https://inaturalist-open-data.s3.amazonaws.com/photos/6/square.jpg"}
        ],
    },
    {
        "id": 100007,
        "observed_on": "2026-04-22",
        "time_observed_at": "2026-04-22T16:20:00-07:00",
        "uri": "https://www.inaturalist.org/observations/100007",
        "place_guess": "Point Reyes, CA",
        "license_code": "cc-by",
        "taxon": {
            "name": "Pelecanus occidentalis",
            "preferred_common_name": "Brown Pelican",
        },
        "photos": [
            {"url": "https://inaturalist-open-data.s3.amazonaws.com/photos/7/square.jpg"}
        ],
    },
    {
        "id": 100008,
        "observed_on": "2026-04-22",
        "time_observed_at": "2026-04-22T16:35:00-07:00",
        "uri": "https://www.inaturalist.org/observations/100008",
        "place_guess": "Point Reyes, CA",
        "license_code": "cc-by-nc",
        "taxon": {
            "name": "Haematopus bachmani",
            "preferred_common_name": "Black Oystercatcher",
        },
        "photos": [
            {"url": "https://inaturalist-open-data.s3.amazonaws.com/photos/8/square.jpg"}
        ],
    },
    {
        "id": 100009,
        "observed_on": "2026-04-20",
        "time_observed_at": "2026-04-20T10:00:00-07:00",
        "uri": "https://www.inaturalist.org/observations/100009",
        "place_guess": "Tilden Park, Berkeley, CA",
        "license_code": "cc-by",
        "taxon": {
            "name": "Lynx rufus",
            "preferred_common_name": "Bobcat",
        },
        "photos": [
            {"url": "https://inaturalist-open-data.s3.amazonaws.com/photos/9/square.jpg"}
        ],
    },
    {
        "id": 100010,
        "observed_on": "2026-04-18",
        "time_observed_at": "2026-04-18T14:10:00-07:00",
        "uri": "https://www.inaturalist.org/observations/100010",
        "place_guess": "Lake Merritt, Oakland, CA",
        "license_code": "cc-by-nc",
        "taxon": {
            "name": "Aechmophorus occidentalis",
            "preferred_common_name": "Western Grebe",
        },
        "photos": [
            {"url": "https://inaturalist-open-data.s3.amazonaws.com/photos/10/square.jpg"}
        ],
    },
    {
        "id": 100011,
        "observed_on": "2026-04-18",
        "time_observed_at": "2026-04-18T14:25:00-07:00",
        "uri": "https://www.inaturalist.org/observations/100011",
        "place_guess": "Lake Merritt, Oakland, CA",
        "license_code": "cc-by",
        "taxon": {
            "name": "Phalacrocorax auritus",
            "preferred_common_name": "Double-crested Cormorant",
        },
        "photos": [
            {"url": "https://inaturalist-open-data.s3.amazonaws.com/photos/11/square.jpg"}
        ],
    },
    {
        "id": 100012,
        "observed_on": "2026-04-15",
        "time_observed_at": "2026-04-15T06:45:00-07:00",
        "uri": "https://www.inaturalist.org/observations/100012",
        "place_guess": "Marin Headlands, CA",
        "license_code": "cc-by-nc",
        "taxon": {
            "name": "Aquila chrysaetos",
            "preferred_common_name": "Golden Eagle",
        },
        "photos": [
            {"url": "https://inaturalist-open-data.s3.amazonaws.com/photos/12/square.jpg"}
        ],
    },
]
