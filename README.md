# QA Reliability Case Study

A scripted simulation of a verdict-classification failure mode seen in earlier work. It uses synthetic observations to exercise the difference between an incorrect output and insufficient evidence to issue a verdict.

## The simulated regression

An operation has exited, but its stop-time counter still shows one active member. A later observation confirms cleanup. The earlier rule treats the stale count as `INVALID`. The corrected rule checks direct exit, a final count of zero and successful cleanup before judging the output.

| Scripted observation | Earlier rule | Corrected rule |
| --- | --- | --- |
| Correct output, stale count, confirmed cleanup | `INVALID` | `PASS` |
| Wrong output, stale count, confirmed cleanup | `INVALID` | `FAIL` |
| Missing or nonzero final observation | `INVALID` | `INVALID` |

[Case study and verdict definitions](CASE-STUDY.md)

## Reproduce locally

Run from the repository root with Python 3.10 or later. The simulator uses the standard library and runs offline.

```sh
python -B reliability.py
python -B -m unittest -v
```

The demo prints 12/12 expected ordinary scripted verdicts and four focused scenarios. Tests vary the stage, output correctness, stop evidence, final evidence and cleanup. Local verification used Windows with Python 3.10.11 and 3.14.7. GitHub Actions is configured for Windows and Linux with both Python series. [Hosted GitHub Actions CI](https://github.com/ryanlupardus/qa-reliability-case-study/actions/runs/45376595699) passed all four jobs on Windows and Linux with Python 3.10 and 3.14.

The fixture demonstrates verdict logic. The historical implementation, campaign records, host behavior and natural defect frequency are outside its scope. [Contributions and AI assistance](CONTRIBUTIONS.md)

## Reuse

This portfolio sample carries no open-source license grant.
