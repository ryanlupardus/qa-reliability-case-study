"""Simulate a verifier reading stale bookkeeping and later cleanup evidence."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Observation:
    output_matches: bool
    stop_counts: tuple[int, int] | None = (0, 1)
    direct_exit: bool = True
    final_active: int | None = 0
    cleanup_succeeded: bool = True


def evaluate(stages, *, corrected):
    """Each stage is a trusted synthetic observation, with counts (active, cumulative)."""
    for stage in stages:
        if not stage.direct_exit or stage.stop_counts is None:
            return "INVALID"
        active, total = stage.stop_counts
        if not 0 <= active <= total or total < 1:
            return "INVALID"
        if active == 1 and total == 1 and not corrected:
            return "INVALID"
        if stage.final_active != 0 or not stage.cleanup_succeeded:
            return "INVALID"
    still_active = any(stage.stop_counts[0] > 0 and stage.stop_counts[1] > 1 for stage in stages)
    return "FAIL" if still_active or not stages[0].output_matches else "PASS"


def run_demo():
    ordinary = [(Observation(True), Observation(True))] * 8
    ordinary += [(Observation(False), Observation(True))] * 4
    expected = ["PASS"] * 8 + ["FAIL"] * 4
    observed = [evaluate(stages, corrected=False) for stages in ordinary]
    matches = sum(a == b for a, b in zip(observed, expected, strict=True))
    print(f"Ordinary scripted cases: {matches}/{len(expected)} expected verdicts")
    print("Focused scripted scenario           Earlier   Corrected")
    for stages, label in [
        ((Observation(True, (1, 1)), Observation(True)), "Stage 1 count stale, correct"),
        ((Observation(False), Observation(True, (1, 1))), "Stage 2 count stale, wrong"),
        ((Observation(True), Observation(True, (1, 1), final_active=None)), "Missing final proof"),
        ((Observation(True, (1, 1), final_active=1), Observation(True)), "Nonzero final observation"),
    ]:
        print(f"{label:35} {evaluate(stages, corrected=False):9} {evaluate(stages, corrected=True)}")


if __name__ == "__main__":
    run_demo()
