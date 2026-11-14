
from pathlib import Path
from rdflib import Graph, Namespace, RDF, RDFS, Literal

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "agriculture.ttl"

AGRI = Namespace("http://example.org/agriculture#")

graph = Graph()
graph.parse(DATA_PATH, format="turtle")

disease = AGRI.CassavaBrownStreakDisease
whitefly = AGRI.Whitefly

viruses = [
    AGRI.CassavaBrownStreakVirus,
    AGRI.UgandanCassavaBrownStreakVirus,
]

# Find the existing disease-level transmission claims.
old_claims = []

for claim in graph.subjects(RDF.subject, disease):
    if (
        (claim, RDF.predicate, AGRI.transmittedBy) in graph
        and (claim, RDF.object, whitefly) in graph
    ):
        old_claims.append(claim)

# Preserve the original supporting sources and evidence sections.
claim_sources = []

for claim in old_claims:
    sources = list(graph.objects(claim, AGRI.supportedBy))
    sections = list(graph.objects(claim, AGRI.evidenceSection))

    for source in sources:
        section = sections[0] if sections else Literal(
            "Discussion of virus transmission"
        )
        claim_sources.append((source, section))

# Remove the old disease-level asserted relationship.
graph.remove((disease, AGRI.transmittedBy, whitefly))

# Remove old claims and their source-to-claim links.
for claim in old_claims:
    for source in graph.subjects(AGRI.hasClaim, claim):
        graph.remove((source, AGRI.hasClaim, claim))

    graph.remove((claim, None, None))

# Add the biologically accurate virus-level relationships.
for virus in viruses:
    graph.add((virus, AGRI.transmittedBy, whitefly))

# Add evidence-backed claims for both viruses and both sources.
for virus in viruses:
    for source, section in claim_sources:

        virus_name = str(virus).split("#")[-1]
        source_name = str(source).split("#")[-1]

        claim = AGRI[f"Claim_{virus_name}_TransmittedByWhitefly_{source_name}"]

        graph.add((claim, RDF.type, AGRI.Claim))
        graph.add((claim, RDF.subject, virus))
        graph.add((claim, RDF.predicate, AGRI.transmittedBy))
        graph.add((claim, RDF.object, whitefly))

        graph.add((
            claim,
            AGRI.claimDescription,
            Literal(
                f"{virus_name} is transmitted by whiteflies (Bemisia tabaci)."
            )
        ))

        if source_name == "Rwanda_CBSD_Research_2018":
            evidence = (
                "The study identifies Bemisia tabaci as an insect vector "
                "responsible for transmitting cassava brown streak viruses."
            )
        else:
            evidence = (
                "MINAGRI's annual report identifies Bemisia tabaci "
                "as the whitefly vector transmitting cassava brown "
                "streak viruses in Rwanda."
            )

        graph.add((
            claim,
            AGRI.evidenceDescription,
            Literal(evidence)
        ))

        graph.add((claim, AGRI.evidenceSection, section))
        graph.add((claim, AGRI.supportedBy, source))
        graph.add((source, AGRI.hasClaim, claim))

# Save the updated knowledge graph.
graph.serialize(destination=str(DATA_PATH), format="turtle")

print("=" * 60)
print("CBSD TRANSMISSION MIGRATION")
print("=" * 60)
print("Old claims removed:", len(old_claims))
print("New claims created:", len(viruses) * len(claim_sources))
print("Virus transmission relationships:")

for virus in viruses:
    print(f"  {virus.split('#')[-1]} -> Whitefly")

print("\nUpdated graph triples:", len(graph))
print("Saved:", DATA_PATH)
