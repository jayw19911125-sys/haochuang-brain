# Manus Media Contract — Three-Tier Priority Model

This file is the single source of truth for **how speech, music, images, sound effects, and audio transcription are produced inside the `html-video-production` skill in Manus**. It overrides any conflicting media instructions in the bundled upstream HyperFrames skills under `references/`. Whenever an upstream file describes a different path (the `audio.mjs` / `resolve.mjs` orchestrators, HeyGen, ElevenLabs, Kokoro, Lyria, `npx hyperframes lambda`, etc.), the model below wins.

## The model in one screen

| Tier | What | When | Examples |
| --- | --- | --- | --- |
| **Tier 1 — Manus native** | `generate_speech`, `generate_music`, `generate_image` | **Default for all generative media.** Always prefer this. | Voiceover, score/underscore, product images, icons, background plates |
| **Tier 2 — Local open-source fallback (permitted)** | `npx hyperframes transcribe` (whisper.cpp), `npx hyperframes remove-background` (U2-Net), bundled Pixabay SFX, `npx hyperframes tts` (Kokoro) | When no native tool fits, or the task has no native equivalent. Free, local, offline. | Word-level caption timing, subject cutout/matting, quick SFX, last-resort voice |
| **Tier 3 — Hard prohibited** | `npx hyperframes init` skill auto-pull · `hyperframes lambda *` · the HeyGen-paid branch of `audio.mjs`/`resolve.mjs` | Never. | — |

> Why tiers and not a blanket ban: the CLI media subcommands (`tts`/`transcribe`/`remove-background`) run **local open-source models**, not paid cloud. They are free and offline, so they are a legitimate fallback, not a violation. The only genuine violations are the three Tier-3 items.

---

## Tier 1 — Manus-native generation (the default path)

### Hard rules

1. **Narration / voiceover** → `generate_speech`.
2. **Background music / underscore / stings** → `generate_music`. Never compose with ffmpeg or call a third-party music API.
3. **Raster images / icons / product shots / textured backgrounds** not supplied by the user → `generate_image` (or `generate_image_variation` for edits). Never use placeholder image services or assume runtime-fetched images.
4. **Word-level timestamps** → see Tier 2 (`transcribe`) or the OpenAI Whisper API; `generate_speech` does not return word timings.
5. **Always generate the asset before referencing it** in HTML. No `<audio src>` / `<img src>` against a path that does not yet exist.

Read the `tts-prompter` skill for speech prompt construction and the `music-prompter` skill for music prompt construction. This document is the integration contract for slotting their outputs into a HyperFrames project.

### The critical substitution: do NOT run the orchestrators

Upstream workflows call two scripts that, when a `HEYGEN_API_KEY` is present, hit the **paid HeyGen cloud**:

- `references/hyperframes-media/scripts/audio.mjs` — unified TTS + BGM + SFX → `audio_meta.json`
- `references/media-use/scripts/resolve.mjs` — asset resolver → `.media/manifest.jsonl`

**Do not run either.** Instead, generate each asset with the Tier-1 tools and **hand-write the ledger files those scripts would have produced**, so the downstream pipeline (captions, duration sync, assembly, render) consumes them transparently. The schemas are below.

### `audio_meta.json` — hand-written (id-keyed; consumed by caption/assembly steps)

Place voice files at `assets/voice/<id>.wav`, BGM at `assets/bgm/track.wav`. The `words` array is the caption-timing source — fill it from a Tier-2 `transcribe` pass (preferred) or the Whisper API.

```json
{
  "tts_provider": "manus-generate_speech",
  "voice_id": "<the Manus voice you used>",
  "bgm": { "path": "assets/bgm/track.wav", "volume": 0.15, "mode": "generate", "query": null, "duration_s": 12.3 },
  "bgm_pending": false, "bgm_provider": "manus-generate_music", "bgm_pid": null, "bgm_log": null,
  "bgm_mode": "generate", "bgm_target_duration_s": 12.3, "bgm_seed_duration_s": null, "bgm_loop_count": null,
  "voices": [
    { "id": "01", "path": "assets/voice/01.wav", "duration_s": 3.2,
      "words": [ { "id": "w0", "text": "Hello", "start": 0.0, "end": 0.4 } ] }
  ],
  "sfx": [
    { "id": "01", "name": "whoosh", "file": "assets/sfx/whoosh.mp3", "source": "bundled-pixabay",
      "offset_s": 0, "duration_s": 0.8, "volume": 1 }
  ],
  "total_duration_s": 12.3
}
```

If a workflow expects subset merges (`audio.mjs --only tts,bgm,sfx`, `sync-durations`, `fetch-sfx`), just regenerate/patch the relevant keys of this same file by hand — the downstream steps only read the JSON, they do not require the script to have written it.

### `.media/manifest.jsonl` — hand-written (one JSON record per line)

When a workflow uses the `media-use` resolver, generate the image with `generate_image`, save it under `.media/images/`, and append one line per asset. Directory map: `bgm→.media/audio/bgm`, `sfx→.media/audio/sfx`, `voice→.media/audio/voice`, `image|icon|brand→.media/images`, `video→.media/video`. IDs are `<type>_<NNN>` zero-padded. After appending, you may regenerate `.media/index.md` by hand or leave it — downstream reads the `.jsonl`.

```json
{ "id":"image_001", "type":"image", "path":".media/images/image_001.png", "source":"generated", "description":"<intent>", "width":1920, "height":1080, "transparent":false, "provenance": { "provider":"manus-generate_image", "prompt":"<intent>" } }
```

