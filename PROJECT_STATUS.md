# Project Status: Rwanda Agricultural Knowledge Assistant

**Last updated:** 14 November 2026
**Status:** Working research prototype
**Primary objective:** Demonstrate knowledge graph construction, semantic retrieval, evidence provenance, validation, and LLM integration for agricultural question answering in Rwanda.

---

## 1. Project Summary

The Rwanda Agricultural Knowledge Assistant is a knowledge-graph-grounded question-answering system.

It combines:

- An RDF/OWL agricultural ontology.
- An RDF knowledge graph containing agricultural facts.
- SPARQL-based retrieval using RDFLib.
- Claim-level source provenance.
- SHACL validation.
- Local LLM inference using Gemma 3 4B through Ollama.
- A Streamlit conversational interface.

The current knowledge domain covers maize and common beans, their associated pests, symptoms, and management practices.

The project is intended to demonstrate practical experience in knowledge representation, semantic technologies, retrieval-augmented generation, and responsible AI.

## 2. Development Environment

| Component           | Current Setup      |
| ------------------- | ------------------ |
| Operating system    | Windows            |
| IDE                 | Visual Studio Code |
| Shell               | PowerShell         |
| Python              | 3.13               |
| Virtual environment | `.venv`            |
| RDF library         | RDFLib             |
| Validation          | pySHACL            |
| LLM runtime         | Ollama             |
| LLM                 | Gemma 3 4B         |
| Interface           | Streamlit          |
| Main language       | Python             |
| Data format         | RDF/Turtle         |

