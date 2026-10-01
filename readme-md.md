# 🌊 ReliefLedger (Simple Flood Aid Verification Engine)

A lightweight, zero-dependency Python solution designed to address aid distribution fraud, duplicate claims, and lack of trust during post-flood disaster relief operations (inspired by the 2022 Khairpur flood crisis).

---

## 📌 Problem Statement

During major disaster responses, aid distribution often encounters critical issues:
- **Duplicate Claims ("Double Dipping"):** Families accessible by road often register across multiple NGOs under different variations of their name, while remote villages receive nothing.
- **Lost Documentation:** Floods wash away physical identity cards and household paperwork, making verification difficult.
- **Reporting Pressure:** Aid workers and local leaders face pressure to inflate figures, compromising donor trust.
- **Infrastructure Collapse:** Extreme field conditions (loss of electricity, cellular towers, and zero smartphone access) prevent reliance on complex cloud software.

---

## 💡 Solution Overview

`ReliefLedger` provides an offline-capable, lightweight verification script:
1. **Privacy-Preserving Hash Tokens:** Generates an 8-to-12 character SHA-256 token using a head-of-family identifier (NIC or temporary relief tag) and birth year—no personal identity data is stored directly.
2. **Cross-Agency De-duplication:** Ensures that once a token is logged in a distribution cycle, subsequent claims by the same token (even under a different NGO name) are rejected.
3. **Tamper-Evident Ledger:** Employs basic cryptographic block-chaining (`prev_hash`) so records cannot be rewritten or modified post-distribution.
4. **Zero Dependencies:** Runs on standard, vanilla Python without requiring network connectivity or external packages.

---

## 🛠️ System Flow

```text
[Beneficiary ID / Temp Token] + [Birth Year]
                    │
                    ▼
          [SHA-256 Tokenization]
                    │
                    ▼
          [Aid Claim Attempt]
          ┌─────────┴─────────┐
          ▼                   ▼
   [Token Exists?]     [Token New?]
          │                   │
   [❌ REJECT DUPLICATE]      [✅ APPEND TO TAMPER-PROOF LEDGER]
```

---

## 🚀 Quickstart

### Prerequisites
- Python 3.8 or higher (No third-party packages required).

### Installation & Run

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/relief-ledger.git
   cd relief-ledger
   ```

2. Run the tracking script:
   ```bash
   python relief_tracker.py
   ```

---

## 📊 Sample Output

```text
--- 1. Generating Beneficiary Tokens ---
Family A Token: a19f38c71b02
Family B Token: 82bc0e5f29c4

--- 2. Recording Relief Aid ---
[SUCCESS] Aid recorded for Token a19f38c71b02 by Red Crescent in Village B.
[SUCCESS] Aid recorded for Token 82bc0e5f29c4 by Local Relief Fund in Village C.
[REJECTED] Duplicate entry! Token a19f38c71b02 has already claimed aid.

--- 3. Verifying Ledger Integrity ---
Is ledger valid and untampered?: True
Total Valid Distributions: 2
```

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).