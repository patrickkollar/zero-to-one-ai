import streamlit as st

from examples.run_job_needle_finder import run_finder
from src.config_loader import load_yaml
from src.deep_dive import deep_dive_job
from src.llm import OpenAIClient


st.set_page_config(
    page_title="Job Needle Finder",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 Job Needle Finder")
st.caption(
    "Find the opportunities that actually match the candidate."
)

current_tab, future_tab = st.tabs(
    ["Current State", "Future State"]
)


# ============================================================
# CURRENT STATE
# ============================================================

with current_tab:

    st.subheader("Working Prototype")

    col1, col2 = st.columns([3, 1])

    with col1:
        use_real_llm = st.checkbox(
            "Use real LLM reasoning",
            value=False,
        )

    with col2:
        run_button = st.button(
            "Run Job Needle Finder",
            type="primary",
            use_container_width=True,
        )

    if run_button:
        with st.spinner("Finding the needles..."):
            results, filtered_jobs = run_finder(
                use_real_llm=use_real_llm
            )

        st.session_state["results"] = results
        st.session_state["filtered_jobs"] = filtered_jobs
        st.session_state["deep_dive_index"] = None
        st.session_state["deep_dive"] = None

    if "results" in st.session_state:

        results = st.session_state["results"]
        filtered_jobs = st.session_state["filtered_jobs"]

        good_fits = [
            r for r in results
            if r["evaluation"].score >= 85
        ]

        possible_fits = [
            r for r in results
            if 70 <= r["evaluation"].score < 85
        ]

        poor_fits = [
            r for r in results
            if r["evaluation"].score < 70
        ]

        st.divider()

        st.subheader("Job Search Dashboard")

        summary_cols = st.columns(4)

        with summary_cols[0]:
            st.metric(
                "Jobs Analyzed",
                len(results),
            )

        with summary_cols[1]:
            st.metric(
                "Good Fits",
                len(good_fits),
            )

        with summary_cols[2]:
            st.metric(
                "Possible Fits",
                len(possible_fits),
            )

        with summary_cols[3]:
            st.metric(
                "Poor Fits",
                len(poor_fits),
            )

        st.divider()

        st.subheader("Opportunities")

        for index, result in enumerate(results, start=1):

            job = result["job"]
            evaluation = result["evaluation"]
            score = evaluation.score

            if score >= 85:
                fit = "GOOD FIT"
                apply_decision = "YES"
            elif score >= 70:
                fit = "POSSIBLE FIT"
                apply_decision = "MAYBE"
            else:
                fit = "POOR FIT"
                apply_decision = "NO"

            is_open = (
                st.session_state.get("deep_dive_index")
                == index - 1
            )

            with st.container(border=True):

                header_col, score_col = st.columns([5, 1])

                with header_col:
                    st.markdown(
                        f"### {index}. {job['title']}"
                    )
                    st.write(
                        f"**{job['company']}**"
                    )

                with score_col:
                    st.metric(
                        "Score",
                        f"{score:.1f}",
                    )

                fit_col, apply_col = st.columns(2)

                with fit_col:
                    st.markdown(
                        f"**FIT:** {fit}"
                    )

                with apply_col:
                    st.markdown(
                        f"**APPLY:** {apply_decision}"
                    )

                st.markdown("**Why**")

                if evaluation.strengths:
                    st.write(
                        evaluation.strengths[0]
                    )
                else:
                    st.write(
                        evaluation.reasoning
                    )

                if evaluation.concerns:
                    st.markdown(
                        "**Where it doesn't fit**"
                    )

                    for concern in evaluation.concerns[:2]:
                        st.write(
                            f"- {concern}"
                        )

                button_label = (
                    "Close Deep Dive ↑"
                    if is_open
                    else "Deep Dive →"
                )

                if st.button(
                    button_label,
                    key=f"deep_dive_{index}",
                ):

                    if is_open:

                        st.session_state[
                            "deep_dive_index"
                        ] = None

                        st.session_state[
                            "deep_dive"
                        ] = None

                    else:

                        st.session_state[
                            "deep_dive_index"
                        ] = index - 1

                        with st.spinner(
                            "Analyzing this opportunity..."
                        ):

                            candidate_profile = load_yaml(
                                "config/candidate_profile.example.yaml"
                            )

                            llm_client = OpenAIClient(
                                model="gpt-5.6-luna"
                            )

                            deep_dive = deep_dive_job(
                                job=job,
                                candidate_profile=candidate_profile,
                                initial_evaluation=evaluation,
                                llm_client=llm_client,
                            )

                            st.session_state[
                                "deep_dive"
                            ] = deep_dive

                    st.rerun()

                if is_open:

                    deep_dive = st.session_state.get(
                        "deep_dive"
                    )

                    if deep_dive is not None:

                        st.divider()

                        st.markdown("## Deep Dive")

                        st.markdown(
                            "### Why this is a fit"
                        )

                        for item in deep_dive.why_it_fits:
                            st.write(
                                f"- {item}"
                            )

                        st.markdown(
                            "### Where it doesn't fit"
                        )

                        for item in deep_dive.where_it_doesnt_fit:
                            st.write(
                                f"- {item}"
                            )

                        st.markdown(
                            "### What to investigate"
                        )

                        for item in deep_dive.investigate:
                            st.write(
                                f"- {item}"
                            )

                        st.markdown(
                            "### Bottom line"
                        )

                        st.write(
                            deep_dive.bottom_line
                        )

        if filtered_jobs:

            st.divider()

            with st.expander(
                f"Filtered Out ({len(filtered_jobs)})"
            ):

                for item in filtered_jobs:

                    job = item["job"]

                    st.write(
                        f"**{job['title']} — "
                        f"{job['company']}**"
                    )

                    st.caption(
                        f"Reason: {item['reason']}"
                    )


# ============================================================
# FUTURE STATE
# ============================================================

with future_tab:

    st.subheader("Future State")
    st.caption(
        "Conceptual mock-up — these capabilities are not "
        "implemented yet."
    )

    st.info(
        "The current prototype answers: "
        "\"Is this job worth my time?\" "
        "The future version understands the candidate, "
        "their career goals and how those goals evolve."
    )

    st.divider()

    st.markdown("### Candidate Profile")

    profile_col1, profile_col2 = st.columns(2)

    with profile_col1:

        st.markdown("**Career Level**")

        st.selectbox(
            "Career Level",
            [
                "Senior Manager",
                "Director",
                "Senior Manager / Director",
            ],
            index=2,
            disabled=True,
            label_visibility="collapsed",
        )

        st.markdown("**Target Functions**")

        st.multiselect(
            "Target Functions",
            [
                "Business Operations",
                "Customer Operations",
                "Customer Success Operations",
                "Revenue Operations",
                "Order Management",
                "Quote-to-Cash",
                "Transformation",
            ],
            default=[
                "Business Operations",
                "Customer Operations",
                "Revenue Operations",
                "Transformation",
            ],
            disabled=True,
            label_visibility="collapsed",
        )

    with profile_col2:

        st.markdown("**Compensation Target**")

        st.slider(
            "Compensation",
            100,
            250,
            (160, 200),
            step=5,
            disabled=True,
            label_visibility="collapsed",
        )

        st.markdown("**Work Model**")

        st.radio(
            "Work Model",
            [
                "Remote preferred",
                "Hybrid",
                "On-site",
            ],
            index=0,
            disabled=True,
            label_visibility="collapsed",
        )

    st.divider()

    st.markdown("### Reasoning Engine")

    engine_col1, engine_col2 = st.columns(2)

    with engine_col1:

        st.markdown("**LLM**")

        st.selectbox(
            "LLM",
            [
                "GPT-5.6 Luna",
                "GPT-5.6 Sol",
                "Other model",
            ],
            disabled=True,
            label_visibility="collapsed",
        )

    with engine_col2:

        st.markdown("**Reasoning Controls**")

        st.checkbox(
            "Structured reasoning",
            value=True,
            disabled=True,
        )

        st.checkbox(
            "Candidate career memory",
            value=True,
            disabled=True,
        )

        st.checkbox(
            "Feedback learning",
            value=False,
            disabled=True,
        )

    st.divider()

    st.markdown("### Future Capabilities")

    capability_cols = st.columns(3)

    with capability_cols[0]:

        with st.container(border=True):

            st.markdown("#### Job Sources")

            st.write(
                "Expand beyond the current job dataset "
                "to real job sources and company career sites."
            )

            st.caption(
                "LinkedIn • Indeed • Company Sites"
            )

    with capability_cols[1]:

        with st.container(border=True):

            st.markdown("#### Career Memory")

            st.write(
                "Maintain a structured understanding of "
                "experience, accomplishments, projects "
                "and career preferences."
            )

            st.caption(
                "Experience • Projects • Capabilities"
            )

    with capability_cols[2]:

        with st.container(border=True):

            st.markdown("#### Feedback Loop")

            st.write(
                "Learn from decisions and feedback to "
                "improve future opportunity evaluation."
            )

            st.caption(
                "Applied • Passed • Interviewed • Rejected"
            )

    st.divider()

    st.markdown("### Where This Is Going")

    st.write(
        "Job Needle Finder is the first step toward an "
        "AI operating partner for career decisions — "
        "one that understands both the opportunity and "
        "the person evaluating it."
    )