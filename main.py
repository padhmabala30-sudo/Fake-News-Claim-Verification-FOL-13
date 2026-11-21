from knowledge_base import KnowledgeBase
from claim_processor import ClaimProcessor
from inference_engine import FOLInferenceEngine
from explanation import print_explanation
from xai_explainer import XAIExplainer

def main():
    print("=" * 65)
    print("  FAKE NEWS CLAIM VERIFICATION SYSTEM (FOL + Explainable AI)")
    print("  K. Ramakrishnan College of Engineering - AI & Data Science")
    print("=" * 65)

    kb = KnowledgeBase()
    processor = ClaimProcessor()
    engine = FOLInferenceEngine(kb)
    explainer = XAIExplainer(kb)

    print(f"\nKnowledge Base: {kb.total_facts()} facts | {len(kb.rules)} logical rules")
    print("Type ANY claim. You will receive a full Explainable AI report.\n")

    while True:
        print("-" * 65)
        claim = input("Enter claim (or 'exit'): ").strip()
        if claim.lower() in ("exit", "quit", "q"):
            print("Thank you.")
            break
        if len(claim) < 5:
            print("Please enter a longer claim.")
            continue

        claim_info = processor.extract_entities_and_predicates(claim)
        print("\nExtracted Entities   :", claim_info["entities"] or "None")
        print("Suggested Predicates :", claim_info["suggested_predicates"] or "None")

        user_predicate, user_args = processor.try_map_to_fol(claim_info, kb)

        if user_predicate is None:
            print("\n🟡 DECISION: UNKNOWN")
            print("Could not map claim strongly to FOL predicates.")
            continue

        result = engine.check_consistency(claim_info, user_predicate, user_args)
        print_explanation(result, claim)

        # ---- XAI Report ----
        xai = explainer.generate_full_explanation(
            claim, claim_info, user_predicate, user_args, result
        )
        print("\n" + "=" * 65)
        print("          EXPLAINABLE AI (XAI) REPORT")
        print("=" * 65)
        print("\n📖 Plain-English Explanation:")
        print("  " + xai["natural_language"])
        print("\n❓ Why this decision?")
        for r in xai["why"]:
            print("  •", r)
        print("\n⚖️ Fact Importance:")
        for item in xai["fact_importance"]:
            print(f"  [{item['role']}] {item['fact']} (importance={item['importance']})")
        print("\n🔄 Counterfactuals:")
        for cf in xai["counterfactuals"]:
            print("  •", cf)
        print(f"\n📐 Rule: {xai['logical_rule']['name']} — {xai['logical_rule']['description']}")
        print(f"📊 Confidence: {xai['confidence_breakdown']['score']:.2f} ({xai['confidence_breakdown']['level']})")
        print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
