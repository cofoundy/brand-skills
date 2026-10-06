# Brand Mod — method and decisions

Why the spinner looks the way it does. Every rule here came from a version that was built, shown
live, and rejected (October 2026, building Cofoundy's own spinner before turning it into this skill).

## The icon: a 2×2 square of half blocks

- **Two characters of half blocks (`▀ ▄`) make a square.** A terminal cell is about twice as tall as
  it is wide, so a one-character glyph (`▟ ▙ ▛ ▜`) reads as a tall rectangle with a bite out of it.
- **Each character carries two cubes:** the top half is the text color and the bottom half is the
  background color, so every cube gets its own tone.
- **Rejected:** a hexagon `⬢` (generic, every agent uses it), braille cubes (read as noise),
  animations that build up and tear down (the restart is visible), a fixed shape with only moving
  light (reads as static), a rotating two-row pyramid (messy between vertices), a two-row factory
  belt (too big for a spinner).

## Motion

- **Real movement with a seamless loop.** What people liked always moves and has no visible restart
  point (waves, an orbit, the turning gap).
- **One glint** crosses the square diagonally and carries on through the word, so the icon and the
  text read as one piece.
- **Claude Code redraws the spinner at most 10 times a second.** A 150 ms step shows as alternating
  100 and 200 ms; pick multiples of 100 ms if the rhythm must be even.

## The desktop app

- **Draw the logo as an image.** An `Svg` with `isInteractive` (a sandboxed frame, needed for
  hover) is rebuilt on every frame and flickers. As an image, SMIL animation still runs, or the
  logo stays still, which is acceptable.
- **The word is one color.** The glint's near-white tones vanish on a light theme.
- **A short, strong flash reads as blinking.** The sweep is slow and soft (3.2 s, about half
  opacity).
- **Dark mode:** the generated SVG carries both logos and picks with `prefers-color-scheme`, which
  follows the OS. If someone sets the app theme apart from the OS, the logo can be the other one.

## The terminal logo

- Only with kitty graphics: Ghostty or kitty run directly. Multiplexers (herdr, tmux, zellij,
  screen) don't pass images through, so the mod draws nothing there, not even a stand-in glyph.
- Use the light logo on a dark terminal.

## Words

See `SKILL.md` § Words. The short version: real gerunds the team says, from the voice guide; no brand
puns; past participles for the end of turn.

## README capture

- `agent-browser` records the whole viewport (1280 px wide, regardless of `viewport`), so the
  script measures the window with `eval` and crops with ffmpeg.
- A hash-only URL change doesn't reload the page; each shot opens the preview with its own query.

## Limits to tell the owner

- The mods API is early access. If a Claude Code update changes it, the spinner falls back to Claude
  Code's own and nothing else breaks, but the mod needs maintenance.
- The preview uses the browser's font; proportions in a real terminal can differ slightly.

## Checklist before shipping

- [ ] `--check` green (validate + test).
- [ ] Preview reviewed on both desktop themes and "inside herdr".
- [ ] Words read by someone on the team.
- [ ] Owner's approval in writing.
- [ ] Real run: `claude --plugin-dir ./<slug>-spinner` in Ghostty and in the desktop app's Code tab.
