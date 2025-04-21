# core/hookspecs.py

import pluggy

hookspec = pluggy.HookspecMarker("spectorin")

class SpectorinSpec:
    """Spectorin plugin specifications"""
    
    @hookspec
    def get_analyzer(self, language: str):
        """Get analyzer for a specific language"""
        
    @hookspec
    def analyze(self, code: str):
        """Analyze code and return results"""
        
    @hookspec
    def calculate_security_score(self, analysis_results: dict) -> int:
        """Calculate security score from analysis results"""
