from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class UserProfile:
    track: str  # "수시" or "정시"
    gpa: Optional[float] = None
    csat_summary: Optional[str] = None
    major_keyword: str = "미정"
    preference: str = "적정 위주"


def load_rules(path: str = "./configs/rules_ku_sejong_2026.json") -> Dict[str, Any]:
    p = Path(path)
    if not p.exists():
        return {"programs": []}
    return json.loads(p.read_text(encoding="utf-8"))


def recommend_six(profile: UserProfile, rules: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    MVP: rules.json에 (모집단위/전형/핵심조건)만 적어두고,
    프로필에 따라 간단 필터 → 상향/적정/안전 2+2+2로 뽑는 자리.
    """
    programs = rules.get("programs", [])
    if not programs:
        return []

    # 여기부터는 너 rules 구조에 맞춰 로직 채우면 됨 (MVP로는 그냥 앞에서 6개)
    selected = programs[:6]
    out = []
    for i, p in enumerate(selected):
        out.append(
            {
                "bucket": p.get("bucket", ["상향", "적정", "안전"][min(i // 2, 2)]),
                "program": p.get("program", "모집단위 미상"),
                "track": p.get("track", profile.track),
                "note": p.get("note", "요강 근거 기반으로 조건 확인 필요"),
            }
        )
    return out
