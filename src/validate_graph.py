
from pathlib import Path

from pyshacl import validate
from rdflib import Graph, RDF

from knowledge_graph import load_knowledge_graph, AGRI


# ---------------------------------------------------------
# FILE PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SHAPES_PATH = (
    PROJECT_ROOT / "validation" / "agriculture_shapes.ttl"
)


# ---------------------------------------------------------
# SHACL VALIDATION
# ---------------------------------------------------------

def validate_shacl(data_graph):

    shapes_graph = Graph()

    if not SHAPES_PATH.exists():
        raise FileNotFoundError(
            f"SHACL shapes file not found: {SHAPES_PATH}"
        )

    shapes_graph.parse(
        SHAPES_PATH.as_uri(),
        format="turtle",
    )

    print(f"Loaded {len(shapes_graph)} SHACL triples.")

    conforms, report_graph, report_text = validate(
        data_graph,
        shacl_graph=shapes_graph,
        inference="none",
        abort_on_first=False,
        allow_infos=False,
        allow_warnings=False,
        meta_shacl=False,
        advanced=False,
        js=False,
    )

    print("\nSHACL VALIDATION:")
    print(report_text)

    return conforms


# ---------------------------------------------------------
# CLAIM-TO-GRAPH CONSISTENCY
# ---------------------------------------------------------

def validate_claim_assertions(data_graph):

    print("\n" + "=" * 60)
    print("CLAIM-TO-GRAPH CONSISTENCY")
    print("=" * 60)

    claims = list(
        data_graph.subjects(
            RDF.type,
            AGRI.Claim,
        )
    )

    print(f"Claims found: {len(claims)}")

    valid_claims = 0
    invalid_claims = []

    for claim in claims:

        subjects = list(
            data_graph.objects(claim, RDF.subject)
        )

        predicates = list(
            data_graph.objects(claim, RDF.predicate)
        )

        objects = list(
            data_graph.objects(claim, RDF.object)
        )

        # Each claim must describe exactly one triple.
        if (
            len(subjects) != 1
            or len(predicates) != 1
            or len(objects) != 1
        ):
            invalid_claims.append(
                (claim, "Incomplete or ambiguous RDF statement")
            )
            continue

        subject = subjects[0]
        predicate = predicates[0]
        obj = objects[0]

        # Check whether the described relationship
        # actually exists in the knowledge graph.
        if (subject, predicate, obj) in data_graph:

            valid_claims += 1

        else:

            invalid_claims.append(
                (
                    claim,
                    f"Missing relationship: "
                    f"{subject} {predicate} {obj}",
                )
            )

    print(f"Consistent claims: {valid_claims}")
    print(f"Inconsistent claims: {len(invalid_claims)}")

    if invalid_claims:

        print("\nINCONSISTENCIES:")

        for claim, reason in invalid_claims:
            print(f"\nClaim: {claim}")
            print(f"Problem: {reason}")

    else:

        print(
            "\nSUCCESS: Every claim corresponds "
            "to an asserted graph relationship."
        )

    return len(invalid_claims) == 0


# ---------------------------------------------------------
# MAIN VALIDATION
# ---------------------------------------------------------

def validate_knowledge_graph():

    print("=" * 60)
    print("AGRICULTURAL KNOWLEDGE GRAPH VALIDATION")
    print("=" * 60)

    print("\nLoading knowledge graph...")

    data_graph = load_knowledge_graph()

    print(f"Loaded {len(data_graph)} triples.")

    shacl_conforms = validate_shacl(data_graph)

    claims_consistent = validate_claim_assertions(
        data_graph
    )

    # Both validation stages must pass.
    overall_success = (
        shacl_conforms and claims_consistent
    )

    print("\n" + "=" * 60)
    print("FINAL VALIDATION RESULT")
    print("=" * 60)

    if overall_success:

        print(
            "\nSUCCESS: Knowledge graph passed "
            "all validation checks."
        )

    else:

        print(
            "\nFAILURE: Knowledge graph contains "
            "validation problems."
        )

    return overall_success


# ---------------------------------------------------------
# EXECUTION
# ---------------------------------------------------------

if __name__ == "__main__":

    success = validate_knowledge_graph()

    if not success:
        raise SystemExit(1)
