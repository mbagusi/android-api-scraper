import httpx
import json

BASE = "https://p.grabtaxi.com"

URL = f"{BASE}/api/passenger/v3/grabfood/nearby"

params = {
    "latlng": "-6.2017,106.6140",
    "categoryShortcutID": "229",
    "searchID": "",
    "offset": "0",
    "pageSize": "20",
    "requireSortAndFilters": "true",
    "dryrunSortAndFilters": "false",
    "filtersApplied": "false",
    "poiID": "YOUR_POI_ID",
    "keyword": "",
    "searchMetadata": "",
    "sourceType": ""
}

headers = {
    "User-Agent": ".../5.402.0 (Android 16)",
    "X-Mts-Ssid": "YOUR_TOKEN_HERE",
    "Session-Id": "YOUR_SESSION_ID",
    "Accept": "application/json",
    "Accept-Language": "en-US",
    "X-Device-Timezone": "Asia/Jakarta"
}

results = []

with httpx.Client(http2=True, headers=headers, timeout=20) as client:

    print("REQUEST NEARBY")

    res = client.get(URL, params=params)

    print("STATUS:", res.status_code)

    data = res.json()

    merchants = data.get("searchResult", {}).get("searchMerchants", [])

    print(f"✅ FOUND {len(merchants)} MERCHANTS")

    for m in merchants[:25]:

        mid = m.get("id")

        name = m.get("address", {}).get("name")

        print("👉", name, "| ID:", mid)

        detail_url = f"{BASE}/api/passenger/v4/grabfood/merchants/{mid}"

        detail_res = client.get(detail_url, params={
            "latlng": "-6.2017,106.6140",
            "deliverBy": "GRAB"
        })

        if detail_res.status_code != 200:
            continue

        try:
            detail = detail_res.json()
        except:
            continue

        merchant = detail.get("merchant", {})

        item = {
            "merchant_name": merchant.get("name"),
            "address": merchant.get("address", {}).get("combinedAddress"),
            "coordinates": merchant.get("latlng"),
            "operating_hours": merchant.get("openingHours", {}).get("displayedHours"),
            "rating": merchant.get("rating"),
            "products": []
        }

        for cat in merchant.get("menu", {}).get("categories", []):
            for p in cat.get("items", []):

                prod = {
                    "name": p.get("name"),
                    "original_price": p.get("priceV2", {}).get("amountDisplay"),
                    "discounted_price": p.get("discountedPriceV2", {}).get("amountDisplay"),
                    "customization": [
                        mod.get("name") for mod in p.get("modifierGroups", [])
                    ]
                }

                item["products"].append(prod)

        results.append(item)


with open("output.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"\n🎉 DONE — {len(results)} merchants saved to output.json")
