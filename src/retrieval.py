
import sys
import re
from pathlib import Path

from rdflib import RDF, RDFS

# ============================================================
# PROJECT PATHS AND IMPORTS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from knowledge_graph import load_knowledge_graph, AGRI


# ============================================================
# LOAD KNOWLEDGE GRAPH
# ============================================================

graph = load_knowledge_graph()


# ============================================================
# ENTITY RECOGNITION
# ============================================================

ENTITY_ALIASES = {
    "cassava brown streak disease": "CassavaBrownStreakDisease",
    "cassava brown streak virus": "CassavaBrownStreakVirus",
    "ugandan cassava brown streak virus": "UgandanCassavaBrownStreakVirus",
    "bean stem maggot": "BeanStemMaggot",
    "fall armyworm": "FallArmyworm",
    "bemisia tabaci": "Whitefly",
    "common beans": "CommonBean",
    "common bean": "CommonBean",
    "whitefly": "Whitefly",
    "cassava": "Cassava",
    "maize": "Maize",
    "corn": "Maize",
    "beans": "CommonBean",
    "bean fly": "BeanStemMaggot",
    "faw": "FallArmyworm",
    "cbsd": "CassavaBrownStreakDisease",
    "cbsv": "CassavaBrownStreakVirus",
    "ucbsv": "UgandanCassavaBrownStreakVirus",
}

ENTITY_URIS = {
    name: AGRI[name]
    for name in [
        "Maize",
        "FallArmyworm",
        "CommonBean",
        "BeanStemMaggot",
        "Cassava",
        "CassavaBrownStreakDisease",
        "CassavaBrownStreakVirus",
        "UgandanCassavaBrownStreakVirus",
        "Whitefly",
    ]
}


# ============================================================
# INTENT RECOGNITION
# ============================================================

INTENTS = {
    "vectors": [
        "vector",
        "vectors",
        "transmitted by",
        "transmission",
        "spread by",
        "spreads through",
        "how does it spread",
    ],
    "pathogens": [
        "pathogen",
        "pathogens",
        "virus",
        "viruses",
        "caused by",
        "causative agent",
    ],
    "management": [
        "management",
        "manage",
        "control",
        "controls",
        "prevent",
        "prevention",
        "treatment",
        "mitigation",
        "how to deal with",
        "how can farmers",
    ],
    "symptoms": [
        "symptom",
        "symptoms",
        "sign",
        "signs",
        "damage",
        "what does it cause",
        "what are the effects",
    ],
    "diseases": [
        "disease",
        "diseases",
    ],
    "pests": [
        "pest",
        "pests",
        "insect",
        "insects",
        "attack",
        "attacks",
        "affect",
        "affects",
    ],
}

UNSUPPORTED_INTENTS = {
    "chemical_treatment": [
        "chemical",
        "pesticide",
        "insecticide",
        "fungicide",
        "spray",
        "spraying",
    ],
    "economic_impact": [
        "yield",
        "yield loss",
        "economic impact",
        "financial impact",
        "economic loss",
        "cost of",
        "how much does",
        "how much do farmers lose",
        "how much is lost",
        "percentage of",
    ],
}

RELATIONSHIPS = {
    "pests": AGRI.affectedBy,
    "symptoms": AGRI.causesSymptom,
    "management": AGRI.managedBy,
    "diseases": AGRI.hasDisease,
    "pathogens": AGRI.causedBy,
}


# ============================================================
# GENERAL HELPERS
# ============================================================

def local_name(uri):
    """Extract the local name from an RDF URI."""
    return str(uri).split("#")[-1].split("/")[-1]


def get_label(uri):
    """Return an RDF label, falling back to the URI local name."""
    labels = list(graph.objects(uri, RDFS.label))

    if labels:
        return str(labels[0])

    return local_name(uri).replace("_", " ")


def extract_entities(question):
    """Identify known entities using whole-word alias matching."""
    question_lower = question.lower()
    found = []

    aliases = sorted(
        ENTITY_ALIASES.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    )

    for alias, entity in aliases:
        pattern = r"(?<![a-z0-9])" + re.escape(alias) + r"(?![a-z0-9])"

        if re.search(pattern, question_lower):
            if entity not in found:
                found.append(entity)

    return found


def extract_intent(question):
    """Identify the user's intended information category."""
    question_lower = question.lower()

    for intent, keywords in INTENTS.items():
        if any(keyword in question_lower for keyword in keywords):
            return intent

    return None


def detect_unsupported_intent(question):
    """Identify question types not supported by the knowledge graph."""
    question_lower = question.lower()

    for intent, keywords in UNSUPPORTED_INTENTS.items():
        if any(keyword in question_lower for keyword in keywords):
            return intent

    return None


