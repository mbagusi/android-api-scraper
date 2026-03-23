# Reverse Engineering Report

## 📌 Overview

This document describes the reverse engineering process used to extract the app data via direct API calls.

The approach focuses on analyzing the mobile application, bypassing protections, and replaying internal APIs.

---

## 🧰 Tooling

The following tools were used:

- **Frida** → Dynamic instrumentation and SSL pinning bypass  
- **Burp Suite** → Intercepting and analyzing HTTPS traffic  
- **ADB** → Device interaction and debugging  

---

## 🔐 Protection Analysis

### SSL Pinning

The application implements SSL pinning using **OkHttp / Conscrypt**.

#### Bypass Method:
- Hooked TrustManager implementation
- Hooked OkHttp CertificatePinner using Frida
- Used universal SSL unpinning script

### How to Bypassed SSL Pinning :
- Using rooted devices like KernelSU, Magisk or anything else
- Install ZygiskNext and LSPosed into KernelSU for bypass root detection
- Install Hide My Applist application into devices
- Configure enabled HMA on LSPosed and enabled system framework
- Configure app target (for bypass root detection) enable hide, emable work mode, and exclude system apps on HMA App Settings
- Running frida-server
- Open app target
- Attach frida in the midle app using command "frida -U -N com.app.target"
- After attach frida, copy script Frida-Multiple-Unpinning, You Can get script in a link https://codeshare.frida.re/@akabe1/frida-multiple-unpinning/
- After that, SSL Pinning can be bypass.
- For the intercept API using Burp Suite, setting proxy on rooted device, setting for IP and Proxy which use on MacOS
- After setting IP and Proxy, install CA certificate with open google chrome and visit http://burp so that show burp suite page and download certificate, after download, install certificate to rooted devices.
- After successfully install CA certificate, on Burp Suite enable Intercept On button.
- Open app target, and API app target can be intercept on Burp Suite.
- Forward all http request, and see API request and response what is needed.

#### Result:
- Successfully bypass root detection
- Successfully intercepted HTTPS traffic via Burp Suite
- Able to inspect all API requests and responses

---

## 🔑 Request Signing / Anti-Bot Mechanism

No traditional request-signing mechanism (e.g., HMAC, X-G-Signature) was found.

Instead, the API relies on:

- **X-Mts-Ssid** → Session authentication token  
- **Session-Id** → Request session identifier  
- **latlng + poiID** → Location context validation  

#### Key Insight:
The backend validates requests based on **session + device context**, not cryptographic signatures.

---

## ⚙️ Execution Strategy

- Frida was used only for:
  - SSL pinning bypass
  - Traffic interception

- No Frida-RPC or runtime request generation was used

- All API requests were replayed using **pure Python (httpx with HTTP/2)**

---

## 📊 Data Extraction Flow

```
The Application
   ↓
Frida (SSL bypass)
   ↓
Burp Suite (capture API)
   ↓
Python script (API replay)
   ↓
Structured JSON output
```

---

## 🚀 Collection Method Justification

### Chosen Method: Direct API Extraction

#### Advantages:
- Faster than UI automation
- More reliable (not affected by UI changes)
- Easier to scale
- Cleaner structured data

#### Comparison:

| Method | Result |
|------|--------|
| UI Automation | Slow, unstable |
| Hybrid (UI + API) | Medium |
| Direct API | Fast, scalable, reliable |

---

## 📈 Scalability

The solution can be extended by:

- Adding pagination support (100+ merchants)
- Running multi-location scraping
- Parallelizing requests
- Automating token refresh

---

## 🏁 Conclusion

This project demonstrates a practical mobile reverse engineering workflow:

- Bypassing application protections  
- Discovering internal APIs  
- Replaying authenticated requests  
- Extracting structured data at scale  
