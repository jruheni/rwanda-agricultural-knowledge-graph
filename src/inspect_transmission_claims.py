
from rdflib import RDF, RDFS
from knowledge_graph import load_knowledge_graph, AGRI

graph = load_knowledge_graph()

print("=" * 65)
print("CBSD TRANSMISSION CLAIM INSPECTION")
print("=" * 65)

for subject, predicate, obj in graph.triples(
    (None, AGRI.transmittedBy, None)
):
    print("\nASSERTED RELATIONSHIP:")
    print("Subject:", subject)
    print("Object:", obj)

    for claim in graph.subjects(RDF.subject, subject):
        if (
            (claim, RDF.predicate, predicate) in graph
            and (claim, RDF.object, obj) in graph
        ):
            print("\nSUPPORTING CLAIM:", claim)

            for prop in [
                AGRI.claimDescription,
                AGRI.evidenceDescription,
                AGRI.evidenceSection,
                AGRI.supportedBy
            ]:
                for value in graph.objects(claim, prop):
                    print(f"{prop.split('#')[-1]}: {value}")

print("\n" + "=" * 65)
