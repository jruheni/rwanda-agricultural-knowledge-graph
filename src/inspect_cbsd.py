
from rdflib import RDFS
from knowledge_graph import load_knowledge_graph

graph = load_knowledge_graph()

print("=" * 65)
print("CBSD KNOWLEDGE GRAPH INSPECTION")
print("=" * 65)

# Find relevant entities by their labels
entities = {}

for subject, label in graph.subject_objects(RDFS.label):
    label_text = str(label)

    if any(term in label_text.lower() for term in [
        "cassava",
        "brown streak",
        "whitefly",
        "chlorosis",
        "lesion",
        "necrosis",
        "constriction",
        "dieback",
        "planting material",
        "tolerant",
        "roguing"
    ]):
        entities[subject] = label_text

# Display all relationships involving those entities
for subject, predicate, obj in graph:
    if subject in entities or obj in entities:
        subject_label = entities.get(subject, str(subject))
        object_label = entities.get(obj, str(obj))

        print(f"\n{subject_label}")
        print(f"  Predicate: {predicate}")
        print(f"  Object:    {object_label}")
