# deep-researcher-render

FastAPI web service that streams research using OpenAI o3-deep-research.

- Endpoint: `/research?topic=ping`
- Env: `OPENAI_API_KEY`

Dockerfile builds a minimal image using Python 3.11 and runs `uvicorn server:app` on port 8000.
