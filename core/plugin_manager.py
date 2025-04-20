# core/plugin_manager.py

import pluggy
from core.hookspecs import HookSpecs

def get_plugin_manager():
    pm = pluggy.PluginManager("spectorin")
    pm.add_hookspecs(HookSpecs)

    # Load built-in plugins
    from plugins.default_plugin import DefaultPlugin
    pm.register(DefaultPlugin())

    # 🔍 Optional: Discover other installed plugins via setuptools entrypoints
    # pm.load_setuptools_entrypoints("spectorin")

    return pm
