
from rdflib import Literal
from knowledge_graph import load_knowledge_graph


graph = load_knowledge_graph()


# ============================================================
# PEST QUERIES
# ============================================================

def get_pests_for_crop(crop_name):
    query = """
    PREFIX agri: <http://example.org/agriculture#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?label
    WHERE {
        ?crop rdfs:label ?cropLabel ;
              agri:affectedBy ?pest .

        ?pest rdfs:label ?label .

        FILTER(LCASE(STR(?cropLabel)) = LCASE(STR(?name)))
    }
    """

    results = graph.query(
        query,
        initBindings={"name": Literal(crop_name)}
    )

    return sorted(str(row.label) for row in results)


def get_pest_symptoms(pest_name):
    query = """
    PREFIX agri: <http://example.org/agriculture#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?label
    WHERE {
        ?pest rdfs:label ?pestLabel ;
              agri:causesSymptom ?symptom .

        ?symptom rdfs:label ?label .

        FILTER(LCASE(STR(?pestLabel)) = LCASE(STR(?name)))
    }
    """

    results = graph.query(
        query,
        initBindings={"name": Literal(pest_name)}
    )

    return sorted(str(row.label) for row in results)


def get_management_practices(pest_name):
    query = """
    PREFIX agri: <http://example.org/agriculture#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?label
    WHERE {
        ?pest rdfs:label ?pestLabel ;
              agri:managedBy ?practice .

        ?practice rdfs:label ?label .

        FILTER(LCASE(STR(?pestLabel)) = LCASE(STR(?name)))
    }
    """

    results = graph.query(
        query,
        initBindings={"name": Literal(pest_name)}
    )

    return sorted(str(row.label) for row in results)


# ============================================================
# CASSAVA DISEASE QUERIES
# ============================================================

def get_diseases_for_crop(crop_name):
    query = """
    PREFIX agri: <http://example.org/agriculture#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?label
    WHERE {
        ?crop rdfs:label ?cropLabel ;
              agri:hasDisease ?disease .

        ?disease rdfs:label ?label .

        FILTER(LCASE(STR(?cropLabel)) = LCASE(STR(?name)))
    }
    """

    results = graph.query(
        query,
        initBindings={"name": Literal(crop_name)}
    )

    return sorted(str(row.label) for row in results)


def get_disease_pathogens(disease_name):
    query = """
    PREFIX agri: <http://example.org/agriculture#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?label
    WHERE {
        ?disease rdfs:label ?diseaseLabel ;
                 agri:causedBy ?pathogen .

        ?pathogen rdfs:label ?label .

        FILTER(LCASE(STR(?diseaseLabel)) = LCASE(STR(?name)))
    }
    """

    results = graph.query(
        query,
        initBindings={"name": Literal(disease_name)}
    )

    return sorted(str(row.label) for row in results)


def get_disease_symptoms(disease_name):
    query = """
    PREFIX agri: <http://example.org/agriculture#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?label
    WHERE {
        ?disease rdfs:label ?diseaseLabel ;
                 agri:causesSymptom ?symptom .

        ?symptom rdfs:label ?label .

        FILTER(LCASE(STR(?diseaseLabel)) = LCASE(STR(?name)))
    }
    """

    results = graph.query(
        query,
        initBindings={"name": Literal(disease_name)}
    )

    return sorted(str(row.label) for row in results)



def get_pathogen_vectors(pathogen_name):
    query = """
    PREFIX agri: <http://example.org/agriculture#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?label
    WHERE {
        ?pathogen rdfs:label ?pathogenLabel ;
                  agri:transmittedBy ?vector .

        ?vector rdfs:label ?label .

        FILTER(LCASE(STR(?pathogenLabel)) = LCASE(STR(?name)))
    }
    """

    results = graph.query(
        query,
        initBindings={"name": Literal(pathogen_name)}
    )

    return sorted(str(row.label) for row in results)



