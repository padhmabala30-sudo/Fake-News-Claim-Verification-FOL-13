def print_explanation(result: dict, claim: str):
    print("\n" + "=" * 65)
    print("          ADVANCED FOL VERIFICATION REPORT")
    print("=" * 65)
    print(f"\nClaim: \"{claim}\"")

    print("\nReasoning Steps:")
    for step in result["reasoning_steps"]:
        print("  " + step)

    print("\nSupporting Facts:")
    if result["supporting_facts"]:
        for f in result["supporting_facts"]:
            print(f"  ✅ {f}")
    else:
        print("  (none)")

    print("\nContradicting Facts:")
    if result["contradicting_facts"]:
        for f in result["contradicting_facts"]:
            print(f"  ❌ {f}")
    else:
        print("  (none)")

    if result.get("matched_rule"):
        print(f"\nMatched Logical Rule : {result['matched_rule']}")
    if result.get("sources"):
        print(f"Source(s)            : {', '.join(result['sources'])}")
    if result.get("category"):
        print(f"Category             : {result['category']}")
    if result.get("confidence"):
        print(f"Confidence           : {result['confidence']:.2f}")

    print("\n" + "-" * 65)
    status = result["status"]
    if status == "CONSISTENT":
        print("🟢 FINAL DECISION: CONSISTENT")
        print("   The claim is entailed by the verified knowledge base.")
    elif status == "INCONSISTENT":
        print("🔴 FINAL DECISION: INCONSISTENT")
        print("   The claim contradicts known facts under logical rules.")
    else:
        print("🟡 FINAL DECISION: UNKNOWN")
        print("   Insufficient evidence in the knowledge base.")
    print("=" * 65 + "\n")
