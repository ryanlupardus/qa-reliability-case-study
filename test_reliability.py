from dataclasses import replace
import unittest

from reliability import Observation, evaluate


class ReliabilityTest(unittest.TestCase):
    def stages(self, correct, stage_index, **fields):
        stages = [Observation(correct), Observation(True)]
        stages[stage_index] = replace(stages[stage_index], **fields)
        return stages

    def test_ordinary_verdicts_match(self):
        for correct, expected in [(True, "PASS"), (False, "FAIL")]:
            for corrected in (False, True):
                self.assertEqual(evaluate(self.stages(correct, 0), corrected=corrected), expected)

    def test_delayed_count_exposes_original_defect_in_each_stage(self):
        for stage in (0, 1):
            for correct, expected in [(True, "PASS"), (False, "FAIL")]:
                with self.subTest(stage=stage, correct=correct):
                    observations = self.stages(correct, stage, stop_counts=(1, 1))
                    self.assertEqual(evaluate(observations, corrected=False), "INVALID")
                    self.assertEqual(evaluate(observations, corrected=True), expected)

    def test_final_proof_and_stop_evidence_are_required(self):
        for stage in (0, 1):
            for correct in (False, True):
                for bad in ({"final_active": None}, {"final_active": 1}, {"cleanup_succeeded": False},
                            {"stop_counts": None}, {"stop_counts": (2, 1)}, {"direct_exit": False}):
                    fields = {"stop_counts": (1, 1)} | bad
                    with self.subTest(stage=stage, correct=correct, fields=fields):
                        self.assertEqual(evaluate(self.stages(correct, stage, **fields), corrected=True), "INVALID")

    def test_verified_residual_fails(self):
        for stage in (0, 1):
            self.assertEqual(evaluate(self.stages(True, stage, stop_counts=(1, 2)), corrected=True), "FAIL")
