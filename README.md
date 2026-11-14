# Rwanda Agricultural Knowledge Assistant

A knowledge-graph-grounded question-answering system for agricultural information in Rwanda. The project combines Semantic Web technologies, structured agricultural knowledge, source provenance, and a locally hosted Large Language Model (LLM) to provide context-sensitive answers to agricultural questions.

## 1. Project Overview

Agricultural information is distributed across government publications, research papers, and technical field guides. Although these sources contain valuable information, retrieving specific facts and understanding relationships between agricultural concepts can be difficult.

This project explores how knowledge graphs can make agricultural information more structured, interpretable, and accessible.

The Rwanda Agricultural Knowledge Assistant allows users to ask natural-language questions about crops, pests, diseases, symptoms, pathogens, vectors, and management practices. It retrieves relevant relationships from an RDF knowledge graph and uses a locally hosted LLM to generate readable answers grounded in the retrieved information.

### Current Knowledge Domain

The prototype covers three crops:

- **Maize (*Zea mays*)**
  - Fall Armyworm (*Spodoptera frugiperda*)
  - Associated symptoms and management practices

- **Common bean (*Phaseolus vulgaris*)**
  - Bean Stem Maggot (*Ophiomyia* spp.)
  - Associated symptoms and management practices

- **Cassava (*Manihot esculenta*)**
  - Cassava Brown Streak Disease (CBSD)
  - Associated viruses: Cassava brown streak virus (CBSV) and Ugandan cassava brown streak virus (UCBSV)
  - Whitefly (*Bemisia tabaci*) as a vector
  - Disease symptoms and management practices

The knowledge base incorporates information from Rwandan government publications, international agricultural organizations, and agricultural research.

## 2. Project Objectives

The project demonstrates:

1. **Ontology design:** Representing agricultural concepts and their relationships using RDF/OWL.
2. **Knowledge graph construction:** Encoding crop, pest, disease, pathogen, symptom, vector, and management relationships as structured RDF data.
3. **Semantic querying:** Retrieving information through SPARQL.
4. **Evidence provenance:** Linking graph claims to supporting sources and source-specific evidence descriptions.
5. **Knowledge validation:** Applying SHACL constraints and claim-to-graph consistency checks.
6. **LLM integration:** Using a locally hosted language model to generate natural-language answers grounded in retrieved graph information.
7. **Conversational retrieval:** Resolving follow-up questions using conversational context.
8. **Evaluation:** Testing retrieval, concept coverage, unsupported-question handling, conversational context, and answer grounding.

## 3. System Architecture

The application follows a knowledge-graph-grounded retrieval-augmented generation approach. The knowledge graph provides the factual foundation for the LLM rather than relying on the model's pretrained knowledge alone.

```text
                 User Question
                       |
                       v
              Streamlit Interface
                       |
                       v
             Question Understanding
                       |
                       v
              Knowledge Retrieval
                       |
                       v
                 SPARQL Queries
                       |
                       v
              RDF Agricultural Graph
                       |
                       v
              Retrieved Facts
              + Source Evidence
                       |
                       v
                 Ollama / Gemma 3
                       |
                       v
              Grounded Answer
                       |
                       v
              Answer + Evidence
```

### Main Components

| Component | Technology | Purpose |
|---|---|---|
| Ontology | RDF/OWL, Turtle | Defines agricultural concepts and relationships |
| Knowledge graph | RDFLib | Stores and loads structured agricultural facts |
| Retrieval | SPARQL | Queries relationships between agricultural entities |
| Validation | SHACL, pySHACL | Checks graph structure and data constraints |
| LLM | Gemma 3 4B | Generates natural-language answers |
| Local inference | Ollama | Hosts and serves the language model |
| Interface | Streamlit | Provides an interactive conversational interface |
| Evaluation | Python | Tests retrieval and generated-answer behaviour |

## 4. Knowledge Representation

The ontology defines the main concepts and relationships in the agricultural domain.

### Core Classes

The ontology includes:

- `Crop`
- `Pest`
- `Disease`
- `Pathogen`
- `Vector`
- `Symptom`
- `ManagementPractice`
- `SoilCondition`
- `ClimateCondition`
- `Region`
- `Source`
- `Claim`

### Core Relationships

Examples of the graph's object properties include:

- `affectedBy`: connects a crop to a pest.
- `hasDisease`: connects a crop to a disease.
- `causesSymptom`: connects a pest or disease to an associated symptom.
- `managedBy`: connects a pest or disease to a management practice.
- `causedBy`: connects a disease to its associated pathogen.
- `transmittedBy`: connects a pathogen to its vector.
- `requiresSoilCondition`: represents soil requirements.
- `suitableUnder`: represents suitable environmental conditions.
- `observedIn`: connects an entity to a geographical region.
- `supportedBy`: links a claim to its supporting source.
- `hasClaim`: links a source to claims derived from it.

