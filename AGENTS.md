# AGENTS.md

## Scope
These instructions apply to the entire repository.

## Project Vision
Open WebUI is an extensible, offline‑capable AI platform.  For this fork, the goal is to evolve it into a personal assistant that can:
- speak and video chat in real time using the OpenAI Real‑Time API;
- interact with multiple MCP (Machine Control Protocol) servers for home automation or robotics control;
- remain self‑hostable and keep the existing front‑end/back‑end tech stack.

## Tech Stack
- **Frontend**: Svelte 4, TypeScript, Vite, Tailwind CSS.
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy.
- **Node**: >= 18.13.0 (see `package.json`).

## General Guidelines
- Keep UX, theming and component aesthetics consistent with the current Svelte/Tailwind design.
- Prefer the existing plugin/extension architecture when adding new capabilities such as real‑time streaming or MCP integrations.
- All configuration secrets (API keys, tokens) must be provided via environment variables.
- Write concise commit messages using the Conventional Commits style (`feat:`, `fix:`, `docs:` …).

## Frontend
- Use TypeScript and Svelte components stored under `src/`.
- Style exclusively with Tailwind CSS utilities and existing design tokens.
- Validate code with ESLint and `svelte-check`.

## Backend
- Use type‑hinted, async Python code organized under `backend/open_webui/`.
- Format with `black` and lint with `pylint`.
- Encapsulate integrations (OpenAI Real‑Time API, MCP servers, etc.) in well‑named modules or routers.

## Testing
Before committing, run all checks:
1. `npm run lint` – runs ESLint, Svelte type checks and `pylint` for the backend.
2. `npm run test:frontend` – executes the Vitest test suite (pass‑with‑no‑tests).
3. `pytest` – runs backend tests; requires Docker to spin up a temporary Postgres instance.

Tests must pass (or best effort made if an environment limitation is hit) before submitting a PR.

## Documentation
- Update `docs/` or relevant Markdown files when behaviour or configuration options change.
- Include usage examples for new real‑time or MCP features.

## Pull Requests
- Keep PRs focused and small.
- Describe the change, the motivation, and relevant configuration steps.
- Mention any new environment variables or migrations.

