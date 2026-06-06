from __future__ import annotations

from typing import Protocol, TypeVar, runtime_checkable


InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


@runtime_checkable
class Agent(Protocol[InputT, OutputT]):
    def run(self, input_data: InputT) -> OutputT:
        ...
