# Realtime Conversation API

Open WebUI now exposes a small helper endpoint for the [OpenAI Realtime API](https://platform.openai.com/docs/guides/realtime).
It follows the [blog post announcement](https://openai.com/blog) and the official API and prompting guides.

## Usage

1. Start a session by requesting an ephemeral key from the backend:
   ```bash
   curl -H "Authorization: Bearer <token>" \
        https://your-webui.example.com/api/v1/realtime/session
   ```
2. Use the returned `client_secret` with a WebRTC connection to `gpt-4o-realtime-preview`.
3. The included Svelte page (`/realtime`) demonstrates streaming text between the user and assistant while the
   assistant responds aloud using the new `verse` voice.

## Prompting

Send conversational prompts over the data channel. The API guide linked above
contains several examples for composing real‑time instructions.
