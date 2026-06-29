class TaskSkill:
    """
    Task execution skill for Jarvondis.
    Handles structured commands, simple task parsing, and future expansion.
    """

    def __init__(self):
        # Future: load task plugins, OS integrations, cloud actions, etc.
        pass

    def handle(self, input_str: str, context: dict) -> str:
        """
        Main task handler.
        Parses the user's request and executes a simple task.
        """

        identity = context.get("identity_id", "unknown")
        guardian_mode = context.get("guardian_mode", "companion")
        channel = context.get("channel", "default")
        kid_safe = context.get("kid_safe", True)

        # Kid-safe filter
        safe_input = self._apply_kid_safe_filter(input_str) if kid_safe else input_str

        # Parse task intent
        task_type = self._detect_task_type(safe_input)

        # Execute task
        result = self._execute_task(task_type, safe_input)

        # Format output
        return self._format_response(
            identity=identity,
            guardian_mode=guardian_mode,
            channel=channel,
            task_type=task_type,
            result=result
        )

    # -------------------------
    # Kid-safe filter
    # -------------------------

    def _apply_kid_safe_filter(self, text: str) -> str:
        replacements = {
            "damn": "darn",
            "hell": "heck",
            "shit": "shoot",
            "crap": "crud",
        }
        for bad, safe in replacements.items():
            text = text.replace(bad, safe)
        return text

    # -------------------------
    # Task detection
    # -------------------------

    def _detect_task_type(self, text: str) -> str:
        lowered = text.lower()

        if any(word in lowered for word in ["list", "show", "display"]):
            return "list"

        if any(word in lowered for word in ["create", "make", "build"]):
            return "create"

        if any(word in lowered for word in ["calculate", "compute", "math"]):
            return "calculate"

        if any(word in lowered for word in ["check", "status", "verify"]):
            return "check"

        return "general"

    # -------------------------
    # Task execution
    # -------------------------

    def _execute_task(self, task_type: str, text: str) -> str:
        """
        Placeholder execution logic.
        Later we will connect real modules, OS actions, cloud tasks, etc.
        """

        if task_type == "list":
            return "Here is your list: [placeholder items]"

        if task_type == "create":
            return f"I created a placeholder object based on: '{text}'"

        if task_type == "calculate":
            return "Calculation complete: 42 (placeholder result)"

        if task_type == "check":
            return "Status check complete: all systems nominal."

        return f"General task processed: '{text}'"

    # -------------------------
    # Response formatting
    # -------------------------

    def _format_response(self, identity, guardian_mode, channel, task_type, result):
        base = f"[{identity}|{guardian_mode}|task:{task_type}] {result}"

        if channel == "captain-log":
            base = f"📘 Captain’s Log — Task Execution:\n{base}"

        if channel == "classroom":
            base = f"🏫 Classroom Mode — Task Explanation:\n{base}"

        if channel == "kids-safe":
            base = f"🧸 Kid-Safe Task Mode:\n{base}"

        return base
