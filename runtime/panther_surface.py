from runtime.panther_plugins import PantherPluginSystem

class PantherSurface:
    """
    Panther-OS Command Surface
    A lightweight command shell that sits above the CLI and below the orchestrator.
    """

    def __init__(self, jarvondis):
        self.jarvondis = jarvondis

    def execute(self, command: str) -> str:
        """
        Parse and execute Panther-OS commands.
        """

        lowered = command.lower().strip()

        # Help
        if lowered in ("help", "panther help"):
            return self._help()

        # Identity
        if lowered in ("identity", "panther identity"):
            return self._identity()

        # Status
        if lowered in ("status", "panther status"):
            return self._status()

        # Mode switching
        if lowered.startswith("mode ") or lowered.startswith("panther mode"):
            return self._set_mode(lowered)

        # Memory view
        if lowered in ("memory", "panther memory show"):
            return self._memory()

        # Clear screen (CLI only)
        if lowered in ("clear", "panther clear"):
            return "\033c"  # ANSI clear screen

        # Fallback: send to Jarvondis
        return self.jarvondis.respond(command)

    # -------------------------
    # Commands
    # -------------------------

    def _help(self) -> str:
        return (
            "Panther-OS Commands:\n"
            "  panther help          - Show this help menu\n"
            "  panther identity      - Show Jarvondis identity\n"
            "  panther status        - Show current guardian mode + channel\n"
            "  panther mode <type>   - Switch guardian mode (companion/guardian/observer)\n"
            "  panther memory show   - Display recent memory entries\n"
            "  panther clear         - Clear the screen\n"
        )

    def _identity(self) -> str:
        snap = self.jarvondis.snapshot_identity()
        lines = [f"{k}: {v}" for k, v in snap.items()]
        return "Jarvondis Identity Snapshot:\n" + "\n".join(lines)

    def _status(self) -> str:
        ctx = self.jarvondis.context()
        return (
            "Panther-OS Status:\n"
            f"  Guardian mode: {ctx['guardian_mode']}\n"
            f"  Channel: {ctx['channel']}\n"
            f"  Kid-safe: {ctx['kid_safe']}\n"
            f"  Environment: {ctx['environment_tag']}\n"
        )

    def _set_mode(self, lowered: str) -> str:
        parts = lowered.split()
        if len(parts) < 2:
            return "Usage: panther mode <companion|guardian|observer>"

        mode = parts[-1]
        if mode not in ("companion", "guardian", "observer"):
            return "Invalid mode. Choose: companion, guardian, observer."

        self.jarvondis.guardian_mode = mode
        return f"Guardian mode updated to: {mode}"

    def _memory(self) -> str:
        entries = self.jarvondis.memory[-10:]  # last 10 entries
        if not entries:
            return "Memory is empty."

        formatted = []
        for e in entries:
            formatted.append(
                f"{e['timestamp']} | {e['input']} -> {e['response']}"
            )

        return "Recent Memory Entries:\n" + "\n".join(formatted)
