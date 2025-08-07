import os
from typing import Optional

from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import PlainTextResponse
from openai import OpenAI

app = FastAPI(title="Deep Researcher")

def run_research(topic: str, effort: str = "medium", max_tokens: int = 120000) -> str:
    if not os.getenv("OPENAI_API_KEY"):
        raise HTTPException(status_code=500, detail="OPENAI_API_KEY environment variable is not set")

    client = OpenAI()

    prompt = (
        "You are an expert research assistant.\n\n"
        "First, immediately output a concise executive summary as 6 short bullets with one cited, working URL per bullet.\n"
        "Only after the bullets, continue with deeper research.\n\n"
        f"Topic: {topic}\n\n"
        "Research requirements (for the deeper section):\n"
        "- Search widely across credible, up-to-date sources.\n"
        "- Provide a structured, well-cited report with clear sections.\n"
        "- Include direct source URLs next to claims where possible.\n"
        "- Compare conflicting viewpoints and note consensus vs. disagreement.\n"
        "- Summarize key takeaways and action items at the end.\n"
        "- Avoid speculation; clearly mark uncertainties or insufficient evidence.\n"
    )

    collected_text_parts: list[str] = []
    with client.responses.stream(
        model="o3-deep-research",
        input=prompt,
        reasoning={"effort": effort},
        max_output_tokens=max_tokens,
        tools=[{"type": "web_search_preview"}],
    ) as stream:
        for event in stream:
            delta = getattr(event, "delta", None)
            if delta is not None:
                text_piece = getattr(delta, "text", None)
                if isinstance(text_piece, str) and text_piece:
                    collected_text_parts.append(text_piece)

    return "".join(collected_text_parts) if collected_text_parts else ""


@app.get("/research", response_class=PlainTextResponse)
def research(
    topic: str = Query(..., description="Topic to research"),
    effort: str = Query("medium", pattern="^(medium)$", description="Reasoning effort"),
    max_tokens: int = Query(120000, ge=1, le=200000, description="Max output tokens"),
):
    text = run_research(topic=topic, effort=effort, max_tokens=max_tokens)
    if not text:
        return "[Info] No textual content emitted. Try narrowing the prompt or increasing max_tokens."
    return text