For CBSD, the graph represents disease transmission through the pathogen relationships: CBSD is caused by CBSV and UCBSV, and both viruses are associated with transmission by whiteflies. This preserves the distinction between the disease and its causative viruses.

### Evidence and Provenance

The graph does not only store agricultural relationships. It also represents the claims and sources supporting those relationships.

Claims include:

- RDF subject, predicate, and object.
- A human-readable claim description.
- A source-specific evidence description.
- A relevant evidence section.
- A link to the supporting source.

Source records also include metadata such as title, publisher, URL, publication year, geographic scope, language, source type, and access date where available.

This allows the application to present supporting evidence alongside retrieved facts.

### Current Graph Statistics

| Measure | Count |
|---|---:|
| RDF triples loaded (ontology and data) | 609 |
| Claims represented | 32 |
| Crops | 3 |
| Pests | 2 |
| Diseases | 1 |

These figures describe the current prototype and are not measures of domain completeness.

## 5. Data Sources

The knowledge graph draws on publications from government institutions, international agricultural organizations, and research.

### Maize and Fall Armyworm

1. **Ministry of Agriculture and Animal Resources (MINAGRI), Rwanda** — Government publication on efforts to contain Fall Armyworm.  
   https://www.minagri.gov.rw/updates/news-details/government-intensifies-efforts-to-contain-fall-armyworms

2. **FAO and CABI (2019)** — *Fall Armyworm Field Handbook: Identification and Management*.  
   https://site.cabi.org/wp-content/uploads/FAW-pocket-guide.pdf

3. **World Bank Group (2015)** — *Rwanda Agricultural Sector Risk Assessment*.  
   https://documents1.worldbank.org/curated/en/525111468180254519/pdf/96290-WP-P148140-Box393232B-PUBLIC-TAP-Rwanda-ASRA-WEB-10062015.pdf

### Common Bean and Bean Stem Maggot

4. **Rwanda Journal of Agricultural Sciences (2024)** — *Effect of Imidacloprid Gaucho-Seed Coating on Mosaic Virus Transmission and the Dynamics of the Main Insect Pests of Common Bean (Phaseolus vulgaris L.) Cultivation in Rwanda*.  
   https://www.ajol.info/index.php/rjeas/article/view/266782

### Cassava and Cassava Brown Streak Disease

5. **Plant Pathology (2018)** — *Cassava brown streak disease in Rwanda, the associated viruses and disease phenotypes*.  
   https://pmc.ncbi.nlm.nih.gov/articles/PMC5832305/

6. **Ministry of Agriculture and Animal Resources (MINAGRI), Rwanda (2018–2019)** — *MINAGRI Annual Report 2018–2019*.  
   https://www.minagri.gov.rw/fileadmin/user_upload/Minagri/Publications/Annual_Reports/Minagri_Annual_Report_2018-19.pdf

7. **FAO** — *Cassava Farmer Field Schools Handbook*.  
   https://www.fao.org/4/i3447e/i3447e.pdf

8. **Ministry of Agriculture and Animal Resources (MINAGRI), Rwanda (2016)** — Publication on the distribution of new cassava varieties in Southern Province.  
   https://www.minagri.gov.rw/updates/news-details/farmers-and-local-officials-commit-to-ensure-fair-distribution-of-new-cassava-varieties-in-southern-province

The implementation uses selected information from these sources. It is not intended to represent an exhaustive agricultural knowledge base.

## 6. Installation and Setup

### Prerequisites

- Python 3.13
- Git
- Ollama
- Gemma 3 4B model

### Clone the Repository

```powershell
git clone https://github.com/jruheni/rwanda-agricultural-knowledge-graph.git
cd rwanda-agricultural-knowledge-graph
```

### Create a Virtual Environment

```powershell
py -3.13 -m venv .venv
.venv\Scripts\Activate.ps1
```

### Install Dependencies

```powershell
pip install -r requirements.txt
```

### Install and Start Ollama

Install Ollama from:

https://ollama.com/

Download the model:

```powershell
ollama pull gemma3:4b
```

Make sure Ollama is running before starting the application.

## 7. Running the Application

From the project root, activate the virtual environment and run:

```powershell
streamlit run app.py
```

The application opens in a browser.

The interface includes a knowledge coverage overview and example questions that users can select to explore the available information.

Example questions include:

**Maize**
- What pests affect maize?
- What symptoms does Fall Armyworm cause?
- How is Fall Armyworm managed?

**Common beans**
- What pests affect common beans?
- What are the symptoms of Bean Stem Maggot infestation?
- What management practices are used against Bean Stem Maggot?

