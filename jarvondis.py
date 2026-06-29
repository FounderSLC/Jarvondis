"""
Jarvondis Orchestrator – Multi-skill Companion Core
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Optional

# Models
from models.jarvondis_identity import JarvondisIdentity
from models.personality import Personality

# Runtime
from runtime.dispatcher import Dispatcher
from runtime.erebus_sync import ErebusSync

# Skills
from skills.chat.chat_skill import ChatSkill
from skills.tasks.task_skill import TaskSkill
from skills.health.health_skill import HealthSkill
from skills.system.system_skill import SystemSkill


@dataclass
class JarvondisIdentity:
    identity_id: str
    lineage_tag: str = "Space-LEAF-Jarvondis"
    model_version: str = "3.0"
    persona_tag: str = "guardian-companion"
    sovereignty_scope: str = "local-first"
    environment_tag: str = "panther-os"
    schema_version: str = "1.0"


class Jarvondis:
    def __init__(
        self,
        identity: Optional[JarvondisIdentity] = None,
        personality: Optional[Personality] = None,
        memory_file: str = "jarvondis_memory.json",
        guardian_mode: str = "companion",
        channel: str = "captain-log",
        kid_safe: bool = True,
    ):
        # Identity + persona
        self.identity = identity or JarvondisIdentity(identity_id="jarvondis-local-001")
        self.personality = personality or Personality(
            tone="witty",
            channel=channel,
            kid_safe=kid_safe,
        )

        # Modes
        self.guardian_mode = guardian_mode

        # Backend bridge
        self.erebus_sync = ErebusSync()

        # Skills + dispatcher
        self.dispatcher = Dispatcher(
            {
                "chat": ChatSkill(),
                "tasks": TaskSkill(),
                "health": HealthSkill(),
                "system": SystemSkill(),
            }
        )

        # Persistence
        self.memory_file = memory_file
        self._memory: List[Dict[str, str]] = []
        self._load_memory()
        self.update_revision: int = self._compute_revision()

    # -------------------------
    # Context
    # -------------------------

    def context(self) -> Dict[str, str]:
        return {
            "identity_id": self.identity.identity_id,
            "lineage_tag": self.identity.lineage_tag,
            "model_version": self.identity.model_version,
            "persona_tag": self.identity.persona_tag,
            "sovereignty_scope": self.identity.sovereignty_scope,
            "environment_tag": self.identity.environment_tag,
            "guardian_mode": self.guardian_mode,
            "channel": self.personality.channel,
            "kid_safe": self.personality.kid_safe,
            "schema_version": self.identity.schema_version,
        }

    # -------------------------
    # Lifecycle
    # -------------------------

    def initialize(self) -> None:
        print(
            f"🟢 Jarvondis online.\n"
            f"   Identity: {self.identity.identity_id} ({self.identity.model_version})\n"
            f"   Mode: {self.guardian_mode} | Channel: {self.personality.channel}"
        )

    # -------------------------
    # Core interaction
    # -------------------------

    def respond(self, input_str: str) -> str:
        ctx = self.context()
        output = self.dispatcher.route(input_str, ctx)
        self._log_memory(input_str, output)
        return output

    def _log_memory(self, input_str: str, response: str) -> None:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "input": input_str,
            "response": response,
            "identity_id": self.identity.identity_id,
            "lineage_tag": self.identity.lineage_tag,
            "model_version": self.identity.model_version,
            "guardian_mode": self.guardian_mode,
            "channel": self.personality.channel,
            "kid_safe": str(self.personality.kid_safe),
            "schema_version": self.identity.schema_version,
            "update_revision": str(self.update_revision),
        }
        self._memory.append(entry)

    # -------------------------
    # Updates
    # -------------------------

    def snapshot_identity(self) -> Dict[str, str]:
        snap = asdict(self.identity)
        snap["guardian_mode"] = self.guardian_mode
        snap["channel"] = self.personality.channel
        snap["kid_safe"] = self.personality.kid_safe
        snap["update_revision"] = self.update_revision
        return {k: str(v) for k, v in snap.items()}

    def apply_update(self, new_model_version: str, note: str = "") -> None:
        self.identity.model_version = new_model_version
        self.update_revision += 1
        self._memory.append(
            {
                "timestamp": datetime.now().isoformat(),
                "input": f"UPDATE_APPLIED::{note}",
                "response": f"Jarvondis updated to {new_model_version} (rev {self.update_revision})",
                "identity_id": self.identity.identity_id,
                "lineage_tag": self.identity.lineage_tag,
                "model_version": self.identity.model_version,
                "guardian_mode": self.guardian_mode,
                "channel": "system",
                "kid_safe": "True",
                "schema_version": self.identity.schema_version,
                "update_revision": str(self.update_revision),
            }
        )

    def _compute_revision(self) -> int:
        max_rev = 0
        for row in self._memory:
            try:
                r = int(row.get("update_revision", "0"))
                max_rev = max(max_rev, r)
            except ValueError:
                continue
        return max_rev + 1

    # -------------------------
    # Persistence
    # -------------------------

    def save_memory(self, filename: Optional[str] = None) -> None:
        filename = filename or self.memory_file
        tmp = tempfile.NamedTemporaryFile(
            "w",
            delete=False,
            dir=os.path.dirname(os.path.abspath(filename)) or None,
        )
        try:
            payload = {
                "schema_version": self.identity.schema_version,
                "identity_snapshot": self.snapshot_identity(),
                "entries": self._memory,
            }
            with open(tmp.name, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            os.replace(tmp.name, filename)
        finally:
            if os.path.exists(tmp.name):
                try:
                    os.remove(tmp.name)
                except Exception:
                    pass

    def _load_memory(self, filename: Optional[str] = None) -> None:
        filename = filename or self.memory_file
        if not os.path.exists(filename):
            self._memory = []
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                payload = json.load(f)
            if isinstance(payload, dict) and "entries" in payload:
                self._memory = payload.get("entries", [])
            elif isinstance(payload, list):
                self._memory = payload
            else:
                self._memory = []
        except Exception:
            self._memory = []

    @property
    def memory(self) -> List[Dict[str, str]]:
        return list(self._memory)


__all__ = ["Jarvondis"]
