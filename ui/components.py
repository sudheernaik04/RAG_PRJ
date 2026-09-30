from __future__ import annotations

import streamlit as st


def render_status_badge(label: str, value: str, state: str = "ok") -> None:
    state_class = {
        "ok": "status-ok",
        "warn": "status-warn",
        "bad": "status-bad",
    }.get(state, "status-warn")
    st.markdown(
        f"<span class='status-badge {state_class}'>{label}: {value}</span>",
        unsafe_allow_html=True,
    )


def render_retrieval_panel(retrieved_results: list[dict]) -> None:
    if not retrieved_results:
        st.info("No relevant chunks were retrieved. The answer will not be grounded in unrelated content.")
        return

    with st.expander("View retrieved context", expanded=False):
        for result in retrieved_results:
            source_name = result.get("source_name", "unknown")
            page_number = result.get("page_number")
            chunk_id = result.get("chunk_id", "unknown")
            score = result.get("score", 0.0)
            text = result.get("text", "")

            st.markdown(f"### {chunk_id}")
            st.caption(f"Source: {source_name} | Page: {page_number or 'n/a'} | Similarity: {score:.4f}")
            st.write(text)
            st.markdown("---")
