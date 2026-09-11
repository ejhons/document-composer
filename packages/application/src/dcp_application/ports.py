from __future__ import annotations

from typing import Any
from abc import ABC, abstractmethod

from dcp_engine.solving.resolution.resolution_collector import PendingResolution

class InteractionPort(ABC):
    """
    Port for obtaining values required during document execution.

    Implementations belong to the delivery layer, such as:
    - CLI / terminal
    - HTTP API
    - GUI
    """

    @abstractmethod
    def resolve(
        self,
        pending: PendingResolution,
    ) -> dict[str, Any]:
        """
        Resolve pending external values.

        Parameters
        ----------
        pending:
            Values required to continue the execution.

        Returns
        -------
        dict[str, Any]
            Values supplied by the external actor.
        """
        raise NotImplementedError