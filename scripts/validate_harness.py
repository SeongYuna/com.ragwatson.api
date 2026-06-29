"""
validate_harness.py

하네스 엔지니어링 — 온톨로지 토폴로지 검증 스크립트

[목적]
MD 파일의 Frontmatter(type, links 필드)를 파싱하여
스타 토폴로지(Hub-and-Spoke) 규칙 위반을 탐지한다.

[검사 항목]
1. spoke → spoke 직접 링크 금지
2. hub → spoke 직접 링크 금지 (hub는 포트를 노출할 뿐, spoke를 알지 못함)
3. 고립 노드(isolated node): 아무 링크도 없는 MD 파일
4. 순환 참조(cycle): spoke A → hub → spoke B 경로가 사이클을 형성하는 경우

[Frontmatter 형식 예시]
---
type: hub          # 또는 spoke
title: Starcraft Hub
links:
  - titanic_m_learning/overview
---

[실행]
python backend/scripts/validate_harness.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml  # pip install pyyaml

ROOT = Path(__file__).resolve().parents[2]  # com.ragwatson/
BACKEND_APPS = ROOT / "backend" / "apps"
DOCS_DIRS = ["_docs"]  # 각 앱 안에서 MD를 찾을 서브디렉터리

EXIT_OK = 0
EXIT_FAIL = 1


def _parse_frontmatter(md_path: Path) -> dict:
    """YAML Frontmatter 블록을 파싱한다. 없으면 빈 dict 반환."""
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", maxsplit=2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def _collect_nodes(apps_dir: Path) -> dict[str, dict]:
    """
    apps/ 아래 모든 MD 파일을 수집하고
    {node_id: {type, links, path}} 형태로 반환한다.
    node_id = 앱 이름 (디렉터리명)
    """
    nodes: dict[str, dict] = {}
    for app_dir in apps_dir.iterdir():
        if not app_dir.is_dir() or app_dir.name.startswith("_"):
            continue
        for docs_sub in DOCS_DIRS:
            docs_path = app_dir / docs_sub
            if not docs_path.exists():
                continue
            for md_file in docs_path.glob("*.md"):
                fm = _parse_frontmatter(md_file)
                node_type = fm.get("type", "unknown")
                links = fm.get("links") or []
                # 앱 이름을 node_id로 사용 (여러 MD가 있으면 앱 단위로 병합)
                node_id = app_dir.name
                if node_id not in nodes:
                    nodes[node_id] = {"type": node_type, "links": [], "paths": []}
                nodes[node_id]["links"].extend(links)
                nodes[node_id]["paths"].append(str(md_file.relative_to(ROOT)))
                if node_type != "unknown":
                    nodes[node_id]["type"] = node_type  # 명시된 type 우선
    return nodes


def _check_spoke_to_spoke(nodes: dict[str, dict]) -> list[str]:
    """스포크 → 스포크 직접 링크 탐지."""
    errors: list[str] = []
    spokes = {k for k, v in nodes.items() if v["type"] == "spoke"}
    for node_id, meta in nodes.items():
        if meta["type"] != "spoke":
            continue
        for link in meta["links"]:
            target = link.split("/")[0]
            if target in spokes:
                errors.append(
                    f"[SPOKE→SPOKE] '{node_id}' → '{target}' 직접 참조 금지"
                )
    return errors


def _check_hub_to_spoke(nodes: dict[str, dict]) -> list[str]:
    """허브 → 스포크 내부 직접 링크 탐지."""
    errors: list[str] = []
    spokes = {k for k, v in nodes.items() if v["type"] == "spoke"}
    for node_id, meta in nodes.items():
        if meta["type"] != "hub":
            continue
        for link in meta["links"]:
            target = link.split("/")[0]
            if target in spokes:
                errors.append(
                    f"[HUB→SPOKE] 허브 '{node_id}'가 스포크 '{target}'을 직접 참조 — "
                    f"허브는 포트(인터페이스)만 노출해야 함"
                )
    return errors


def _check_isolated(nodes: dict[str, dict]) -> list[str]:
    """아무 링크도 없는 고립 노드 탐지."""
    warnings: list[str] = []
    for node_id, meta in nodes.items():
        if not meta["links"]:
            warnings.append(
                f"[ISOLATED] '{node_id}' (type={meta['type']}) — 연결된 링크 없음"
            )
    return warnings


def _check_cycles(nodes: dict[str, dict]) -> list[str]:
    """DFS로 순환 참조 탐지."""
    errors: list[str] = []
    adj: dict[str, set[str]] = {
        k: {lnk.split("/")[0] for lnk in v["links"] if lnk.split("/")[0] in nodes}
        for k, v in nodes.items()
    }
    visited: set[str] = set()
    stack: set[str] = set()

    def dfs(node: str, path: list[str]) -> None:
        visited.add(node)
        stack.add(node)
        for neighbor in adj.get(node, set()):
            if neighbor not in visited:
                dfs(neighbor, path + [neighbor])
            elif neighbor in stack:
                cycle_start = path.index(neighbor) if neighbor in path else 0
                cycle = " → ".join(path[cycle_start:] + [neighbor])
                errors.append(f"[CYCLE] 순환 참조 탐지: {cycle}")
        stack.discard(node)

    for node_id in nodes:
        if node_id not in visited:
            dfs(node_id, [node_id])

    return errors


def main() -> int:
    print(f"[Harness Validator] 스캔 경로: {BACKEND_APPS}")
    nodes = _collect_nodes(BACKEND_APPS)

    if not nodes:
        print("경고: MD 파일에서 Frontmatter(type 필드)를 가진 노드를 찾지 못했습니다.")
        print("  → _docs/*.md 파일에 ---\\ntype: hub|spoke\\n--- 형식의 Frontmatter를 추가하세요.")
        return EXIT_OK

    print(f"  발견된 노드: {list(nodes.keys())}\n")

    all_errors: list[str] = []
    all_warnings: list[str] = []

    all_errors.extend(_check_spoke_to_spoke(nodes))
    all_errors.extend(_check_hub_to_spoke(nodes))
    all_errors.extend(_check_cycles(nodes))
    all_warnings.extend(_check_isolated(nodes))

    for w in all_warnings:
        print(f"  WARN  {w}")

    if all_errors:
        print()
        for e in all_errors:
            print(f"  ERROR {e}")
        print(f"\n[FAIL] 하네스 검증 실패 — {len(all_errors)}개 위반 발견")
        return EXIT_FAIL

    print(f"[OK] 하네스 검증 통과 — 토폴로지 무결성 확인됨 (경고 {len(all_warnings)}개)")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
