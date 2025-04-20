from core.analyzers import AnalyzerManager
from core.verifiers import VerifierManager
from core.fuzzers import FuzzerManager
from core.ai_agents import AIAgent

class Engine:
    def __init__(self):
        self.analyzer = AnalyzerManager()
        self.verifier = VerifierManager()
        self.fuzzer   = FuzzerManager()
        self.ai_agent = AIAgent()

    def static_analyze(self, path: str, plugin: str):
        # load plugin (e.g. solidity, python, rust)
        return self.analyzer.run(path, plugin)

    def formal_verify(self, path: str, property: str):
        # ask AI to generate SMT spec, then Z3 to prove
        smt_spec = self.ai_agent.generate_spec(path, property)
        return self.verifier.verify(smt_spec)

    def fuzz_test(self, path: str, max_runs: int):
        # fuzz with hypothesis or AFL
        return self.fuzzer.run(path, max_runs)