# ============================================================
# CONVERSATIONAL CONTEXT
# ============================================================

def resolve_context_entities(previous_result):
    """
    Identify the entity most likely referenced by a follow-up.

    For questions about pests, diseases, and pathogens, the
    relevant entity is normally the object of the previous fact.

    For symptoms and management questions, it is normally
    the subject of the previous fact.
    """
    if not previous_result:
        return []

    facts = previous_result.get("facts", [])
    previous_intent = previous_result.get("intent")

    if previous_intent in {"pests", "diseases", "pathogens"}:
        field = "object"
    else:
        field = "subject"

    resolved = []

    for fact in facts:
        label = fact.get(field, "").strip().lower()

        for entity, uri in ENTITY_URIS.items():
            if label == get_label(uri).lower():
                if entity not in resolved:
                    resolved.append(entity)

    if resolved:
        return resolved

    # Fallback for previous results without usable facts.
    return previous_result.get("entities", [])


# ============================================================
# EVIDENCE AND PROVENANCE
# ============================================================

def get_claim_evidence(subject, predicate, obj):
    """Find claims supporting a graph relationship."""
    evidence = []

    for claim in graph.subjects(RDF.subject, subject):
        if (claim, RDF.predicate, predicate) not in graph:
            continue

        if (claim, RDF.object, obj) not in graph:
            continue

        for source in graph.objects(claim, AGRI.supportedBy):
            evidence.append({
                "source_title": str(
                    next(
                        graph.objects(source, AGRI.sourceTitle),
                        "Unknown source",
                    )
                ),
                "publisher": str(
                    next(
                        graph.objects(source, AGRI.publisher),
                        "Unknown publisher",
                    )
                ),
                "source_url": str(
                    next(graph.objects(source, AGRI.sourceURL), "")
                ),
                "publication_year": str(
                    next(graph.objects(source, AGRI.publicationYear), "")
                ),
                "geographic_scope": str(
                    next(graph.objects(source, AGRI.geographicScope), "")
                ),
                "evidence_description": str(
                    next(
                        graph.objects(claim, AGRI.evidenceDescription),
                        "",
                    )
                ),
                "evidence_section": str(
                    next(
                        graph.objects(claim, AGRI.evidenceSection),
                        "",
                    )
                ),
            })

    return evidence


def make_fact(subject, predicate, obj):
    """Build a structured fact with supporting evidence."""
    return {
        "subject": get_label(subject),
        "predicate": local_name(predicate),
        "object": get_label(obj),
        "relationship": (
            f"{get_label(subject)} "
            f"{local_name(predicate)} "
            f"{get_label(obj)}"
        ),
        "evidence": get_claim_evidence(subject, predicate, obj),
    }


# ============================================================
# DUPLICATE REMOVAL
# ============================================================

def deduplicate_facts(facts):
    """Remove duplicate relationships while preserving their order."""
    unique = []
    seen = set()

    for fact in facts:
        key = (
            fact["subject"],
            fact["predicate"],
            fact["object"],
        )

        if key not in seen:
            seen.add(key)
            unique.append(fact)

    return unique


# ============================================================
# FACT RETRIEVAL
# ============================================================

def retrieve_facts(entity, intent):
    """Retrieve facts for one entity and information category."""
    entity_uri = ENTITY_URIS.get(entity)
    predicate = RELATIONSHIPS.get(intent)

    if entity_uri is None or predicate is None:
        return []

    return [
        make_fact(entity_uri, predicate, obj)
        for obj in graph.objects(entity_uri, predicate)
    ]


def retrieve_from_multiple_entities(entities, intent):
    """Retrieve facts for all recognized entities."""
    facts = []

    for entity in entities:
        facts.extend(retrieve_facts(entity, intent))

    return deduplicate_facts(facts)


def retrieve_vector_facts(entities):
    """
    Retrieve pathogen-to-vector relationships.

    CBSD transmission is represented as:
        Disease -> Pathogen -> Vector
    """
    facts = []
    diseases = set()
    pathogens = set()

    for entity in entities:
        entity_uri = ENTITY_URIS.get(entity)

        if entity_uri is None:
            continue

        if entity == "CassavaBrownStreakDisease":
            diseases.add(entity_uri)

        for disease in graph.objects(entity_uri, AGRI.hasDisease):
            diseases.add(disease)

        if entity in {
            "CassavaBrownStreakVirus",
            "UgandanCassavaBrownStreakVirus",
        }:
            pathogens.add(entity_uri)

    for disease in diseases:
        pathogens.update(
            graph.objects(disease, AGRI.causedBy)
        )

    for pathogen in pathogens:
        for vector in graph.objects(pathogen, AGRI.transmittedBy):
            facts.append(
                make_fact(pathogen, AGRI.transmittedBy, vector)
            )

    return deduplicate_facts(facts)


