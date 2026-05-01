from __future__ import annotations

import argparse
import json
from pathlib import Path

from .agent import build_handoff_packet
from .models import GoalRequest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a public-safe agent handoff packet.")
    parser.add_argument("goal_json", help="Path to a goal request JSON file.")
    parser.add_argument("--out", help="Optional output JSON path.")
    args = parser.parse_args()

    goal_path = Path(args.goal_json)
    goal = GoalRequest.from_dict(json.loads(goal_path.read_text(encoding="utf-8")))
    packet = build_handoff_packet(goal)
    output = json.dumps(packet, indent=2, ensure_ascii=False)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
