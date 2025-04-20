import importlib

class AnalyzerManager:
    def __init__(self):
        self.plugins = {}

    def run(self, path: str, plugin: str):
        if plugin not in self.plugins:
            module = importlib.import_module(f"plugins.{plugin}.analyzer")
            self.plugins[plugin] = module.Analyzer()
        return self.plugins[plugin].analyze(path)
