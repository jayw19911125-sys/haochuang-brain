#!/usr/bin/env python3
"""
audit_skills.py
掃描 /home/ubuntu/skills/ 下所有技能，提取 name / description / 檔案清單，
輸出 JSON 供後續分析或手冊更新使用。
用法：python audit_skills.py [--output <path>]
"""
import os
import json
import argparse
import re
from pathlib import Path

SKILLS_DIR = Path("/home/ubuntu/skills")

def parse_frontmatter(skill_md: str) -> dict:
    """從 SKILL.md 提取 YAML frontmatter 的 name 與 description。"""
    match = re.search(r"^---\s*\n(.*?)\n---", skill_md, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fm[key.strip()] = val.strip()
    return fm

def audit():
    results = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md_path = skill_dir / "SKILL.md"
        if not skill_md_path.exists():
            continue
        content = skill_md_path.read_text(encoding="utf-8")
        fm = parse_frontmatter(content)
        files = [str(p.relative_to(skill_dir)) for p in skill_dir.rglob("*") if p.is_file()]
        results.append({
            "name": fm.get("name", skill_dir.name),
            "description": fm.get("description", ""),
            "path": str(skill_dir),
            "files": files,
            "skill_md_lines": len(content.splitlines())
        })
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="/tmp/skills_audit.json")
    args = parser.parse_args()
    data = audit()
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 掃描完成，共 {len(data)} 個技能，結果已輸出至 {args.output}")
    for item in data:
        print(f"  - {item['name']} ({item['skill_md_lines']} 行)")
