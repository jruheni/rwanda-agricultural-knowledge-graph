
import sys
from pathlib import Path

import streamlit as st


# ---------------------------------------------------------
# PROJECT SETUP
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from llm import generate_answer
from retrieval import answer_question


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Rwanda Agricultural Knowledge Assistant",
    page_icon="🌱",
    layout="centered",
)

st.title("Rwanda Agricultural Knowledge Assistant")

st.write(
    "Ask questions about crops, pests, diseases, symptoms, "
    "pathogens, vectors, and agricultural management practices."
)

st.caption(
    "Answers are generated using a local language model "
    "grounded in an RDF agricultural knowledge graph."
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "previous_result" not in st.session_state:
    st.session_state.previous_result = None

if "selected_question" not in st.session_state:
    st.session_state.selected_question = None


# ---------------------------------------------------------
# KNOWLEDGE COVERAGE
# ---------------------------------------------------------

st.subheader("Knowledge coverage")

st.write(
    "The assistant currently covers the following agricultural "
    "topics. Its answers are limited to information represented "
    "in the knowledge graph and its supporting sources."
)

with st.container(border=True):

    col1, col2, col3 = st.columns(3)

    col1.metric("Crops", "3")
    col2.metric("Pests", "2")
    col3.metric("Diseases", "1")

    st.divider()

    st.markdown("**Crops covered**")

    st.markdown(
        "- Maize (*Zea mays*)\n"
        "- Common beans (*Phaseolus vulgaris*)\n"
        "- Cassava (*Manihot esculenta*)"
    )

    st.markdown("**Pests and disease covered**")

    st.markdown(
        "- Fall Armyworm (*Spodoptera frugiperda*)\n"
        "- Bean Stem Maggot (*Ophiomyia* spp.)\n"
        "- Cassava Brown Streak Disease (CBSD)"
    )

    st.markdown("**CBSD pathogens and vector**")

    st.markdown(
        "- Cassava Brown Streak Virus (CBSV)\n"
        "- Ugandan Cassava Brown Streak Virus (UCBSV)\n"
        "- Whitefly (*Bemisia tabaci*)"
    )

    st.markdown("**Information available**")

    st.markdown(
        "- Pests affecting crops\n"
        "- Diseases affecting crops\n"
        "- Disease-causing pathogens\n"
        "- Symptoms and signs\n"
        "- Disease transmission and vectors\n"
        "- Agricultural management practices"
    )

    st.caption(
        "Scope reflects the current knowledge graph, not all "
        "agricultural knowledge about these crops."
    )


# ---------------------------------------------------------
# EXAMPLE QUESTIONS
# ---------------------------------------------------------

st.subheader("Try an example question")

st.write(
    "Select a question to send it directly to the assistant."
)


def select_question(question):
    """Store an example question for processing after rerun."""
    st.session_state.selected_question = question


col1, col2 = st.columns(2)

with col1:
    st.markdown("**Maize**")

    st.button(
        "What pests affect maize?",
        key="example_maize_pests",
        on_click=select_question,
        args=("What pests affect maize?",),
        use_container_width=True,
    )

    st.button(
        "What symptoms does Fall Armyworm cause?",
        key="example_maize_symptoms",
        on_click=select_question,
        args=("What symptoms does Fall Armyworm cause?",),
        use_container_width=True,
    )

    st.button(
        "How can farmers manage Fall Armyworm?",
        key="example_maize_management",
        on_click=select_question,
        args=("How can farmers manage Fall Armyworm?",),
        use_container_width=True,
    )

with col2:
    st.markdown("**Common beans**")

    st.button(
        "What pests affect common beans?",
        key="example_beans_pests",
        on_click=select_question,
        args=("What pests affect common beans?",),
        use_container_width=True,
    )

    st.button(
        "What symptoms does Bean Stem Maggot cause?",
        key="example_beans_symptoms",
        on_click=select_question,
        args=("What symptoms does Bean Stem Maggot cause?",),
        use_container_width=True,
    )

    st.button(
        "How can farmers manage Bean Stem Maggot?",
        key="example_beans_management",
        on_click=select_question,
        args=("How can farmers manage Bean Stem Maggot?",),
        use_container_width=True,
    )

st.markdown("**Cassava and CBSD**")

cassava_col1, cassava_col2 = st.columns(2)

with cassava_col1:
    st.button(
        "What diseases affect cassava?",
        key="example_cassava_diseases",
        on_click=select_question,
        args=("What diseases affect cassava?",),
        use_container_width=True,
    )

    st.button(
        "What pathogens cause CBSD?",
        key="example_cassava_pathogens",
        on_click=select_question,
        args=("What pathogens cause CBSD?",),
        use_container_width=True,
    )

    st.button(
        "What symptoms does CBSD cause?",
        key="example_cassava_symptoms",
        on_click=select_question,
        args=("What symptoms does CBSD cause?",),
        use_container_width=True,
    )

with cassava_col2:
    st.button(
        "What vectors transmit CBSD?",
        key="example_cassava_vectors",
        on_click=select_question,
        args=("What vectors transmit CBSD?",),
        use_container_width=True,
    )

    st.button(
        "How can farmers manage CBSD?",
        key="example_cassava_management",
        on_click=select_question,
        args=("How can farmers manage CBSD?",),
        use_container_width=True,
    )


st.divider()


# ---------------------------------------------------------
# EVIDENCE DISPLAY
# ---------------------------------------------------------

def display_evidence(facts):
    """
    Display retrieved graph facts and their source-specific
    supporting evidence.
    """

    if not facts:
        return

    with st.expander("View knowledge graph and source evidence"):

        for index, fact in enumerate(facts, start=1):

            st.markdown(
                f"**Fact {index}:** "
                f"{fact['subject']} "
                f"— *{fact['relationship']}* → "
                f"**{fact['object']}**"
            )

            evidence = fact.get("evidence", [])

            if not evidence:
                st.caption(
                    "No supporting source is currently recorded "
                    "for this fact."
                )
                continue

            for source_index, source in enumerate(evidence, start=1):

                st.markdown("---")

                source_title = source.get(
                    "source_title",
                    "Untitled source",
                )

                source_url = source.get("source_url")

                st.markdown(
                    f"**Supporting source {source_index}**"
                )

                if source_url:
                    st.markdown(
                        f"[{source_title}]({source_url})"
                    )
                else:
                    st.markdown(source_title)

                st.caption(
                    source.get("publisher")
                    or "Publisher not specified"
                )

                publication_year = (
                    source.get("publication_year")
                    or "Not specified"
                )

                geographic_scope = (
                    source.get("geographic_scope")
                    or "Not specified"
                )

                st.write(
                    f"**Publication year:** {publication_year}"
                )

                st.write(
                    f"**Geographic scope:** {geographic_scope}"
                )

                description = source.get("evidence_description")

                if description:
                    st.markdown("**Evidence description**")
                    st.write(description)

                section = source.get("evidence_section")

                if section:
                    st.caption(f"Relevant section: {section}")


# ---------------------------------------------------------
# DISPLAY PREVIOUS MESSAGES
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":
            display_evidence(message.get("facts", []))

            if message.get("context_used"):
                st.caption(
                    "Resolved using previous conversation context."
                )


# ---------------------------------------------------------
# QUESTION PROCESSING
# ---------------------------------------------------------

def process_question(question):
    """Run retrieval and LLM generation for a user question."""

    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Searching agricultural knowledge..."):

            retrieval_result = answer_question(
                question,
                previous_result=st.session_state.previous_result,
            )

        if retrieval_result["status"] == "success":

            with st.spinner("Generating answer..."):

                answer = generate_answer(
                    question,
                    retrieval_result=retrieval_result,
                )

            facts = retrieval_result["facts"]

            st.session_state.previous_result = retrieval_result

        else:

            answer = retrieval_result["message"]
            facts = []

        st.markdown(answer)

        display_evidence(facts)

        context_used = retrieval_result.get(
            "context_used",
            False,
        )

        if context_used:
            st.caption(
                "Resolved using previous conversation context."
            )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "facts": facts,
        "context_used": context_used,
    })


# ---------------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------------

typed_question = st.chat_input(
    "Ask an agricultural question..."
)

selected_question = st.session_state.selected_question

# Reset the selected example so it is only processed once.
st.session_state.selected_question = None

question = selected_question or typed_question

if question:
    process_question(question)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("About this project")

    st.write(
        "This prototype combines an RDF knowledge graph "
        "with a locally running language model to answer "
        "agricultural questions."
    )

    st.markdown("**Knowledge graph coverage**")

    st.write(
        "- 3 crops\n"
        "- 2 pests\n"
        "- 1 disease\n"
        "- 2 disease-causing viruses\n"
        "- 1 disease vector"
    )

    st.caption(
        "The assistant is currently a focused research "
        "prototype, not a comprehensive agricultural advisory system."
    )

    st.divider()

    st.markdown("**Technologies**")

    st.write(
        "- RDF / Turtle\n"
        "- RDFLib\n"
        "- SPARQL\n"
        "- SHACL\n"
        "- Ollama\n"
        "- Gemma 3 4B\n"
        "- Streamlit"
    )

    st.divider()

    if st.button("Clear conversation", use_container_width=True):

        st.session_state.messages = []
        st.session_state.previous_result = None
        st.session_state.selected_question = None

        st.rerun()