# ============================================================
# MAIN QUESTION ANSWERING FUNCTION
# ============================================================

def answer_question(question, previous_result=None):
    """Retrieve graph facts relevant to a question."""

    unsupported = detect_unsupported_intent(question)

    if unsupported:
        return {
            "status": "unsupported",
            "message": (
                "The knowledge graph does not currently contain "
                "sufficient evidence to answer this type of question."
            ),
            "facts": [],
            "entities": [],
            "context_used": False,
        }

    entities = extract_entities(question)
    intent = extract_intent(question)
    context_used = False

    # Resolve follow-up questions.
    if not entities and previous_result:
        entities = resolve_context_entities(previous_result)
        context_used = bool(entities)

    if not entities:
        return {
            "status": "not_found",
            "message": (
                "I could not identify a supported crop, pest, "
                "disease, pathogen, or vector in your question."
            ),
            "facts": [],
            "entities": [],
            "context_used": context_used,
        }

    if intent is None:
        return {
            "status": "not_found",
            "message": (
                "I identified the entity, but could not determine "
                "what information you are requesting."
            ),
            "facts": [],
            "entities": entities,
            "context_used": context_used,
        }

    if intent == "vectors":
        facts = retrieve_vector_facts(entities)
    else:
        facts = retrieve_from_multiple_entities(entities, intent)

    facts = deduplicate_facts(facts)

    if not facts:
        return {
            "status": "not_found",
            "message": (
                "The knowledge graph does not contain a matching "
                "relationship for this question."
            ),
            "facts": [],
            "entities": entities,
            "intent": intent,
            "context_used": context_used,
        }

    return {
        "status": "success",
        "message": f"Retrieved {len(facts)} relevant facts.",
        "facts": facts,
        "entities": entities,
        "intent": intent,
        "context_used": context_used,
    }


# ============================================================
# TERMINAL OUTPUT
# ============================================================

def print_result(question, result):
    """Print a readable retrieval result."""
    print("\n" + "=" * 65)
    print(f"QUESTION: {question}")
    print("=" * 65)

    print(f"Status: {result['status']}")

    if result.get("context_used"):
        print("Context: Previous conversation context used.")

    if result.get("message"):
        print(f"Message: {result['message']}")

    for fact in result.get("facts", []):
        print(
            f"\n{fact['subject']} -> "
            f"{fact['predicate']} -> {fact['object']}"
        )

        for evidence in fact["evidence"]:
            print(f"  Source: {evidence['source_title']}")
            print(f"  Publisher: {evidence['publisher']}")
            print(f"  Year: {evidence['publication_year']}")
            print(f"  Evidence: {evidence['evidence_description']}")
            print(f"  Section: {evidence['evidence_section']}")
            print(f"  URL: {evidence['source_url']}")


# ============================================================
# MANUAL RETRIEVAL TESTS
# ============================================================

if __name__ == "__main__":

    test_questions = [
        "What pests affect maize?",
        "What symptoms does Fall Armyworm cause?",
        "How can farmers manage Fall Armyworm?",
        "What pests affect common beans?",
        "What symptoms does Bean Stem Maggot cause?",
        "How can farmers manage Bean Stem Maggot?",
        "What diseases affect cassava?",
        "What pathogens cause Cassava Brown Streak Disease?",
        "What symptoms does CBSD cause?",
        "What vectors transmit CBSD?",
        "What vectors transmit CBSV?",
        "What vectors transmit UCBSV?",
        "How can farmers manage CBSD?",
        "What chemical treatment controls CBSD?",
        "What is the economic impact of CBSD?",
        "What pests affect rice?",
    ]

    for question in test_questions:
        result = answer_question(question)
        print_result(question, result)

    # Conversational follow-up tests.
    print("\n\n" + "#" * 65)
    print("CONVERSATIONAL FOLLOW-UP TESTS")
    print("#" * 65)

    previous_result = answer_question("What pests affect maize?")
    follow_up = "What symptoms does it cause?"
    result = answer_question(follow_up, previous_result)
    print_result(follow_up, result)

    previous_result = answer_question("What pests affect common beans?")
    follow_up = "What symptoms does it cause?"
    result = answer_question(follow_up, previous_result)
    print_result(follow_up, result)
