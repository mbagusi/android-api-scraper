# android-api-scraper
Mobile API to extract merchant and product data using direct API replay (HTTP/2).

## 📌 Overview
This project extracts merchant and product data using direct API replay.

---

## ⚙️ Requirements & Setup

### 1. Environment
- Real Devices (Google Pixel 7 - Android 16)
- Python 3.10+
- pip3

### 2. Install Dependencies
```bash
pip3 install "httpx[http2]"
```

---

## 🔧 Configuration

Before running, update the following in `scraper.py`:

### 1. Authentication Headers (from Burp/Frida)
```python
HEADERS = {
    "User-Agent": ".../5.402.0",
    "X-Mts-Ssid": "YOUR_TOKEN_HERE",
    "Session-Id": "YOUR_SESSION_ID",
}
```

### 2. GPS Coordinates
```python
LATLNG = "-6.2017,106.6140"  # example: Karawaci
```

### 3. poiID (must match location)
```python
"poiID": "YOUR_POI_ID"
```

> ⚠️ Important:
- Token (`X-Mts-Ssid`) must be captured from live traffic
- `latlng` and `poiID` must match

---

## 🚀 How to Run

```bash
python3 scraper.py
```

---

## 🌐 Proxy Setup (Optional)

If using Burp Suite:

1. Set device proxy to Burp
2. Install Burp certificate
3. Capture request
4. Copy headers into script

---

## 📊 Output Format

The script generates:

```bash
output.json
```

### Sample:
```json
{
  "merchant_name": "Puyo Desserts",
  "address": "Tangcity Mall...",
  "coordinates": {
    "lat": -6.20,
    "lng": 106.61
  },
  "operating_hours": "10:00-22:00",
  "rating": 4.5,
  "products": [
    {
      "name": "Chocolate Dessert",
      "original_price": "Rp25.000",
      "discounted_price": "Rp20.000",
      "customization": ["Extra topping"]
    }
  ]
}
```

---

## 🧠 Notes

- Uses HTTP/2 via httpx
- Requires valid session token
- Data source:
  - Nearby API → merchant list
  - Detail API → menu & full data

---

## 👨‍💻 Author
Mochammad Bagus Insan
