from rdflib import Graph

# Load ontology
graph = Graph()

graph.parse(
    "ontology/agriculture.ttl",
    format="turtle"
)

print("Ontology loaded successfully!")
print(f"Number of triples: {len(graph)}")

# Display the defined classes
query = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX agri: <http://example.org/agriculture#>

SELECT ?class
WHERE {
    ?class a owl:Class .
}
"""

for row in graph.query(query):
    print(row["class"])