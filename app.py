import streamlit as st

from examples.run_job_needle_finder import run_finder


st.set_page_config(
    page_title="Job Needle Finder",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 Job Needle Finder")
st.write(
    "Find the opportunities that actually match the candidate."
)

st.divider()

use_real_llm = st.checkbox(
    "Use real LLM reasoning",
    value=False,
)

if st.button("Run Job Needle Finder", type="primary"):

    with st.spinner("Finding the needles..."):

        results, filtered_jobs = run_finder(
            use_real_llm=use_real_llm
        )

    st.success(
        f"Found {len(results)} ranked opportunities."
    )

    st.subheader("Top Opportunities")

    for index, result in enumerate(results, start=1):

        job = result["job"]
        evaluation = result["evaluation"]

        with st.container(border=True):

            st.markdown(
                f"### {index}. {job['title']}"
            )

            st.write(
                f"**{job['company']}**"
            )

            st.metric(
                "Needle Score",
                f"{evaluation.score:.1f}"
            )

            st.write(
                f"**Recommendation:** "
                f"{evaluation.recommendation.upper()}"
            )

            st.write(
                f"**Why:** {evaluation.reasoning}"
            )

            if evaluation.strengths:
                st.write("**Strengths**")
                for strength in evaluation.strengths:
                    st.write(f"- {strength}")

            if evaluation.concerns:
                st.write("**Concerns**")
                for concern in evaluation.concerns:
                    st.write(f"- {concern}")