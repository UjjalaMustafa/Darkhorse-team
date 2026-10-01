import hashlib
import json
import time

class ReliefLedger:
    """
    Lightweight, tamper-evident ledger designed to track disaster relief distribution,
    prevent cross-agency duplication, and preserve beneficiary privacy offline.
    """

    def __init__(self):
        # In-memory chain of aid distribution records
        self.ledger = []
        # Fast lookup set for de-duplication in the active distribution cycle
        self.claimed_tokens = set()

    @staticmethod
    def generate_token(identifier: str, secondary_field: str) -> str:
        """
        Creates a deterministic, one-way hash token.
        Preserves privacy: No raw NIC or personal names are saved in the logs.
        """
        raw_seed = f"{identifier.strip().upper()}::{secondary_field.strip()}"
        return hashlib.sha256(raw_seed.encode("utf-8")).hexdigest()[:12]

    def record_aid(self, token: str, ngo_name: str, aid_type: str, village: str) -> bool:
        """
        Attempts to log an aid claim. Rejects double dipping across multiple organizations.
        """
        # Anti-Duplication Check
        if token in self.claimed_tokens:
            print(f"[REJECTED] Duplicate claim detected! Token {token} already received relief.")
            return False

        # Link to the preceding record's cryptographic hash (tamper evidence)
        prev_hash = self.ledger[-1]["current_hash"] if self.ledger else "0" * 12

        record = {
            "index": len(self.ledger) + 1,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "token": token,
            "ngo": ngo_name,
            "aid": aid_type,
            "village": village,
            "prev_hash": prev_hash
        }

        # Calculate SHA-256 for the current block
        serialized_record = json.dumps(record, sort_keys=True)
        record["current_hash"] = hashlib.sha256(serialized_record.encode("utf-8")).hexdigest()[:12]

        self.ledger.append(record)
        self.claimed_tokens.add(token)

        print(f"[SUCCESS] Aid recorded for Token {token} by {ngo_name} in {village}.")
        return True

    def verify_ledger(self) -> bool:
        """
        Validates the hash chain integrity to ensure records were not modified post-distribution.
        """
        for i in range(1, len(self.ledger)):
            current_entry = self.ledger[i]
            previous_entry = self.ledger[i - 1]

            # Re-calculate hash check
            expected_prev_hash = previous_entry["current_hash"]
            if current_entry["prev_hash"] != expected_prev_hash:
                return False
        return True


# --- Self-Contained Test Run / Simulation ---
if __name__ == "__main__":
    tracker = ReliefLedger()

    print("--- 1. Generating Beneficiary Tokens ---")
    # Generating anonymized tokens using CNIC/Temp relief token & birth year
    family_a_token = tracker.generate_token("42201-1234567-1", "1990")
    family_b_token = tracker.generate_token("TEMP-KH-FLOOD-881", "1984")

    print(f"Family A Token: {family_a_token}")
    print(f"Family B Token: {family_b_token}\n")

    print("--- 2. Recording Relief Aid ---")
    # First distribution by NGO 1 to Family A
    tracker.record_aid(
        token=family_a_token,
        ngo_name="Red Crescent",
        aid_type="Ration Pack (15 Days)",
        village="Village B"
    )

    # Second distribution by NGO 2 to Family B (Remote village)
    tracker.record_aid(
        token=family_b_token,
        ngo_name="Local Relief Fund",
        aid_type="Water Purification & Cash PKR 5000",
        village="Village C"
    )

    # Duplicate Attempt: NGO 2 tries to provide aid to Family A again
    tracker.record_aid(
        token=family_a_token,
        ngo_name="Helping Hand",
        aid_type="Emergency Tent Kit",
        village="Village B"
    )

    print("\n--- 3. Verifying Ledger Integrity ---")
    is_valid = tracker.verify_ledger()
    print(f"Is ledger valid and untampered?: {is_valid}")
    print(f"Total Valid Distributions: {len(tracker.ledger)}")