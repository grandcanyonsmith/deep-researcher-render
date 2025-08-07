# deep-researcher-render

FastAPI web service that streams research using OpenAI `o3-deep-research` via the Responses API.

- Service name in Blueprint: `deep-researcher-service`
- Endpoint: `/research?topic=ping`
- Env: `OPENAI_API_KEY`
- Port: `10000` (binds to `$PORT`)

## Deploy

Use the Render Blueprint:

[Deploy to Render](https://render.com/deploy?repo=https://github.com/grandcanyonsmith/deep-researcher-render)

The Blueprint expects you to provide `OPENAI_API_KEY` during setup.

Alternatively, create a Web Service from this repo. The service builds from the Dockerfile and runs `uvicorn server:app`.
