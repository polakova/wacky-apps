# 111 Wacky Apps — Builder's Style Guide (READ FULLY)

You are building tiny, self-contained web "toy" apps for a retro-but-cool site called **111 Wacky Apps**.
Vibe: old-internet soul (GeoCities, Flash games, Magic 8-Balls, bubble wrap) with **modern polish**.
Fun for boomers, millennials, and gen-z alike. Each app must feel finished, delightful, and a little silly.

## Hard rules (non-negotiable)
1. **One file per app:** `/home/tana/wacky-apps/apps/<slug>/index.html`. Create the folder. Nothing else.
2. **Self-contained.** Plain HTML + CSS + vanilla JS in that one file. The ONLY external reference allowed is the shared stylesheet: `<link rel="stylesheet" href="../_shared/wacky.css">`. **No CDNs, no frameworks, no fonts, no images, no network calls of any kind.** Emoji are fine. Sound via the WebAudio API only (no audio files).
3. **It must actually work** and be genuinely interactive. No placeholders, no "TODO", no fake buttons. Test the logic in your head end-to-end.
4. **Mobile friendly.** Works at 360px wide and on desktop. Tappable targets.
5. Keep each app focused and not huge — roughly 60–180 lines. Quality over size.
6. Follow the app's `spec` in apps.json, but add charming little touches.

## Required page skeleton (use EXACTLY this top, fill placeholders)
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE} · 111 Wacky Apps</title>
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>{EMOJI}</text></svg>">
<link rel="stylesheet" href="../_shared/wacky.css">
<style> /* app-specific styles here */ </style>
</head>
<body>
<div class="wacky-bar">
  <a class="back" href="../../">← all 111</a>
  <span class="title">{EMOJI} {TITLE}</span>
  <span class="spacer"></span>
  <span class="num">#{ID}</span>
</div>
<!-- your app UI here, ideally inside <div class="wrap"> ... </div> -->
<script> /* your app logic here */ </script>
</body>
</html>
```

## Shared CSS you can use (already loaded — DON'T redefine, just use the classes)
- Layout: `.wrap` (centered max-width container), `.card`, `.center`, `.stack` (vertical flex), `.row` (horizontal flex wrap).
- Buttons: `.btn` plus optional `.pink` / `.purple` / `.blue`. Default is yellow.
- Text: `.big` (huge heading), `.output` (big result text), `.muted`, `.pill`.
- Inputs: plain `<input> <textarea> <select>` are already styled (chunky black border).
- Animations: add class `.shake`, `.pop`, or `.blink`. `canvas` is responsive.
- CSS variables available: `--ink --paper --pink --purple --cyan --yellow --orange --blue --shadow --shadow-sm --mono --sans`.
- Use these for consistency, but you may add your own `<style>` for the app's unique character (themes welcome: a metal app can go dark, a vaporwave app can go neon, etc).

## Quality bar / flavor
- Add a tiny bit of copy/personality (a cheeky subtitle, fun result labels).
- Generators: include **plenty** of varied options (aim for enough combinations that repeats feel rare — e.g. 15+ items per word-array). Make the content actually funny/clever and ORIGINAL — do not copy famous copyrighted lines; write your own.
- Add a "copy to clipboard" button where it makes sense (use navigator.clipboard with a fallback).
- Animations and micro-interactions make these shine. A button press should feel good.
- WebAudio apps: create the AudioContext on first user gesture (autoplay policy).
- Use `localStorage` for high scores / counters where the spec implies persistence.
- Keyboard support where natural (e.g. games, piano).

## Content safety
Keep everything light, kind, and PG. No slurs, no real targeting, no harmful instructions. "Insults"/"roasts" must be clearly silly/Shakespearean-style and harmless.

Build each assigned app to be something you'd actually want to show a friend. Make them smile.
