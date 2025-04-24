# core/plugin_manager.py

import pluggy
from typing import Dict, Any, List
from core.analyzers.base_analyzer import BaseAnalyzer
from .analyzers.pyteal_analyzer import PyTealAnalyzer
from .analyzers.move_analyzer import MoveAnalyzer
from .analyzers.rust_analyzer import RustAnalyzer
from .analyzers.solidity_analyzer import SolidityAnalyzer

class PluginManager:
    """Manages analyzer plugins for different languages"""
    
    def __init__(self):
        self.pm = pluggy.PluginManager("spectorin")
        self.pm.add_hookspecs(BaseAnalyzer)
        self.analyzers = {}
        
        # Register built-in analyzers
        analyzers = [
            PyTealAnalyzer(),
            MoveAnalyzer(),
            RustAnalyzer(),
            SolidityAnalyzer()
        ]
        
        for analyzer in analyzers:
            self.register_analyzer(analyzer)
        
    def register_analyzer(self, analyzer: BaseAnalyzer):
        """Register a language-specific analyzer"""
        self.pm.register(analyzer)
        self.analyzers[analyzer.language] = analyzer
        
    def get_analyzer(self, language: str) -> BaseAnalyzer:
        """Get analyzer for specified language"""
        if language not in self.analyzers:
            raise ValueError(f"No analyzer registered for language: {language}")
        return self.analyzers[language]
        
    def analyze_code(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code using appropriate language analyzer"""
        analyzer = self.get_analyzer(language)
        return analyzer.analyze(code)
