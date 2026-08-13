#!/usr/bin/env python3
"""Unit tests for validate_post.py."""

from __future__ import annotations

import unittest

from validate_post import validate_text


class ValidatorTests(unittest.TestCase):
    def rules(self, text: str) -> set[str]:
        return {finding.rule for finding in validate_text(text, 0, 10000)}

    def test_rejects_em_dash(self) -> None:
        self.assertIn("em-dash", self.rules("Evidence from the test—measured across three runs—supports the result."))

    def test_rejects_list_hashtag_and_emoji(self) -> None:
        rules = self.rules("- A numbered benchmark result explains the mechanism clearly.\n\n#AI improves this claim 🚀")
        self.assertIn("plain-paragraphs", rules)
        self.assertIn("hashtags", rules)
        self.assertIn("emojis", rules)

    def test_rejects_rhetorical_contrast(self) -> None:
        self.assertIn("banned-language", self.rules("The result is not a model improvement but a change in evaluation design."))

    def test_rejects_marketing_language(self) -> None:
        self.assertIn("banned-language", self.rules("The company described the release as a revolutionary game changer."))

    def test_accepts_deterministically_clean_text(self) -> None:
        text = (
            "The evaluation measured thirty systems across six datasets and reported consistent gains. "
            "Researchers linked the improvement to explicit planning and stronger evidence checks."
        )
        errors = [finding for finding in validate_text(text, 0, 10000) if finding.severity == "error"]
        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
