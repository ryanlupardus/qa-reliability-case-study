# Testing a verdict under delayed bookkeeping

Ordinary fixtures exercise the path where exit and the stop-time counter agree. A focused fixture combines direct exit with a temporarily positive count. A final observation then establishes whether cleanup succeeded.

Both versions consume the same synthetic observations. The earlier rule rejects the delayed reading immediately. The corrected rule can proceed after direct exit if the final observation shows zero active work and cleanup succeeds. `PASS` accepts a matching output. `FAIL` records an output mismatch or verified residual work. `INVALID` means the evidence is insufficient for a valid judgment.

The regression tests vary which of two stages has the delayed count and whether the output matches. Other cases cover missing or nonzero final proof, invalid stop data, failed cleanup and residual work. The simulator directly supplies each observation, so its output establishes how the rules classify controlled inputs. Estimating a host failure rate would require measurements of real operations.