### Environment Setup

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install rdflib streamlit requests pandas pytest pyshacl
```

Ensure Ollama is running and the model is available:

```powershell
ollama pull gemma3:4b
```

## 3. Completed Components

### 3.1 Ontology Design

**File:** `ontology/agriculture.ttl`

Implemented:

- Crop
- Pest
- Symptom
- ManagementPractice
- SoilCondition
- ClimateCondition
- Region
- Source
- Claim

Defined object properties:

- `affectedBy`
- `causesSymptom`
- `managedBy`
- `requiresSoilCondition`
- `suitableUnder`
- `observedIn`
- `supportedBy`
- `hasClaim`

Defined source metadata and claim-level evidence properties.

**Status:** Implemented.

### 3.2 Knowledge Graph Construction

**File:** `data/processed/agriculture.ttl`

Current agricultural coverage:

**Maize**

- Fall Armyworm
- Leaf Damage
- Window-pane damage
- Frass in maize whorl
- Field Monitoring
- Integrated Pest Management

**Common beans**

- Bean Stem Maggot
- Stem Mining
- Integrated Pest Management
- Resistant Varieties

The graph includes four source records:

1. Rwanda MINAGRI government publication.
2. FAO/CABI Fall Armyworm field handbook (2019).
3. World Bank Rwanda Agricultural Sector Risk Assessment (2015).
4. Rwanda Journal of Agricultural Sciences article (2024).

Claim-level provenance is represented through RDF claim resources, including source-specific evidence descriptions.

**Current graph statistics:**

- 318 RDF triples.
- 13 claims.
- 4 source records.

**Status:** Implemented.

### 3.3 Knowledge Graph Loading

**File:** `src/knowledge_graph.py`

Implemented:

- Loading ontology and processed agricultural data.
- RDFLib graph initialization.
- Agricultural namespace definition.
- Entity retrieval helper functions.

**Status:** Implemented.

### 3.4 SPARQL Retrieval

**File:** `src/test_queries.py`

Implemented and tested queries for:

- Pests affecting maize.
- Fall Armyworm symptoms.
- Fall Armyworm management.
- Pests affecting common beans.
- Bean Stem Maggot symptoms.
- Bean Stem Maggot management.

**Latest result:** 6/6 tests passed.

**Status:** Implemented.

### 3.5 Question Retrieval and Context Management

**File:** `src/retrieval.py`

Implemented:

- Natural-language question interpretation.
- Crop and pest recognition.
- Agricultural relationship retrieval.
- Source and evidence retrieval.
- Unsupported-question handling.
- Unknown-entity handling.
- Conversational follow-up resolution.

Tested conversational examples include:

- Asking what pests affect maize, followed by asking what symptoms they cause.
- Asking what pests affect common beans, followed by asking what symptoms they cause.

The retrieval system also declines unsupported pesticide recommendations and unsupported yield-loss statistics.

**Status:** Implemented.

### 3.6 LLM Integration

**File:** `src/llm.py`

Implemented:

- Ollama API integration.
- Gemma 3 4B inference.
- Formatting retrieved graph facts and supporting evidence.
- Grounded answer generation.
- Instructions against inventing unsupported facts, statistics, or recommendations.
- Separation of generated answers from source citation display.

The LLM receives retrieved knowledge rather than independently searching for agricultural facts.

**Status:** Implemented.

### 3.7 Streamlit Application

**File:** `app.py`

Implemented:

- Conversational chat interface.
- Chat history.
- Follow-up question context.
- LLM-generated answers.
- Retrieved fact display.
- Source links and source metadata.
- Source-specific evidence descriptions.
- Technology information in the sidebar.

The application has been run and manually tested successfully.

**Status:** Implemented.

### 3.8 SHACL Validation

**Files:**

- `validation/agriculture_shapes.ttl`
- `src/validate_graph.py`

Implemented constraints for:

- Claim subject, predicate, and object cardinality.
- Required claim descriptions.
- Required evidence descriptions.
- Supporting source requirements.
- Required source metadata.
- Source URL datatype.

Additional consistency checks verify that each reified claim corresponds to an asserted graph relationship.

**Latest result:**

- SHACL validation: Passed.
- Claims identified: 13.
- Consistent claims: 13.
- Inconsistent claims: 0.

**Status:** Implemented.

### 3.9 Retrieval Evaluation

**File:** `src/evaluation.py`

Implemented:

- Exact triple precision.
- Exact triple recall.
- Exact triple F1.
- Evidence coverage.
- Unsupported-question tests.
- Conversational context tests.

**Latest results:**

| Metric                  | Result |
| ----------------------- | -----: |
| Retrieval tests         |    6/6 |
| Expected facts          |     10 |
| Correct facts retrieved |     10 |
| Precision               |  1.000 |
| Recall                  |  1.000 |
| F1                      |  1.000 |
| Evidence coverage       |  1.000 |
| Unsupported tests       |    2/2 |
| Context tests           |    2/2 |

**Status:** Implemented; requires broader evaluation.

### 3.10 LLM Evaluation

**File:** `src/llm_evaluation.py`

Implemented:

- Expected-concept coverage.
- Maize and common bean answer evaluation.
- Follow-up question evaluation.
- Unknown-crop handling.
- Unsupported pesticide recommendation tests.
- Unsupported yield-statistic tests.
- Prompt-injection-style retrieval tests.
- Manual review of generated-answer grounding.

**Latest results:**

- Standard answer tests: 6/6 passed.
- Expected concepts covered: 10/10.
- Concept coverage: 1.000.
- Context tests: 2/2 passed.
- Retrieval robustness tests: 4/4 passed.
- Generation grounding cases: 6 manually reviewed.

All six manually reviewed generation cases avoided introducing unsupported recommendations or statistics. One response was grammatically awkward despite remaining grounded.

**Status:** Implemented; requires more rigorous testing.

---

## 4. Current Project Structure

```text
rwanda-agricultural-knowledge-graph/
│
├── app.py
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
├── src/
│   ├── knowledge_graph.py
│   ├── retrieval.py
│   ├── llm.py
│   ├── test_queries.py
│   ├── evaluation.py
│   ├── llm_evaluation.py
│   └── validate_graph.py
│
└── .venv/
```

This is the expected structure based on the current implementation. Update it if additional files are introduced.

## 5. Known Limitations

### Knowledge Coverage

- Only two crops are currently represented.
- The number of pests, symptoms, and management practices is limited.
- Some ontology classes and properties are defined but not yet populated with data.
- Source evidence descriptions are paraphrased and some evidence-section labels are approximate.
- Exact passages, page numbers, and section references need further verification.

### Retrieval

- Natural-language interpretation relies on manually defined intent and entity recognition logic.
- The current system is not a general-purpose agricultural question-answering engine.
- The small dataset limits the range of questions that can be answered.

### LLM

- The model can produce awkward or incomplete responses.
- Grounding instructions reduce unsupported output but do not guarantee factual correctness.
- The current evaluation does not establish resistance to prompt injection.

### Evaluation

- Evaluation questions are manually curated.
- The test set is small.
- Concept coverage is a lexical metric, not a comprehensive semantic evaluation.
- There is no independent expert-reviewed benchmark yet.
- Perfect scores on the current test set should not be interpreted as general performance guarantees.

### Data Quality

- Source descriptions and provenance need further verification.
- The graph needs broader coverage and more detailed evidence.
- Agricultural recommendations should not be expanded without reliable supporting sources.

---

## 6. Next Development Priorities

The following tasks are proposed, in order of priority.

### Priority 1: Research Documentation

- [ ] Verify source evidence descriptions against the original publications.
- [ ] Improve source attribution and evidence traceability.
- [ ] Document the ontology design decisions.
- [ ] Prepare a technical report describing the architecture and implementation.
- [ ] Document evaluation methodology and limitations.

### Priority 2: Retrieval Improvements

- [ ] Expand natural-language question coverage.
- [ ] Improve entity recognition and relation identification.
- [ ] Test ambiguous questions and alternative phrasings.
- [ ] Investigate more flexible SPARQL query generation or mapping.

### Priority 3: Evaluation Improvements

- [ ] Develop a larger question-and-answer test set.
- [ ] Add questions with paraphrased wording.
- [ ] Add negative and ambiguous examples.
- [ ] Introduce independent manual review of factual correctness.
- [ ] Compare graph-grounded answers with LLM-only answers.
- [ ] Evaluate source attribution accuracy.

### Priority 4: Knowledge Graph Expansion

- [ ] Add more crops relevant to Rwanda.
- [ ] Add additional pests and crop diseases.
- [ ] Expand soil, climate, and regional information.
- [ ] Add more authoritative agricultural sources.
- [ ] Improve source-specific evidence references.

### Priority 5: Research Presentation

- [ ] Prepare architecture and ontology diagrams.
- [ ] Document technical challenges and design decisions.
- [ ] Prepare a demonstration of the application.
- [ ] Publish the project repository with reproducible setup instructions.

---

## 7. Important Commands

Run the application:

```powershell
streamlit run app.py
```

Run SPARQL query tests:

```powershell
python src/test_queries.py
```

Run retrieval evaluation:

```powershell
python src/evaluation.py
```

Run LLM evaluation:

```powershell
python src/llm_evaluation.py
```

Run SHACL and graph consistency validation:

```powershell
python src/validate_graph.py
```

---

## 8. Development Guidelines

When continuing development:

1. Preserve the existing ontology and RDF namespace conventions.
2. Keep source provenance attached to individual claims.
3. Do not add unsupported agricultural recommendations.
4. Run graph validation after modifying ontology or data.
5. Run retrieval tests after modifying retrieval logic.
6. Run LLM evaluation after modifying prompts or answer generation.
7. Distinguish measured results from assumptions and qualitative observations.
8. Prefer complete, reproducible changes over undocumented manual edits.

---

## 9. Research Positioning

The project investigates how knowledge graphs can complement LLMs in specialized, context-sensitive question-answering applications.

Its central technical idea is to use an explicit knowledge representation and source-linked claims as the factual retrieval layer, while delegating natural-language response generation to an LLM.

Agriculture in Rwanda serves as the initial domain for exploring this approach.

The current implementation establishes a working prototype. Further work should focus on evidence quality, retrieval generalization, independent evaluation, and broader knowledge coverage before making claims about reliability in real-world agricultural decision-making.

**Last verified development state:** 14 November 2026
