## Edge Cases

### 1. Handling App Updates During Collection

If the app updates during data collection, the following strategies are used:

- Monitor API response structure (schema validation)
- Detect changes in response keys (e.g., missing `searchMerchants`)
- Implement fallback logging when parsing fails

Mitigation:
- Re-run API discovery via Burp Suite
- Update parsing logic accordingly

---

### 2. Handling GPS Boundary Issues

Merchants near coordinate boundaries may not appear consistently.

Solution:
- Use multiple nearby coordinates (grid sampling)
- Slightly adjust lat/lng (e.g., ±0.001 offset)
- Merge results and remove duplicates by merchant ID

---

### 3. Retry Strategy for Failed Requests

For failed API requests:

- Retry up to 3 times
- Use exponential backoff (1s → 2s → 4s)
- Skip after max retries

Error handling:
- 400 → parameter issue (no retry)
- 403 → refresh token
- 500 → retry

This ensures robustness and minimizes data loss.