"""CLI interface for hermes-dreaming."""

import argparse
import json
import sys

from . import engine, store
from .models import ProposalStatus


def cmd_dream(args):
    print("=== Hermes Dreaming: Running self-improvement cycle ===\n")
    proposals = engine.dream(data_dir=args.data_dir)
    if not proposals:
        print("No new proposals generated.")
        return
    print(f"Generated {len(proposals)} proposal(s):\n")
    for p in proposals:
        print(f"  {p.summary_line()}")
    print(f"\nRun 'hermes-dreaming review' to inspect details.")


def cmd_review(args):
    proposals = engine.review(data_dir=args.data_dir)
    if not proposals:
        print("No staged proposals to review.")
        return
    print(f"=== {len(proposals)} Staged Proposal(s) ===\n")
    for p in proposals:
        print(f"  {p.summary_line()}")
        print(f"    Reason: {p.reason}")
        if p.before:
            print(f"    Before: {p.before}")
        print(f"    After:  {p.after}")
        print()
    print("Use 'hermes-dreaming approve <id> [<id>...]' or 'hermes-dreaming discard <id> [<id>...]'")


def cmd_approve(args):
    if args.all:
        ids = [p.id for p in store.staged_proposals(args.data_dir)]
    else:
        ids = args.ids
    if not ids:
        print("No proposal IDs specified. Use --all or provide IDs.")
        return
    count = engine.approve(ids, data_dir=args.data_dir)
    print(f"Approved {count} proposal(s).")
    print("Run 'hermes-dreaming apply' to apply approved changes.")


def cmd_discard(args):
    if args.all:
        ids = [p.id for p in store.staged_proposals(args.data_dir)]
    else:
        ids = args.ids
    if not ids:
        print("No proposal IDs specified. Use --all or provide IDs.")
        return
    count = engine.discard(ids, data_dir=args.data_dir)
    print(f"Discarded {count} proposal(s).")


def cmd_apply(args):
    count = engine.apply(data_dir=args.data_dir)
    if count == 0:
        print("No approved proposals to apply.")
    else:
        print(f"Applied {count} proposal(s) to agent knowledge base.")
        print("\nUpdated stores:")
        for name in ["memory.json", "skills.json", "facts.json"]:
            path = store._path(name, args.data_dir)
            if path.exists():
                with open(path) as f:
                    data = json.load(f)
                if data:
                    print(f"  {name}: {len(data)} entries")


def cmd_status(args):
    proposals = store.load_proposals(args.data_dir)
    if not proposals:
        print("No proposals in store.")
        return
    counts = {}
    for p in proposals:
        counts[p.status.value] = counts.get(p.status.value, 0) + 1
    print("=== Proposal Status ===")
    for status, count in sorted(counts.items()):
        print(f"  {status}: {count}")
    print()
    memory = store.load_memory(args.data_dir)
    skills = store.load_skills(args.data_dir)
    facts = store.load_facts(args.data_dir)
    print("=== Knowledge Base ===")
    print(f"  Memory entries: {len(memory)}")
    print(f"  Skills:         {len(skills)}")
    print(f"  Facts:          {len(facts)}")


def main():
    parser = argparse.ArgumentParser(
        prog="hermes-dreaming",
        description="Staged self-improvement engine with review gates",
    )
    parser.add_argument("--data-dir", default=store.DEFAULT_DIR,
                        help="Directory for persistent data (default: .hermes_data)")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("dream", help="Run a dreaming cycle to generate proposals")
    sub.add_parser("review", help="Review staged proposals")

    p_approve = sub.add_parser("approve", help="Approve proposals by ID")
    p_approve.add_argument("ids", nargs="*", help="Proposal IDs to approve")
    p_approve.add_argument("--all", action="store_true", help="Approve all staged")

    p_discard = sub.add_parser("discard", help="Discard proposals by ID")
    p_discard.add_argument("ids", nargs="*", help="Proposal IDs to discard")
    p_discard.add_argument("--all", action="store_true", help="Discard all staged")

    sub.add_parser("apply", help="Apply approved proposals")
    sub.add_parser("status", help="Show proposal and knowledge base status")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {
        "dream": cmd_dream,
        "review": cmd_review,
        "approve": cmd_approve,
        "discard": cmd_discard,
        "apply": cmd_apply,
        "status": cmd_status,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