### Speech details

- **Write `narration.txt` first** (the exact string passed to `generate_speech`, with pronunciation fixes like "API" → "A P I"), separate from the human-readable `SCRIPT.md`. This makes voice re-generation trivial.
- **Use SSML** for pacing: `<break time="...ms"/>`, `<prosody rate/pitch/volume>`, `<emphasis>`.
- **Place the wav** with `data-duration="auto"` so HyperFrames reads true duration via ffprobe; or run `ffprobe -i narration.wav -show_entries format=duration -v quiet -of csv="p=0"` to declare it explicitly.

```html
<audio id="narration" data-start="0" data-duration="auto" data-track-index="2" src="assets/voice/01.wav" data-volume="1"></audio>
```

### Music details

- Decide **role** (underscore / lead bed / sting), **mood arc**, and **duration** (composition length + 0.5 s tail; `generate_music` does not auto-trim).
- `data-volume` defaults: **0.10–0.20** under narration, **0.50–0.70** when music leads, **1.0** for stings.

```html
<audio id="bg-music" data-start="0" data-duration="auto" data-track-index="3" src="assets/bgm/track.wav" data-volume="0.15"></audio>
```

- For audio-reactive beats (`references/hyperframes-animation` / audio-reactive guidance), pre-extract amplitude data from any local `.wav`/`.mp3` with the bundled `extract-audio-data.py` script — it reads local files and is unaffected by tier routing.

### Image details

- **Generate** when the composition needs a product/marketing image, an icon/logo not in `assets/`, a background plate, or a variation of an existing image.
- **Do NOT generate** for pure CSS/GSAP shapes, registry iconography (`hyperframes add <name>`), or charts (build those as live SVG/Canvas, not flat PNG).
- **Aspect ratio** matches the output frame: **16:9 (1920×1080)** or **9:16 (1080×1920)**; square only for an explicit Instagram-feed asset.
- Every image needs motion treatment (per the animation skill's motion principles) — never embed a raw flat image.

```html
<img id="hero" class="clip" data-start="0" data-duration="5" data-track-index="1" src="hero.png" />
```

---

## Tier 2 — Permitted local open-source fallbacks

These run locally, for free, with no external paid call. Use them when Tier 1 does not fit.

| Tool | Engine (local OSS) | Use it for |
| --- | --- | --- |
| `npx hyperframes transcribe <audio>` | whisper.cpp (ggml `small.en` by default) | **Word-level caption timing** — the recommended way to fill the `words` arrays in `audio_meta.json`, even when the voice came from Tier 1 `generate_speech`. |
| `npx hyperframes remove-background <img>` | U2-Net (`u2net_human_seg`, onnxruntime) | Subject cutout / matting. Manus has no native equivalent, so this is the **preferred** path. |
| Bundled SFX `assets/sfx/*.mp3` | Pixabay Content License (commercial-free) | Drop-in sound effects. Always allowed; reference directly, no API call. |
| `npx hyperframes tts <text>` | Kokoro-82M (`kokoro-onnx`) | **Last-resort** voice only, when `generate_speech` is unavailable. Tier 1 is strongly preferred. |
| Local BGM generation (MusicGen/Lyria recipe) | local models | Only if Tier 1 `generate_music` is unavailable. |

Alternative for word timestamps without whisper.cpp installed: call the **OpenAI Whisper API** (`response_format="verbose_json"`, `timestamp_granularities=["word"]`) and convert `transcript.words` into the `{id,text,start,end}` shape used in `audio_meta.json`. Save as `transcript.json` for the caption step.

```python
from openai import OpenAI
client = OpenAI()
with open("assets/voice/01.wav", "rb") as f:
    t = client.audio.transcriptions.create(
        model="whisper-1", file=f,
        response_format="verbose_json", timestamp_granularities=["word"])
```

---

## Tier 3 — Hard prohibitions (never)

1. **`npx hyperframes init` skill auto-pull.** `init` re-fetches the latest skills from GitHub on every run (the `--skip-skills` flag is currently neutered upstream) and would overwrite these Manus-patched skill files, silently re-enabling disabled paths. **Scaffold manually** (`npm init -y` + `npm install hyperframes` + hand-authored composition HTML). `npx hyperframes capture <url>` is fine — it does not re-pull skills.
2. **`hyperframes lambda *`** (deploy / render / progress / destroy / policies) — paid AWS cloud rendering. **Render locally** with `npx hyperframes render` (add `--docker --strict` for long/large jobs); it is CPU-bound but free and offline-safe.
3. **The HeyGen-paid branch** inside `audio.mjs` / `lib/tts.mjs` / `resolve.mjs`. These scripts choose the paid branch only when `heygenCredential() !== null`. **Never set `HEYGEN_API_KEY`** — with no credential the code can never reach the paid path. Combined with rule "do not run the orchestrators" above, this branch is doubly neutralized.

---

## Cross-references

- [`modifications.md`](modifications.md) — every upstream file Manus modified, for Apache 2.0 §4(b).
- `references/hyperframes-media/` — upstream audio-engine docs (read for the `audio_meta.json` schema the scripts emit; do **not** run the scripts).
- `references/media-use/` — upstream asset-resolver docs (read for the `manifest.jsonl` schema; do **not** run the resolver).
- `references/embedded-captions/`, `references/hyperframes-core/` — caption authoring and asset placement (consume the `words` timing produced above).
