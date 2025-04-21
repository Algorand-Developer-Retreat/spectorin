from typing import Dict, Any, List
from core.plugin_manager import PluginManager
from core.ai_agents.manager import AIAgentManager
import logging

logger = logging.getLogger(__name__)

class Engine:
    def __init__(self):
        self.plugin_manager = PluginManager()
        self.ai_manager = AIAgentManager()
        
    def analyze(self, code: str, language: str) -> Dict[str, Any]:
        try:
            # Get the appropriate analyzer
            analyzer = self.plugin_manager.get_analyzer(language)
            if not analyzer:
                raise ValueError(f"No analyzer available for {language}")
            
            # Perform analysis
            analysis_results = analyzer.analyze(code)
            
            # Calculate score
            score = analyzer.calculate_security_score(analysis_results)
            
            # Get AI recommendations
            recommendations = self.ai_manager.get_recommendations(code, language)
            
            return {
                'score': score,
                'issues': analysis_results.get('issues', []),
                'recommendations': recommendations,
                'summary': analysis_results.get('summary', '')
            }
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            raise

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