def get_disease_management(disease_name):
    query = """
    PREFIX agri: <http://example.org/agriculture#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT
        (COALESCE(STR(?practiceLabel),
                  REPLACE(STR(?practice), "^.*[#/]", "")) AS ?label)
    WHERE {
        ?disease rdfs:label ?diseaseLabel ;
                 agri:managedBy ?practice .

        OPTIONAL {
            ?practice rdfs:label ?practiceLabel .
        }

        FILTER(LCASE(STR(?diseaseLabel)) = LCASE(STR(?name)))
    }
    """

    results = graph.query(
        query,
        initBindings={"name": Literal(disease_name)}
    )

    return sorted(str(row.label) for row in results)


# ============================================================
# TEST SUITE
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("AGRICULTURAL KNOWLEDGE GRAPH: SPARQL TESTS")
    print("=" * 60)

    tests = [

        # MAIZE

        (
            "PESTS AFFECTING MAIZE",
            get_pests_for_crop("Maize"),
            ["Fall Armyworm"]
        ),

        (
            "FALL ARMYWORM SYMPTOMS",
            get_pest_symptoms("Fall Armyworm"),
            [
                "Leaf Damage",
                "Window-pane damage",
                "Frass in maize whorl"
            ]
        ),

        (
            "FALL ARMYWORM MANAGEMENT",
            get_management_practices("Fall Armyworm"),
            [
                "Field Monitoring",
                "Integrated Pest Management"
            ]
        ),

        # COMMON BEANS

        (
            "PESTS AFFECTING COMMON BEANS",
            get_pests_for_crop("Common Bean"),
            ["Bean Stem Maggot"]
        ),

        (
            "BEAN STEM MAGGOT SYMPTOMS",
            get_pest_symptoms("Bean Stem Maggot"),
            ["Stem Mining"]
        ),

        (
            "BEAN STEM MAGGOT MANAGEMENT",
            get_management_practices("Bean Stem Maggot"),
            [
                "Integrated Pest Management",
                "Resistant Varieties"
            ]
        ),

        # CASSAVA

        (
            "DISEASES AFFECTING CASSAVA",
            get_diseases_for_crop("Cassava"),
            ["Cassava Brown Streak Disease"]
        ),

        (
            "PATHOGENS CAUSING CBSD",
            get_disease_pathogens("Cassava Brown Streak Disease"),
            [
                "Cassava Brown Streak Virus",
                "Ugandan Cassava Brown Streak Virus"
            ]
        ),

        (
            "CASSAVA BROWN STREAK DISEASE SYMPTOMS",
            get_disease_symptoms("Cassava Brown Streak Disease"),
            [
                "Cassava Leaf Chlorosis",
                "Cassava Stem Lesions",
                "Cassava Root Necrosis",
                "Cassava Root Constrictions",
                "Cassava Root Discolouration"
            ]
        ),

        (
            "CBSV TRANSMITTED BY WHITEFLY",
            get_pathogen_vectors("Cassava Brown Streak Virus"),
            ["Whitefly"]
        ),

        (
            "UCBSV TRANSMITTED BY WHITEFLY",
            get_pathogen_vectors("Ugandan Cassava Brown Streak Virus"),
            ["Whitefly"]
        ),

        (
            "CASSAVA BROWN STREAK DISEASE MANAGEMENT",
            get_disease_management("Cassava Brown Streak Disease"),
            [
                "Clean Planting Material",
                "Removal of Infected Plants",
                "Tolerant Varieties"
            ]
        ),
    ]

    passed = 0

    for name, actual, expected in tests:

        expected = sorted(expected)
        success = actual == expected

        print(f"\n{name}:")
        print(f"Retrieved: {actual}")
        print(f"Expected:  {expected}")
        print("Result:", "PASS" if success else "FAIL")

        if success:
            passed += 1

    print("\n" + "=" * 60)
    print(f"SUMMARY: {passed}/{len(tests)} TESTS PASSED")
    print("=" * 60)

    if passed != len(tests):
        raise SystemExit(1)
