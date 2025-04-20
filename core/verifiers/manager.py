# core/verifiers/manager.py
from core.verifiers.z3_engine import Z3Verifier

class VerifierManager:
    def __init__(self):
        self.verifiers = {
            "z3": Z3Verifier()
        }

    def verify(self, code: str, language: str, properties: list[str]):
        # Choose correct verifier based on language or config
        verifier = self.verifiers["z3"]
        return verifier.verify(code, properties)
