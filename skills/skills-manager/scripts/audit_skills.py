#!/usr/bin/env python3
"""
audit_skills.py
掃描指定的 skills 目錄，提取 name / description / 檔案清單，
輸出 JSON 供後續分析或手冊更新使用。
預設自動偵測：優先使用本檔所在 repo 的 skills 目錄，
若偵測不到則回退至 ~/skills；亦可以 --skills-dir 手動指定。
用法：python audit_skills.py [--skills-dir <dir>] [--output <path>]
"""
import os
import json
import argparse
import re
from pathlib import Path

def default_skills_dir() -> Path:
    """自動偵測 skills 目錄：優先本檔所在 repo，否則回退 ~/skills。"""
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "skills"
        if candidate.is_dir():
            return candidate
        # 本檔本身即位於 skills/ 下的子目錄（如 skills-manager/scripts）
        if parent.name == "skills":
            return parent
    return Path.home() / "skills"

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

def audit(skills_dir: Path):
    results = []
    for skill_dir in sorted(skills_dir.iterdir()):
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
    parser.add_argument("--skills-dir", default=None,
                        help="要掃描的 skills 目錄；預設自動偵測 repo 內的 skills/。")
    parser.add_argument("--output", default="/tmp/skills_audit.json")
    args = parser.parse_args()
    skills_dir = Path(args.skills_dir) if args.skills_dir else default_skills_dir()
    data = audit(skills_dir)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 掃描完成，共 {len(data)} 個技能，結果已輸出至 {args.output}")
    for item in data:
        print(f"  - {item['name']} ({item['skill_md_lines']} 行)")
