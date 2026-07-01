# Manus Modifications to Upstream HyperFrames Skills

This document records every change Manus made to the upstream HyperFrames skill materials when packaging them as the `html-video-production` Manus skill (built on HyperFrames). Maintained per Apache License 2.0 §4(b) ("modified files must carry prominent notices stating that You changed the files").

## Provenance

- **Upstream project:** [`heygen-com/hyperframes`](https://github.com/heygen-com/hyperframes)
- **Upstream license:** Apache License 2.0 (preserved verbatim in `../UPSTREAM_LICENSE_APACHE-2.0.txt`)
- **Pinned upstream commit:** `c811a2750a2f9a242b764959e7509217f9943511`
- **Pinned commit date:** 2026-06-28
- **Packaging model:** Full coverage. All 19 upstream skills under `skills/` are redistributed under `references/` (the upstream `skills/<name>/` layout is flattened one level so that every skill sits directly at `references/<name>/`, preserving the upstream `../<sibling-skill>/` cross-links verbatim).

### Bundled upstream skills (19/19)

Domain skills: `hyperframes` (legacy router), `hyperframes-core`, `hyperframes-animation`, `hyperframes-creative`, `hyperframes-cli`, `hyperframes-registry`, `hyperframes-media`, `media-use`.

Workflow skills: `product-launch-video`, `faceless-explainer`, `pr-to-video`, `motion-graphics`, `embedded-captions`, `talking-head-recut`, `website-to-video`, `music-to-video`, `slideshow`, `general-video`, `remotion-to-hyperframes`.

> Note on the earlier Manus build: the previous packaging bundled only 5 skills (`gsap`, `hyperframes`, `hyperframes-cli`, `hyperframes-registry`, `website-to-hyperframes`) against pinned commit `8d83d4f`. Upstream has since refactored the monolithic `hyperframes` skill into the modular domain/workflow set above, folded the standalone `gsap` skill into `hyperframes-animation`, and renamed `website-to-hyperframes` → `website-to-video`. This build tracks that refactor and expands to full coverage.

## Why these changes exist

Upstream ships several third-party / paid media paths: the unified audio orchestrator `hyperframes-media/scripts/audio.mjs` and the asset resolver `media-use/scripts/resolve.mjs` both **prefer the paid HeyGen cloud API** when a `HEYGEN_API_KEY` is present and fall back to local engines (Kokoro TTS, MusicGen/Lyria BGM, bundled SFX) otherwise; the CLI exposes `tts`, `transcribe`, `remove-background` (local open-source models), and `lambda *` (paid AWS cloud render). Inside Manus these are governed by the **Three-Tier Priority Model** in [`media-generation.md`](media-generation.md):

- **Tier 1 (default):** Manus-native `generate_speech` / `generate_music` / `generate_image`, with the agent hand-writing the `audio_meta.json` and `.media/manifest.jsonl` ledgers the downstream pipeline expects.
- **Tier 2 (permitted fallback):** local, free, offline open-source paths — `hyperframes transcribe` (whisper.cpp), `hyperframes remove-background` (U2-Net), the bundled Pixabay SFX, and `hyperframes tts` (Kokoro) as a last-resort voice fallback.
- **Tier 3 (hard-prohibited):** `npx hyperframes init` skill auto-pull, `hyperframes lambda *`, and the HeyGen-paid branch (neutralized simply by never setting `HEYGEN_API_KEY`).

The modifications below are the minimum required to (a) keep agents on the tiered contract at the exact step they would otherwise run a disabled path, (b) disable the genuine Tier-3 violations (paid HeyGen/ElevenLabs sign-in gates, provider-choice prompts, `init` skill auto-pull, `lambda` cloud render), and (c) annotate modified files per §4(b). All other upstream content is preserved verbatim from the pinned commit.

> **Patch philosophy.** Earlier Manus builds relied only on the additive top-of-file banner (a *declarative* override). That left the upstream body text intact, so a literal step-by-step reading could still hit a sign-in gate or a "choose your TTS provider" prompt — the banner and the body contradicted each other. This build therefore also applies **destructive in-place patches** to the specific body passages that would otherwise (1) **STOP and wait** for a HeyGen sign-in / offline decision, (2) **ask the user to choose a TTS/BGM provider** or set `HEYGEN_API_KEY` / `ELEVENLABS_API_KEY`, or (3) **run `npx hyperframes init`** (skill auto-pull). After patching, the body the agent actually executes is already contract-compliant; `modifications.md` exists for §4(b) compliance and re-sync auditing only and is **not** read at runtime.

## Modified files (relative to skill package root)

### 1. Every bundled `references/<skill>/SKILL.md` (all 19)

- **MANUS OVERRIDE banner prepended** to the top of each `SKILL.md` (above the YAML frontmatter). The banner: (a) points to `media-generation.md` as the controlling contract; (b) says to skip the `npx hyperframes auth status` preflight; (c) forbids running `scripts/audio.mjs` / `media-use/scripts/resolve.mjs` and explains the Tier-1 hand-written-ledger substitute; (d) forbids surfacing a TTS-provider choice; (e) forbids `npx hyperframes init` and `hyperframes lambda *`. No upstream body content is removed by the banner; it is purely additive and sits before the original text.

### 2. `references/hyperframes-cli/SKILL.md`

- **Scaffold step (Workflow #1) rewritten** — the upstream instruction to run `npx hyperframes init my-video` (which re-pulls and overwrites global skills on every run, with `--skip-skills` currently neutered) is replaced with a manual scaffold recipe (`npm init -y` + `npm install hyperframes` + hand-authored composition HTML). `npx hyperframes capture <url>` is explicitly still allowed because it does not re-pull skills.
- **Cloud render line (Workflow #7) rewritten** — the `npx hyperframes lambda render ...` option is replaced with a note that `hyperframes lambda *` is disabled (paid AWS cloud) and that long/large jobs should use local `render --docker --strict`.
- All other CLI command documentation (lint, validate, inspect, preview, render, doctor, browser, info, upgrade, skills, compositions, docs, benchmark, telemetry, and the Tier-2 `tts` / `transcribe` / `remove-background` subcommands) is preserved verbatim from upstream.

### 3. Workflow `SKILL.md` files that invoke the disabled orchestrators

Affected files: `references/faceless-explainer/SKILL.md`, `references/pr-to-video/SKILL.md`, `references/product-launch-video/SKILL.md`, `references/general-video/SKILL.md`, `references/motion-graphics/SKILL.md`.

- **Inline `[MANUS OVERRIDE]` markers inserted** immediately before each command line that runs `node .../scripts/audio.mjs ...` or `node .../resolve.mjs ...`. Each marker tells the agent not to run the following command and to generate the media with native tools + hand-written ledger per `media-generation.md`. The original upstream command lines are left intact directly beneath each marker (not deleted) so the expected inputs/outputs remain documented for ledger construction.

### 4. Sign-in (`auth status`) preflight blocks rewritten in workflow bodies

Affected files: `references/product-launch-video/SKILL.md`, `references/faceless-explainer/SKILL.md`, `references/pr-to-video/SKILL.md`, `references/website-to-video/SKILL.md`, `references/music-to-video/SKILL.md`, `references/hyperframes-media/SKILL.md` (Preflight section), `references/hyperframes-media/references/bgm.md`, `references/hyperframes-media/references/tts.md`, `references/hyperframes-media/references/requirements.md`.

- The upstream **"Show sign-in status" / Preflight** passages — which run `npx hyperframes auth status`, relay HeyGen sign-in guidance, and **STOP and wait for the user to choose** sign-in vs offline — are **replaced in place** with a `[MANUS OVERRIDE]` paragraph instructing the agent to skip the preflight entirely (no auth check, no decision point) and proceed directly, producing voice via `generate_speech` and music via `generate_music`. The associated **Gate** lines that required "sign-in status was shown" were edited to drop that condition.

### 5. `npx hyperframes init` / `skills update` auto-pull rewritten in bodies

Affected files: `references/product-launch-video/SKILL.md`, `references/faceless-explainer/SKILL.md`, `references/pr-to-video/SKILL.md`, `references/music-to-video/SKILL.md`, `references/motion-graphics/SKILL.md`, `references/embedded-captions/SKILL.md` (two mentions), `references/hyperframes/SKILL.md` ("Keeping skills current" section, incl. `skills check` / `skills update`), `references/hyperframes-cli/references/init-and-scaffold.md` (top-of-file note + section heading).

- Every body instruction to scaffold via `npx hyperframes init` (and the router's `skills check` / `skills update` guidance) is **replaced or annotated in place** with a `[MANUS OVERRIDE]` manual-scaffold recipe (`npm init -y` + `npm install hyperframes`), because `init` / `skills update` re-pull the full skill set from GitHub on every run (the `--skip-skills` flag is neutered) and would overwrite these patched files and re-enable disabled paid paths.

### 6. TTS/BGM provider-choice prompts rewritten to Manus-native

Affected files: `references/website-to-video/SKILL.md` (Step 4 summary line), `references/website-to-video/references/step-4-vo.md` (banner added; BGM-source menu, "TTS Provider" choice, HeyGen/ElevenLabs/Kokoro audition blocks, transcription branch, escalation + pronunciation notes), `references/hyperframes-media/references/tts-to-captions.md`.

- All passages that **ask the user to pick a voice/music provider**, that document HeyGen/ElevenLabs REST calls and API-key setup, or that gate generation on `auth status`, are **replaced in place** with the single Manus-native path: voice = `generate_speech`, music = `generate_music`, word timing = OpenAI Whisper API or `hyperframes transcribe` (Tier 2). Upstream provider-chain tables and engine details are retained beneath a `[MANUS OVERRIDE]` "reference only / does not apply under Manus" note rather than deleted, so the schemas remain documented.

## Bundled scripts left in place but governed by the contract

The upstream orchestrator scripts (`*/scripts/audio.mjs`, `media-use/scripts/resolve.mjs`, and their `lib/` providers, plus `assemble-index.mjs`, `captions.*`, `transitions.*`, `build-frame.*`, `analyze-beatgrid.py`, etc.) are redistributed **unmodified**. They are retained for two reasons: (1) their header comments document the exact `audio_meta.json` / `manifest.jsonl` schemas the agent must reproduce by hand under Tier 1; (2) the safe, non-media scripts (captions, transitions, assembly, beatgrid analysis) are still run directly. The media-generating orchestrators are gated by the inline markers above rather than edited, so future upstream re-syncs stay clean.

## Bundled assets

| Path | Source / License | Status |
| --- | --- | --- |
| `assets/sfx/*.mp3` (19 files) + `CREDITS.md` | Pixabay Content License (commercial-free, no attribution required), as shipped in upstream `hyperframes-media/assets/sfx/` | Copied to the package root `assets/` for Tier-2 direct use. The duplicate in-place copies under `references/hyperframes-media/assets/sfx/` and `references/website-to-video/assets/sfx/` were byte-identical and have been removed to avoid triplication. |

## Excluded from the bundle (size compliance)

To keep the package within skill-package size limits (reduced from ~22 MB to ~9 MB) while preserving **all instructional text**, the following **binary / demo / regenerable** files were stripped. None are needed to read or follow the skills; at build time the agent obtains real equivalents via `npm install hyperframes` (which pulls the framework, fonts, GSAP, and example assets into `node_modules/`).

- **All demo/illustrative binaries under `references/`**: images (`*.png/.jpg/.jpeg/.gif/.webp/.avif`), example renders (`*.mp4/.webm/.mov`), and the duplicate SFX `*.mp3` copies. The HTML/Markdown that references them is preserved; only the heavy binaries are removed.
- **Bundled web fonts** (`*.woff2/.woff/.ttf/.otf`, e.g. `embedded-captions/modes/standard/fonts/files/`) and the 1.2 MB generated `fonts.css`. Fonts are reinstalled with the framework; `build-fonts-css.cjs` is kept so the CSS can be regenerated.
- **Vendored `gsap*.min.js` copies** — GSAP is installed via npm; the `hyperframes-animation` skill documents its usage.
- **Canonical `assets/sfx/` at the package root is retained** (Tier-2, always allowed) so the SFX stay available offline without any external fetch.

## Added files

| Path | Purpose |
| --- | --- |
| `SKILL.md` (top-level) | Manus-authored router: fidelity gate (reject photoreal → native video tools), intent dispatch across the 19 bundled skills, and the hard rules. Not derived from any single upstream file. |
| `_manus-overrides/media-generation.md` | Single source of truth for the Three-Tier Priority Model and the exact `audio_meta.json` / `.media/manifest.jsonl` schemas to hand-write under Tier 1. |
| `_manus-overrides/modifications.md` | This file. |
| `LICENSE`, `NOTICE.txt`, `UPSTREAM_LICENSE_APACHE-2.0.txt` | Apache 2.0 license + upstream attribution. |
| `assets/sfx/` | Tier-2 Pixabay SFX (see above). |

## Re-syncing with future upstream releases

1. Bump the pinned commit at the top of this file.
2. Re-copy all 19 skills under `references/`, flattening the `skills/<name>/` layout one level and stripping heavy media binaries.
3. Re-apply the modifications above. They are mechanical and low-surface: (a) prepend the banner to every `SKILL.md`; (b) re-patch the two CLI lines; (c) re-run the inline-marker patcher over the five orchestrator-invoking workflow files; (d) re-apply the body patches in §§4–6 — strip the `auth status` sign-in/STOP preflights, the `npx hyperframes init` / `skills update` auto-pull instructions, and the TTS/BGM provider-choice prompts, replacing each with the `[MANUS OVERRIDE]` native-tool text. Grep guards after re-sync: `grep -rn 'STOP and wait\|STOP for the user'`, `grep -rniE 'which (voice|tts|music) provider|ask the user which'`, and `grep -rn 'hyperframes init'` should return only `[MANUS OVERRIDE]`-annotated lines.
4. Update the bundled-skill list and asset table if the upstream skill set changes.
