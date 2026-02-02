"""AI Mirror — OpenAI synthesis engine.

Constructs a prompt from aggregated data and generates a strategic
'Guerilla Tactic' using GPT-4o. Supports typewriter-style streaming
output via st.empty().
"""

import logging
import time

import streamlit as st
from openai import OpenAI

from mcl_blueprint.config import OPENAI_MAX_TOKENS, OPENAI_MODEL
from mcl_blueprint.models import AggregatedData

logger = logging.getLogger(__name__)


def build_synthesis_prompt(data: AggregatedData) -> str:
    """Construct the system + user prompt from aggregated data.

    Args:
        data: Aggregated response data with top_priority, top_threat,
              and dominant_archetype populated.

    Returns:
        The formatted prompt string for the OpenAI API.
    """
    return (
        "You are a strategic advisor for Muslim Campus Life. "
        f"The data shows students prioritize **{data.top_priority}** "
        f"but face **{data.top_threat}** as their top threat. "
        f"Their universities have a **{data.dominant_archetype}** "
        "policy regarding AI.\n\n"
        "**Task:** Write a specific, 3-sentence 'Guerilla Tactic' for how "
        f"these students can use AI tools to achieve {data.top_priority} "
        f"despite {data.top_threat}, taking advantage of the "
        f"{data.dominant_archetype} policy environment."
    )


def generate_synthesis(data: AggregatedData) -> str:
    """Call OpenAI API to generate the strategic synthesis.

    Args:
        data: Aggregated response data.

    Returns:
        The generated tactic text.

    Raises:
        RuntimeError: If the API call fails or returns empty.
    """
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    prompt = build_synthesis_prompt(data)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a concise strategic advisor. "
                    "Respond in exactly 3 sentences."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_completion_tokens=OPENAI_MAX_TOKENS,
        temperature=1.0,
    )

    content = response.choices[0].message.content
    if content is None:
        raise RuntimeError("OpenAI returned empty response")
    return content


def render_typewriter(text: str, speed: float = 0.03) -> None:
    """Display text character-by-character using st.empty() for drama.

    Args:
        text: The full text to display.
        speed: Seconds between each character. Defaults to 0.03.
    """
    placeholder = st.empty()
    displayed = ""
    for char in text:
        displayed += char
        placeholder.markdown(f"### {displayed}▌")
        time.sleep(speed)
    # Final render without cursor
    placeholder.markdown(f"### {displayed}")
