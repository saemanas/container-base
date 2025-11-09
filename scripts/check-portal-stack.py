"""Guard script ensuring portal stack matches mandated Next.js and React versions."""
from __future__ import annotations

import json
import pathlib
import sys

EXPECTED_VERSIONS = {
    "next": "16",
    "react": "19",
    "react-dom": "19",
}

PORTAL_PACKAGE_JSON = pathlib.Path(__file__).resolve().parents[1] / "src/apps/portal/package.json"


def _load_package_json() -> dict[str, object]:
    if not PORTAL_PACKAGE_JSON.exists():
        print(f"::error ::package.json not found at {PORTAL_PACKAGE_JSON}")
        sys.exit(1)
    with PORTAL_PACKAGE_JSON.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _extract_version(raw_version: str) -> str:
    strip_chars = "^~>=< "
    version = raw_version
    for char in strip_chars:
        version = version.replace(char, "")
    return version


def main() -> None:
    package_json = _load_package_json()
    deps = package_json.get("dependencies", {})
    dev_deps = package_json.get("devDependencies", {})
    if not isinstance(deps, dict) or not isinstance(dev_deps, dict):
        print("::error ::Invalid dependencies block in portal package.json")
        sys.exit(1)

    resolved_versions: dict[str, str] = {}
    for dep in EXPECTED_VERSIONS:
        raw = deps.get(dep) or dev_deps.get(dep)
        if not isinstance(raw, str):
            print(f"::error ::Missing required dependency '{dep}' in portal stack")
            sys.exit(1)
        resolved_versions[dep] = _extract_version(raw)

    errors: list[str] = []
    for dep, expected_major in EXPECTED_VERSIONS.items():
        actual = resolved_versions[dep]
        actual_major = actual.split(".")[0]
        if actual_major != expected_major:
            errors.append(
                f"Dependency '{dep}' must be major {expected_major}.x but found {actual}"
            )

    if errors:
        for line in errors:
            print(f"::error ::{line}")
        sys.exit(1)

    print(
        "Portal stack versions verified: "
        + ", ".join(f"{dep} {resolved_versions[dep]}" for dep in EXPECTED_VERSIONS)
    )


if __name__ == "__main__":
    main()
