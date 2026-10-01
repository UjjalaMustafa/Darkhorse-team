# Darkhorse-team
the trust collapse after floods problm 3 (IET TechFest Hackathon))the trust collapse after floods problm 3 (IET TechFest Hackathon))
# 🌊 ReliefLedger: Verifiable Flood Aid Distribution

A lightweight, zero-dependency, tamper-evident aid distribution engine designed to prevent double-dipping, political patronage, and audit fraud during post-disaster humanitarian relief.

---

## 📌 Problem Context (Khairpur Floods Case Study)
During flood disasters, aid distribution faces severe trust and coordination challenges:
- **Duplicate Claims:** Families register under multiple names across different NGOs.
- **Geographic Bias:** Roadside settlements receive aid repeatedly, while cut-off interior villages are overlooked.
- **Metric Pressure:** NGOs face donor pressure to report high figures, incentivizing unverified reporting.
- **Lost Identification:** Displaced families lose physical documents, making verification difficult.
- **Ground Constraints:** Zero cell connectivity, frequent power outages, and limited smartphone access.

---

## 💡 Solution Overview
ReliefLedger introduces an offline-first, verifiable protocol:

1. **Privacy-Preserving Tokens:** Generates deterministic cryptographic hashes using available identifying data (CNIC, temporary shelter token, birth year) without exposing personal data.
2. **Cross-Agency Anti-Duplication:** Rejects repeated claims from the same entity across participating NGOs.
3. **Tamper-Evident Hash Chaining:** Every distribution record is linked cryptographically to prior records, preventing retrospective alterations by field workers or local gatekeepers.
4. **Offline Resilience:** Enables local batch logging that reconciles seamlessly once network connectivity resumes.

---

## ⚙️ How It Works

```text
[Beneficiary Token / QR]
          │
          ▼
   (Field Worker)
          │
          ├──► Check against Claimed Tokens
          │         │
          │         ├── [Already Claimed] ──► Distribution Rejected
          │         │
          │         └── [New Claim] ───────► Logged into Ledger
          ▼
   Cryptographic Hash Chaining (SHA-256)
          │
          ▼
   Audit-Ready Verifiable Record
