"""
Advanced FOL Inference Engine
-----------------------------
- Uses structured Fact objects (confidence, source, category)
- Applies uniqueness / consistency rules
- Supports multi-level explanation
- Returns rich result for dashboard / terminal
"""

from knowledge_base import KnowledgeBase, Fact
from typing import Dict, List, Tuple, Any, Optional

class FOLInferenceEngine:
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb

    def check_consistency(self, claim_info: dict, user_predicate: str, user_args: tuple) -> Dict[str, Any]:
        result = {
            "status": "UNKNOWN",
            "supporting_facts": [],
            "contradicting_facts": [],
            "reasoning_steps": [],
            "confidence": 0.0,
            "matched_rule": None,
            "sources": [],
            "category": None,
        }

        fact_objects = self.kb.get_fact_objects(user_predicate)
        known_args = [f.arguments for f in fact_objects]

        result["reasoning_steps"].append(
            f"1. Claim converted to FOL formula: {user_predicate}{user_args}"
        )
        result["reasoning_steps"].append(
            f"2. Retrieving all facts for predicate '{user_predicate}' from Knowledge Base "
            f"({len(fact_objects)} facts found)..."
        )

        if not fact_objects:
            result["status"] = "UNKNOWN"
            result["reasoning_steps"].append(
                "3. No facts exist in the Knowledge Base for this predicate."
            )
            result["reasoning_steps"].append(
                "4. Decision → UNKNOWN (knowledge gap)"
            )
            return result

        # ----- Exact match → CONSISTENT -----
        for f in fact_objects:
            if f.arguments == user_args:
                result["status"] = "CONSISTENT"
                result["supporting_facts"].append(f.as_fol())
                result["confidence"] = f.confidence
                result["sources"].append(f.source)
                result["category"] = f.category.value
                result["reasoning_steps"].append(
                    f"3. Exact match found: {f.as_fol()}"
                )
                result["reasoning_steps"].append(
                    f"   Source: {f.source} | Confidence: {f.confidence:.2f} | Category: {f.category.value}"
                )
                result["reasoning_steps"].append(
                    "4. Applying consistency rule → Claim is entailed by the Knowledge Base."
                )
                result["reasoning_steps"].append(
                    "5. Final Decision → CONSISTENT"
                )
                result["matched_rule"] = "ExactEntailment"
                return result

        # ----- Uniqueness / Contradiction check -----
        # Look for facts that share the key argument(s) but differ in the rest
        for rule in self.kb.rules:
            if rule.predicate != user_predicate:
                continue

            key_arity = rule.key_arity
            if len(user_args) < key_arity:
                continue

            user_key = user_args[:key_arity]

            for f in fact_objects:
                fact_key = f.arguments[:key_arity]
                if fact_key == user_key and f.arguments != user_args:
                    # Contradiction under uniqueness rule
                    result["status"] = "INCONSISTENT"
                    result["contradicting_facts"].append(f.as_fol())
                    result["confidence"] = f.confidence
                    result["sources"].append(f.source)
                    result["category"] = f.category.value
                    result["matched_rule"] = rule.name

                    result["reasoning_steps"].append(
                        f"3. Contradiction detected under rule: {rule.name}"
                    )
                    result["reasoning_steps"].append(
                        f"   Rule meaning: {rule.description}"
                    )
                    result["reasoning_steps"].append(
                        f"   Claim asserts   : {user_predicate}{user_args}"
                    )
                    result["reasoning_steps"].append(
                        f"   Knowledge Base  : {f.as_fol()}"
                    )
                    result["reasoning_steps"].append(
                        f"   Source of KB fact: {f.source} (confidence {f.confidence:.2f})"
                    )
                    result["reasoning_steps"].append(
                        "4. Because the rule enforces uniqueness/consistency, "
                        "the claim cannot be true at the same time as the known fact."
                    )
                    result["reasoning_steps"].append(
                        "5. Final Decision → INCONSISTENT"
                    )
                    return result

        # ----- Special handling for IsCapitalOf (country side uniqueness) -----
        if user_predicate == "IsCapitalOf" and len(user_args) == 2:
            city, country = user_args
            for f in fact_objects:
                if f.arguments[1] == country and f.arguments[0] != city:
                    result["status"] = "INCONSISTENT"
                    result["contradicting_facts"].append(f.as_fol())
                    result["confidence"] = f.confidence
                    result["sources"].append(f.source)
                    result["category"] = f.category.value
                    result["matched_rule"] = "UniqueCapital"
                    result["reasoning_steps"].append(
                        "3. Contradiction: different capital claimed for the same country"
                    )
                    result["reasoning_steps"].append(
                        f"   Claim asserts   : IsCapitalOf{user_args}"
                    )
                    result["reasoning_steps"].append(
                        f"   Knowledge Base  : {f.as_fol()}"
                    )
                    result["reasoning_steps"].append(
                        "4. A country can have only one official capital → INCONSISTENT"
                    )
                    result["reasoning_steps"].append(
                        "5. Final Decision → INCONSISTENT"
                    )
                    return result

        # ----- No match, no contradiction -----
        result["status"] = "UNKNOWN"
        result["reasoning_steps"].append(
            "3. No exact match and no uniqueness violation found."
        )
        result["reasoning_steps"].append(
            "4. The claim is neither entailed nor contradicted by current knowledge."
        )
        result["reasoning_steps"].append(
            "5. Final Decision → UNKNOWN (insufficient evidence)"
        )
        return result
