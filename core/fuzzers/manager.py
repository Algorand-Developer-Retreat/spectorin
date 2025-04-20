# core/fuzzers/manager.py
from core.fuzzers.hypothesis_engine import HypothesisFuzzer

class FuzzerManager:
    def __init__(self):
        self.fuzzer = HypothesisFuzzer()

    def fuzz(self, code: str, function_name: str, max_runs: int = 1000):
        return self.fuzzer.fuzz_function(code, function_name, max_runs)
