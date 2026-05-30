#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def version_key(tag: str) -> tuple[tuple[int, object], ...]:
    version = tag.removeprefix("v")
    base, _, suffix = version.partition("-")
    key: list[tuple[int, object]] = [(0, tuple(int(part) for part in re.findall(r"\d+", base)))]

    key.append((1, 1 if not suffix else 0))

    for part in re.findall(r"\d+|[A-Za-z]+", suffix):
        if part.isdigit():
            key.append((2, int(part)))
        else:
            key.append((3, part.lower()))

    return tuple(key)


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", required=True)
    parser.add_argument("--tags-json", required=True)
    parser.add_argument("--manifest-json", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    tags_payload = load_json(args.tags_json)
    manifest_payload = load_json(args.manifest_json)

    tags = [tag for tag in tags_payload.get("tags", []) if tag.startswith("v")]
    top_tags = sorted(tags, key=version_key, reverse=True)[:5]

    annotations = manifest_payload.get("annotations", {})
    component_versions = sorted(
        (
            (name.removeprefix("versions/"), version)
            for name, version in annotations.items()
            if name.startswith("versions/")
        ),
        key=lambda item: item[0],
    )

    lines = [
        f"# VertiGIS Studio Base {args.tag}",
        "",
        "## Best 5 versions",
        "",
        "| Tag | Current |",
        "| --- | --- |",
    ]

    for tag in top_tags:
        current = "Yes" if tag == args.tag else ""
        lines.append(f"| `{tag}` | {current} |")

    lines.extend(
        [
            "",
            "## Versions",
            "",
            "| Component | Version |",
            "| --- | --- |",
        ]
    )

    for component, version in component_versions:
        lines.append(f"| `{component}` | `{version}` |")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
