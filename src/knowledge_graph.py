
from rdflib import Graph, Namespace, RDF, RDFS, OWL

AGRI = Namespace("http://example.org/agriculture#")


def load_knowledge_graph():
    """Load the ontology and agricultural facts into one RDF graph."""

    graph = Graph()

    # Register namespaces for readable output
    graph.bind("agri", AGRI)

    # Load ontology definitions
    graph.parse(
        "ontology/agriculture.ttl",
        format="turtle"
    )

    # Load agricultural facts
    graph.parse(
        "data/processed/agriculture.ttl",
        format="turtle"
    )

    return graph


def get_entities(graph, entity_type):
    """Retrieve all entities belonging to a given class."""

    query = """
    SELECT ?entity ?name
    WHERE {
        ?entity rdf:type ?class .
        ?entity rdfs:label ?name .
        FILTER(?class = ?target)
    }
    """

    results = graph.query(
        query,
        initBindings={"target": entity_type}
    )

    return [
        {
            "entity": str(row.entity),
            "name": str(row.name)
        }
        for row in results
    ]


if __name__ == "__main__":

    graph = load_knowledge_graph()

    print("Knowledge graph loaded successfully!")
    print(f"Total triples: {len(graph)}")

    print("\nCrops:")
    for crop in get_entities(graph, AGRI.Crop):
        print("-", crop["name"])

    print("\nPests:")
    for pest in get_entities(graph, AGRI.Pest):
        print("-", pest["name"])
