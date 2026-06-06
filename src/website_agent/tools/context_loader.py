from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


DEFAULT_CONTEXT_DIR = Path(__file__).resolve().parent.parent / "context"
TEXT_EXTENSIONS = {".txt", ".md", ".markdown", ".json", ".yaml", ".yml", ".csv", ".rst"}


@dataclass(frozen=True)
class ContextFile:
    path: Path
    relative_path: str
    content: str


@dataclass(frozen=True)
class BusinessContextBundle:
    root: Path
    files: tuple[ContextFile, ...]

    def to_prompt_text(self) -> str:
        parts: list[str] = []
        for context_file in self.files:
            parts.append(f"FILE: {context_file.relative_path}\n{context_file.content.strip()}")
        return "\n\n---\n\n".join(parts).strip()


def load_business_context_bundle(context_dir: Path | str = DEFAULT_CONTEXT_DIR) -> BusinessContextBundle:
    root = Path(context_dir)
    if not root.exists():
        raise FileNotFoundError(f"Context directory does not exist: {root}")
    if not root.is_dir():
        raise NotADirectoryError(f"Context path is not a directory: {root}")

    context_files: list[ContextFile] = []
    for file_path in sorted(root.rglob("*")):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        relative_path = file_path.relative_to(root).as_posix()
        content = file_path.read_text(encoding="utf-8")
        context_files.append(
            ContextFile(
                path=file_path,
                relative_path=relative_path,
                content=content,
            )
        )

    if not context_files:
        raise FileNotFoundError(f"No readable context files found in: {root}")

    return BusinessContextBundle(root=root, files=tuple(context_files))
