"""
Explainable AI (XAI) Module for FOL Claim Verification
-------------------------------------------------------
Generates human-readable explanations, counterfactuals,
fact importance, and decision rationale.
"""

from typing import Dict, List, Any, Optional


class XAIExplainer:
    """
    Advanced Explainable AI layer on top of FOL inference results.
    """

    def __init__(self, kb):
        self.kb = kb

    def generate_full_explanation(self, claim: str, claim_info: dict,
                                   user_predicate: str, user_args: tuple,
                                   result: dict) -> Dict[str, Any]:
        """
        Build a complete XAI report for the verification decision.
        """
        status = result["status"]

        report = {
            "decision": status,
            "summary": self._decision_summary(status, claim),
            "why": self._why_explanation(status, user_predicate, user_args, result),
            "key_evidence": self._key_evidence(result),
            "fact_importance": self._fact_importance(result),
            "logical_rule": self._rule_explanation(result),
            "counterfactuals": self._counterfactuals(status, user_predicate, user_args, result),
            "confidence_breakdown": self._confidence_breakdown(result),
            "natural_language": self._natural_language_narrative(
                claim, status, user_predicate, user_args, result
            ),
            "limitations": self._limitations(status, result),
        }
        return report

    # ------------------------------------------------------------------
    def _decision_summary(self, status: str, claim: str) -> str:
        if status == "CONSISTENT":
            return f'The claim "{claim}" is CONSISTENT with the verified knowledge base.'
        if status == "INCONSISTENT":
            return f'The claim "{claim}" is INCONSISTENT — it contradicts known facts under logical rules.'
        return f'The claim "{claim}" cannot be fully verified (UNKNOWN) due to insufficient matching evidence.'

    def _why_explanation(self, status, predicate, args, result) -> List[str]:
        reasons = []
        if status == "CONSISTENT":
            reasons.append(f"The exact FOL statement {predicate}{args} exists in the Knowledge Base.")
            reasons.append("No uniqueness or consistency rule is violated.")
            if result.get("matched_rule"):
                reasons.append(f"Matched rule: {result['matched_rule']} (Exact Entailment).")
        elif status == "INCONSISTENT":
            reasons.append(f"The claim asserts {predicate}{args}.")
            if result["contradicting_facts"]:
                reasons.append(f"This conflicts with the known fact: {result['contradicting_facts'][0]}.")
            if result.get("matched_rule"):
                reasons.append(f"Logical rule triggered: {result['matched_rule']}.")
                # Find rule description
                for rule in self.kb.rules:
                    if rule.name == result["matched_rule"]:
                        reasons.append(f"Rule meaning: {rule.description}.")
                        break
            reasons.append("Under FOL uniqueness/consistency constraints, both cannot be true simultaneously.")
        else:
            reasons.append("No exact matching fact was found in the Knowledge Base.")
            reasons.append("No clear contradiction (uniqueness violation) was detected either.")
            reasons.append("Therefore the system cannot confirm or deny the claim with current knowledge.")
        return reasons

    def _key_evidence(self, result) -> Dict[str, List[str]]:
        return {
            "supporting": result.get("supporting_facts", []),
            "contradicting": result.get("contradicting_facts", []),
        }

    def _fact_importance(self, result) -> List[Dict[str, Any]]:
        """
        Assign importance scores to facts that influenced the decision.
        (Simplified attribution suitable for FOL systems)
        """
        items = []
        for f in result.get("supporting_facts", []):
            items.append({
                "fact": f,
                "role": "Supporting",
                "importance": 1.0,
                "contribution": "Directly entails the claim"
            })
        for f in result.get("contradicting_facts", []):
            items.append({
                "fact": f,
                "role": "Contradicting",
                "importance": 1.0,
                "contribution": "Triggers inconsistency under logical rule"
            })
        if not items:
            items.append({
                "fact": "(none)",
                "role": "None",
                "importance": 0.0,
                "contribution": "No decisive fact found"
            })
        return items

    def _rule_explanation(self, result) -> Dict[str, str]:
        rule_name = result.get("matched_rule") or "None"
        description = "No specific rule was required (or knowledge gap)."
        for rule in self.kb.rules:
            if rule.name == rule_name:
                description = rule.description
                break
        if rule_name == "ExactEntailment":
            description = "The claim is directly present as a verified fact in the Knowledge Base."
        return {"name": rule_name, "description": description}

    def _counterfactuals(self, status, predicate, args, result) -> List[str]:
        """
        Generate simple counterfactual explanations:
        "If the claim had said X instead of Y, the decision would change."
        """
        cfs = []
        if status == "INCONSISTENT" and result.get("contradicting_facts"):
            # Suggest the correct version
            correct = result["contradicting_facts"][0]
            cfs.append(f'If the claim had matched the known fact "{correct}", it would be CONSISTENT.')
            cfs.append("Changing the conflicting argument to the verified value would remove the contradiction.")
        elif status == "CONSISTENT":
            cfs.append("If any key argument in the claim were altered to a different value, "
                       "the uniqueness rule would likely mark it INCONSISTENT.")
            cfs.append("If the matching fact were removed from the Knowledge Base, the decision would become UNKNOWN.")
        else:
            cfs.append("If a supporting fact were added to the Knowledge Base, the claim could become CONSISTENT.")
            cfs.append("If a contradicting fact were present, the claim could become INCONSISTENT.")
        return cfs

    def _confidence_breakdown(self, result) -> Dict[str, Any]:
        conf = result.get("confidence", 0.0)
        return {
            "score": conf,
            "level": "High" if conf >= 0.9 else ("Medium" if conf >= 0.6 else "Low"),
            "source": ", ".join(result.get("sources") or ["—"]),
            "category": result.get("category") or "—",
            "interpretation": (
                "High confidence — fact is well-established in the knowledge base."
                if conf >= 0.9 else
                "Medium confidence — fact is present but with moderate certainty."
                if conf >= 0.6 else
                "Low / no confidence — decision relies on absence of evidence."
            )
        }

    def _natural_language_narrative(self, claim, status, predicate, args, result) -> str:
        """
        Produce a fluent paragraph that a non-technical user can understand.
        """
        if status == "CONSISTENT":
            evidence = result["supporting_facts"][0] if result.get("supporting_facts") else predicate + str(args)
            return (
                f'After analysing the claim "{claim}", the system converted it into the logical form '
                f'{predicate}{args}. This exact statement is present in the verified Knowledge Base '
                f'as "{evidence}". Because the claim is directly entailed by known facts and no '
                f'consistency rule is broken, the system concludes that the claim is CONSISTENT '
                f'(reliable / true according to current knowledge).'
            )
        if status == "INCONSISTENT":
            conflict = result["contradicting_facts"][0] if result.get("contradicting_facts") else "a known fact"
            rule = result.get("matched_rule") or "a uniqueness rule"
            return (
                f'After analysing the claim "{claim}", the system converted it into the logical form '
                f'{predicate}{args}. However, the Knowledge Base contains the conflicting fact "{conflict}". '
                f'Under the logical rule "{rule}", both statements cannot be true at the same time. '
                f'Therefore the system concludes that the claim is INCONSISTENT (contradicts verified knowledge).'
            )
        return (
            f'After analysing the claim "{claim}", the system could not find a strong matching fact '
            f'nor a clear contradiction in the Knowledge Base. The extracted entities and predicates '
            f'were insufficient to reach a definite conclusion. Hence the decision is UNKNOWN — '
            f'more evidence would be required for verification.'
        )

    def _limitations(self, status, result) -> List[str]:
        limits = [
            "Explanation is based only on the current Knowledge Base (closed-world assumption).",
            "Natural-language understanding is rule-based and may miss highly unusual phrasing.",
        ]
        if status == "UNKNOWN":
            limits.append("UNKNOWN does not mean the claim is false — only that evidence is missing.")
        if result.get("confidence", 1) < 1.0:
            limits.append("Confidence is derived from the source reliability stored in the Knowledge Base.")
        return limits
