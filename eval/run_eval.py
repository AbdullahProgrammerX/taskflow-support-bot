"""
Run RAG evaluation against eval/questions.jsonl.

Usage (project root, venv active):
  python eval/run_eval.py
  python eval/run_eval.py --limit 5
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.config import settings
from src.rag.pipeline import answer_with_rag
from src.rag.retriever import retrieve

QUESTIONS_PATH = Path(__file__).parent / "questions.jsonl"
RESULTS_DIR = Path(__file__).parent / "results"

REFUSAL_PATTERNS = [
    r"bilmiyorum",
    r"bulamad[ıi]m",
    r"dokümantasyon",
    r"support@taskflow",
    r"yeterli bilgi yok",
    r"cannot answer",
    r"don't know",
    r"do not know",
]


@dataclass
class EvalCase:
    id: str
    question: str
    expected_sources: list[str]
    expected_keywords: list[str]
    must_refuse: bool


@dataclass
class EvalResult:
    id: str
    question: str
    passed: bool
    retrieval_hit: bool | None
    keyword_hit: bool | None
    refusal_ok: bool | None
    answer_preview: str
    sources: list[str]


def load_questions(path: Path) -> list[EvalCase]:
    cases: list[EvalCase] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        cases.append(
            EvalCase(
                id=row["id"],
                question=row["question"],
                expected_sources=row.get("expected_sources", []),
                expected_keywords=row.get("expected_keywords", []),
                must_refuse=bool(row.get("must_refuse", False)),
            )
        )
    return cases


def is_refusal(text: str) -> bool:
    lower = text.lower()
    return any(re.search(p, lower) for p in REFUSAL_PATTERNS)


def check_keywords(answer: str, keywords: list[str]) -> bool:
    if not keywords:
        return True
    lower = answer.lower()
    return any(kw.lower() in lower for kw in keywords)


def check_retrieval(question: str, expected_sources: list[str]) -> bool:
    if not expected_sources:
        return True
    chunks = retrieve(question)
    found = {c.source for c in chunks}
    return any(src in found for src in expected_sources)


def evaluate_case(case: EvalCase) -> EvalResult:
    rag = answer_with_rag(case.question)
    answer = rag.answer
    source_files = [s.file for s in rag.sources]

    if case.must_refuse:
        refusal_ok = is_refusal(answer)
        passed = refusal_ok
        return EvalResult(
            id=case.id,
            question=case.question,
            passed=passed,
            retrieval_hit=None,
            keyword_hit=None,
            refusal_ok=refusal_ok,
            answer_preview=answer[:200],
            sources=source_files,
        )

    retrieval_hit = check_retrieval(case.question, case.expected_sources)
    if not retrieval_hit and case.expected_sources:
        retrieval_hit = any(s in source_files for s in case.expected_sources)

    keyword_hit = check_keywords(answer, case.expected_keywords)
    passed = retrieval_hit and keyword_hit

    return EvalResult(
        id=case.id,
        question=case.question,
        passed=passed,
        retrieval_hit=retrieval_hit,
        keyword_hit=keyword_hit,
        refusal_ok=None,
        answer_preview=answer[:200],
        sources=source_files,
    )


def write_report(
    results: list[EvalResult],
    summary: dict,
    out_json: Path,
    out_md: Path,
) -> None:
    out_json.write_text(
        json.dumps({"summary": summary, "results": [asdict(r) for r in results]}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    lines = [
        "# Eval Report",
        "",
        f"**Date:** {summary['timestamp']}",
        f"**Model:** {summary['chat_model']}",
        "",
        "## Summary",
        "",
        f"| Metric | Score |",
        f"|--------|-------|",
        f"| Total | {summary['total']} |",
        f"| Passed | {summary['passed']} ({summary['pass_rate']:.0%}) |",
        f"| Retrieval (factual) | {summary['retrieval_rate']:.0%} |",
        f"| Keywords (factual) | {summary['keyword_rate']:.0%} |",
        f"| Refusal (trap) | {summary['refusal_rate']:.0%} |",
        "",
        "## Failed cases",
        "",
    ]
    failed = [r for r in results if not r.passed]
    if not failed:
        lines.append("_None — all passed._")
    else:
        for r in failed:
            lines.append(f"- **{r.id}**: {r.question}")
            lines.append(f"  - retrieval: {r.retrieval_hit}, keywords: {r.keyword_hit}, refusal: {r.refusal_ok}")
            lines.append(f"  - preview: {r.answer_preview[:120]}…")

    out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=0, help="Run only first N questions")
    args = parser.parse_args()

    if not settings.api_key_configured:
        print("ERROR: OPENAI_API_KEY not set")
        sys.exit(1)

    cases = load_questions(QUESTIONS_PATH)
    if args.limit > 0:
        cases = cases[: args.limit]

    print(f"Running eval on {len(cases)} questions…")
    results: list[EvalResult] = []
    for i, case in enumerate(cases, 1):
        print(f"  [{i}/{len(cases)}] {case.id}")
        results.append(evaluate_case(case))

    factual = [r for r in results if r.refusal_ok is None]
    traps = [r for r in results if r.refusal_ok is not None]

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "chat_model": settings.openai_chat_model,
        "total": len(results),
        "passed": sum(1 for r in results if r.passed),
        "pass_rate": sum(1 for r in results if r.passed) / len(results) if results else 0,
        "retrieval_rate": (
            sum(1 for r in factual if r.retrieval_hit) / len(factual) if factual else 0
        ),
        "keyword_rate": (
            sum(1 for r in factual if r.keyword_hit) / len(factual) if factual else 0
        ),
        "refusal_rate": (
            sum(1 for r in traps if r.refusal_ok) / len(traps) if traps else 0
        ),
    }

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_report(
        results,
        summary,
        RESULTS_DIR / "latest.json",
        RESULTS_DIR / "latest.md",
    )

    print()
    print(f"Pass rate:    {summary['pass_rate']:.0%} ({summary['passed']}/{summary['total']})")
    print(f"Retrieval:    {summary['retrieval_rate']:.0%}")
    print(f"Keywords:     {summary['keyword_rate']:.0%}")
    print(f"Refusal:      {summary['refusal_rate']:.0%}")
    print(f"Report:       eval/results/latest.md")


if __name__ == "__main__":
    main()