**Cassava**
- What diseases affect cassava?
- Which pathogens cause Cassava Brown Streak Disease?
- What symptoms does CBSD cause?
- Which vectors transmit CBSV and UCBSV?
- How is CBSD managed?

The interface displays generated answers alongside supporting graph facts and source evidence. Follow-up questions can use the preceding conversational context.

## 8. Knowledge Graph Validation

The project uses SHACL to validate structural requirements for claims and sources.

Validation checks include:

- Each claim has exactly one subject, predicate, and object.
- Each claim has a description and evidence description.
- Each claim references at least one supporting source.
- Each source has a title, publisher, and URL.
- Each claim corresponds to an asserted relationship in the knowledge graph.

Run validation with:

```powershell
python src/validate_graph.py
```

### Verified Validation Results

| Check | Result |
|---|---:|
| RDF triples loaded | 609 |
| SHACL shape triples | 45 |
| Claims identified | 32 |
| Consistent claims | 32 |
| Inconsistent claims | 0 |
| SHACL validation | Conforms |

These results demonstrate that the current graph satisfies the implemented validation constraints. They do not establish the completeness or correctness of every agricultural fact.

## 9. Evaluation

The project includes separate tests for graph querying, retrieval behaviour, and LLM answer generation.

### SPARQL Query Tests

Run:

```powershell
python src/test_queries.py
```

The test suite checks the retrieval of agricultural relationships across the three crops, including pests, symptoms, management practices, CBSD pathogens, and pathogen-level vectors.

**Latest verified result: 12/12 tests passed.**

### LLM Answer Evaluation

Run:

```powershell
python src/llm_evaluation.py
```

The evaluation examines:

- Coverage of expected concepts in generated answers.
- Context-sensitive follow-up responses.
- Handling of unsupported questions.
- Whether generated responses avoid unsupported recommendations and statistics.
- Responses to prompt-injection-style questions.

### Verified LLM Evaluation Results

| Metric | Result |
|---|---:|
| Standard answer tests | 12/12 |
| Expected concepts matched | 23/23 |
| Concept coverage | 1.000 |
| Conversational context tests | 3/3 |
| Retrieval robustness tests | 7/7 |
| Grounding challenge cases reviewed | 9 |

The nine grounding challenge cases involve manual review of generated responses. They are not an automated measure of factual correctness or adversarial security.

### Evaluation Limitations

The results are based on a small, manually curated set of questions and expected concepts.

Concept coverage is a lexical metric rather than a comprehensive measure of semantic correctness. Passing the tests demonstrates proof-of-concept functionality, not generalization to unseen agricultural questions or guaranteed resistance to prompt injection.

## 10. Project Structure

```text
rwanda-agricultural-knowledge-graph/
│
├── app.py
├── requirements.txt
├── README.md
├── PROJECT_STATUS.md
│
├── ontology/
│   └── agriculture.ttl
│
├── data/
│   └── processed/
│       └── agriculture.ttl
│
├── validation/
│   └── agriculture_shapes.ttl
│
└── src/
    ├── knowledge_graph.py
    ├── retrieval.py
    ├── llm.py
    ├── test_queries.py
    ├── evaluation.py
    ├── llm_evaluation.py
    └── validate_graph.py
```

## 11. Limitations and Future Work

The current implementation is a research prototype with a deliberately limited knowledge domain.

Potential extensions include:

- Expanding the graph to additional crops, pests, diseases, and regions in Rwanda.
- Incorporating more verified agricultural publications and datasets.
- Improving evidence extraction and recording precise source sections and page references.
- Extending ontology coverage to soil, climate, and regional agricultural conditions.
- Improving entity linking and natural-language question interpretation.
- Evaluating retrieval and answer quality against a larger, independently reviewed benchmark.
- Comparing graph-grounded answers with conventional LLM-only responses.
- Investigating the reliability of source attribution and hallucination prevention.

These are potential research directions rather than features currently implemented.

## 12. Research Motivation

This project explores the intersection of knowledge representation, information retrieval, and large language models.

It demonstrates how structured domain knowledge, semantic relationships, validation constraints, and explicit evidence provenance can complement generative language models.

The broader motivation is to investigate how knowledge graphs can support more transparent and context-sensitive AI systems in specialized, resource-constrained settings, using agriculture in Rwanda as an initial application domain.

---

**Project status:** Research prototype  
**Primary domain:** Rwandan agriculture  
**Core approach:** Knowledge graph-grounded question answering  
**Knowledge representation:** RDF/OWL and SPARQL  
**Validation:** SHACL and claim consistency checks  
**Language model:** Gemma 3 4B via Ollama  
**Interface:** Streamlit