# core/plugin_manager.py

import pluggy
from typing import Dict, Any, Optional
from core.hookspecs import SpectorinSpec

class PluginManager:
    def __init__(self):
        self.pm = pluggy.PluginManager("spectorin")
        self.pm.add_hookspecs(SpectorinSpec)
        
        # Load plugins for different languages
        self._load_plugins()
        
        # Cache for analyzers
        self._analyzers: Dict[str, Any] = {}
        
    def _load_plugins(self):
        """Load all available plugins"""
        # Register built-in plugins
        from plugins.solidity.analyzer import SolidityAnalyzer
        from plugins.pyteal.analyzer import PyTealAnalyzer
        from plugins.move.analyzer import MoveAnalyzer
        from plugins.rust.analyzer import RustAnalyzer
        
        self.pm.register(SolidityAnalyzer())
        self.pm.register(PyTealAnalyzer())
        self.pm.register(MoveAnalyzer())
        self.pm.register(RustAnalyzer())
        
    def get_analyzer(self, language: str) -> Optional[Any]:
        """Get analyzer for specific language"""
        if language not in self._analyzers:
            # Get the appropriate analyzer from plugins
            analyzers = self.pm.hook.get_analyzer(language=language)
            self._analyzers[language] = analyzers[0] if analyzers else None
            
        return self._analyzers[language]
