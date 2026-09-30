import streamlit as st

from examples.run_job_needle_finder import run_finder


st.set_page_config(
    page_title="Job Needle Finder",
    page_icon="🎯",
    layout="wide",
)


# ---------------------------------------------------------
# Page Header
# ---------------------------------------------------------

st.title("🎯 Job Needle Finder")
st.caption(
    "Find the opportunities that actually match the candidate."
)

st.divider()


# ---------------------------------------------------------
# Controls
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Run Finder
# ---------------------------------------------------------

if run_button:

    with st.spinner("Finding the needles..."):

        results, filtered_jobs = run_finder(
            use_real_llm=use_real_llm
        )

    st.session_state["results"] = results
    st.session_state["filtered_jobs"] = filtered_jobs
    st.session_state["deep_dive_index"] = None


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

if "results" in st.session_state:

    results = st.session_state["results"]
    filtered_jobs = st.session_state["filtered_jobs"]

    # -----------------------------------------------------
    # Summary
    # -----------------------------------------------------

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

    st.subheader("Job Search Dashboard")

    summary_cols = st.columns(4)

    with summary_cols[0]:
        st.metric("Jobs Analyzed", len(results))

    with summary_cols[1]:
        st.metric("Good Fits", len(good_fits))

    with summary_cols[2]:
        st.metric("Possible Fits", len(possible_fits))

    with summary_cols[3]:
        st.metric("Poor Fits", len(poor_fits))

    st.divider()

    # -----------------------------------------------------
    # Opportunities
    # -----------------------------------------------------

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

            # -------------------------------------------------
            # Header
            # -------------------------------------------------

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

            # -------------------------------------------------
            # Decision
            # -------------------------------------------------

            fit_col, apply_col = st.columns(2)

            with fit_col:
                st.markdown(
                    f"**FIT:** {fit}"
                )

            with apply_col:
                st.markdown(
                    f"**APPLY:** {apply_decision}"
                )

            # -------------------------------------------------
            # Why
            # -------------------------------------------------

            st.markdown("**Why**")

            if evaluation.strengths:
                st.write(
                    evaluation.strengths[0]
                )
            else:
                st.write(
                    evaluation.reasoning
                )

            # -------------------------------------------------
            # Where It Doesn't Fit
            # -------------------------------------------------

            if evaluation.concerns:

                st.markdown(
                    "**Where it doesn't fit**"
                )

                for concern in evaluation.concerns[:2]:

                    st.write(
                        f"- {concern}"
                    )

            # -------------------------------------------------
            # Deep Dive Button
            # -------------------------------------------------

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

                else:
                    st.session_state[
                        "deep_dive_index"
                    ] = index - 1

                st.rerun()

            # -------------------------------------------------
            # Deep Dive
            # -------------------------------------------------

            if is_open:

                st.divider()

                st.markdown(
                    "## Deep Dive"
                )

                st.markdown(
                    "### Why this is a fit"
                )

                st.write(
                    evaluation.reasoning
                )

                deep_col1, deep_col2 = st.columns(2)

                with deep_col1:

                    st.markdown(
                        "### Strengths"
                    )

                    if evaluation.strengths:

                        for strength in evaluation.strengths:

                            st.write(
                                f"- {strength}"
                            )

                    else:

                        st.write(
                            "None identified."
                        )

                with deep_col2:

                    st.markdown(
                        "### Where it doesn't fit"
                    )

                    if evaluation.concerns:

                        for concern in evaluation.concerns:

                            st.write(
                                f"- {concern}"
                            )

                    else:

                        st.write(
                            "No significant concerns identified."
                        )

                st.markdown(
                    "### Score Breakdown"
                )

                dimensions = evaluation.dimension_scores

                score_cols = st.columns(
                    len(dimensions)
                )

                for column, (dimension, score) in zip(
                    score_cols,
                    dimensions.items(),
                ):

                    with column:

                        st.metric(
                            dimension.replace(
                                "_",
                                " ",
                            ).title(),
                            f"{score:.1f}",
                        )


    # -----------------------------------------------------
    # Filtered Jobs
    # -----------------------------------------------------

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