import importlib
import os
import sys

class PantherPluginSystem:
    """
    Panther-OS Plugin System
    Loads, registers, and executes modular plugins.
    """

    def __init__(self, plugin_dir="plugins"):
        self.plugin_dir = plugin_dir
        self.plugins = {}

        # Ensure plugin directory exists
        if not os.path.exists(plugin_dir):
            os.makedirs(plugin_dir)

        # Add plugin directory to Python path
        sys.path.append(plugin_dir)

        # Auto-load plugins on startup
        self._discover_plugins()

    # -------------------------
    # Discovery
    # -------------------------

    def _discover_plugins(self):
        """
        Scan the plugin directory for modules.
        """

        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py") and not filename.startswith("_"):
                plugin_name = filename[:-3]
                self._load_plugin(plugin_name)

    # -------------------------
    # Loading
    # -------------------------

    def _load_plugin(self, plugin_name: str):
        """
        Dynamically import a plugin module.
        """

        try:
            module = importlib.import_module(plugin_name)

            if hasattr(module, "PantherPlugin"):
                plugin_class = getattr(module, "PantherPlugin")
                instance = plugin_class()
                self.plugins[plugin_name] = instance
        except Exception as e:
            print(f"⚠️ Failed to load plugin '{plugin_name}': {e}")

    # -------------------------
    # Execution
    # -------------------------

    def execute(self, plugin_name: str, command: str, context: dict) -> str:
        """
        Execute a command on a loaded plugin.
        """

        plugin = self.plugins.get(plugin_name)
        if not plugin:
            return f"Plugin '{plugin_name}' not found."

        try:
            return plugin.run(command, context)
        except Exception as e:
            return f"⚠️ Plugin error: {e}"

    # -------------------------
    # Listing
    # -------------------------

    def list_plugins(self) -> str:
        if not self.plugins:
            return "No plugins loaded."

        return "Loaded Panther-OS Plugins:\n" + "\n".join(
            f"- {name}" for name in self.plugins.keys()
        )
