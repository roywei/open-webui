<script lang="ts">
    import { onMount } from 'svelte';

    type ChatMessage = { role: 'user' | 'assistant'; text: string };
    let messages: ChatMessage[] = [];

    let pc: RTCPeerConnection;
    let dc: RTCDataChannel;

    function append(role: 'user' | 'assistant', delta: string) {
        const last = messages[messages.length - 1];
        if (!last || last.role !== role) {
            messages = [...messages, { role, text: delta }];
        } else {
            last.text += delta;
            messages = [...messages];
        }
    }

    onMount(async () => {
        const tokenRes = await fetch('/api/v1/realtime/session');
        const token = await tokenRes.json();
        const EPHEMERAL_KEY = token.client_secret.value;

        pc = new RTCPeerConnection();

        const audioEl = document.getElementById('assistant-audio') as HTMLAudioElement;
        pc.ontrack = (e) => {
            audioEl.srcObject = e.streams[0];
        };

        dc = pc.createDataChannel('oai-events');
        dc.onmessage = (ev) => {
            try {
                const msg = JSON.parse(ev.data);
                if (msg.type === 'response.output_text.delta') {
                    append('assistant', msg.delta);
                } else if (msg.type === 'input_audio_buffer.transcript.delta') {
                    append('user', msg.delta);
                }
            } catch (err) {
                console.error(err);
            }
        };

        const ms = await navigator.mediaDevices.getUserMedia({ audio: true });
        ms.getTracks().forEach((t) => pc.addTrack(t, ms));

        const offer = await pc.createOffer();
        await pc.setLocalDescription(offer);

        const answer = await fetch('https://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview', {
            method: 'POST',
            body: offer.sdp ?? '',
            headers: {
                Authorization: `Bearer ${EPHEMERAL_KEY}`,
                'Content-Type': 'application/sdp'
            }
        });
        const answerText = await answer.text();
        await pc.setRemoteDescription({ type: 'answer', sdp: answerText });
    });
</script>

<div class="space-y-4">
    <audio id="assistant-audio" autoplay class="hidden"></audio>
    <div class="max-h-64 overflow-y-auto border rounded p-2 text-sm">
        {#each messages as m}
            <div class="my-1">
                <span class="font-bold capitalize">{m.role}:</span> {m.text}
            </div>
        {/each}
    </div>
</div>
