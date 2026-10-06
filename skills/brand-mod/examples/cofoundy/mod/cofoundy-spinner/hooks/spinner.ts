// Pure spinner logic (no `$`): rendering lives in register.tsx.
// Icon: a square 2×2 grid of half blocks (▀ ▄), three cubes and a hole turning clockwise; each
// character carries two cubes (top = color, bottom = bg). One glint crosses the square diagonally
// and carries on through the word. Why this and not something else: the brand-mod skill's method.md.
import { DONE, STOPS, WORDS } from './brand'

export type Cell = { ch: string; color: string; bg?: string }

export const FRAME_MS = 100 // the engine redraws the spinner at most 10 times a second
export const HOLE_MS = 150
const BASE = 3
const tone = (i: number): string => STOPS[Math.max(0, Math.min(STOPS.length - 1, i))] ?? '#888888'
const lit = (distance: number) => tone(Math.max(BASE, STOPS.length - 1 - Math.round(distance * 1.4)))

// The glint crosses the square (columns -3 and -2) and carries on through the word (column 0 on;
// -1 is the space), 1.5 columns per frame, then rests for 10 columns.
export function glintPos(wordLength: number, frame: number): number {
  return (Math.floor(frame * 1.5) % (wordLength + 3 + 10)) - 5
}

// Hole, clockwise: 0 top-left → 1 top-right → 2 bottom-right → 3 bottom-left.
export function square(now: number, pos: number): Cell[] {
  const hole = Math.floor(now / HOLE_MS) % 4
  const cube = (x: number, y: number) => lit(Math.abs(x - 3 + 0.5 * y - pos))
  const column = (x: number, up: number, down: number): Cell => {
    if (hole === up) return { ch: '▄', color: cube(x, 1) }
    if (hole === down) return { ch: '▀', color: cube(x, 0) }
    return { ch: '▀', color: cube(x, 0), bg: cube(x, 1) }
  }
  return [column(0, 0, 3), column(1, 1, 2)]
}

export function shimmerAt(text: string, pos: number): Cell[] {
  return [...text].map((ch, i) => ({ ch, color: lit(Math.abs(i - pos)) }))
}

export function spinnerWord(mode: string, seed: number): string {
  const pool = WORDS[mode] ?? WORDS.responding ?? ['Working']
  return pool[seed % pool.length] ?? 'Working'
}

export function doneWord(durationMs: number): string {
  return DONE[durationMs % DONE.length] ?? 'Done'
}

export function elapsed(ms: number): string {
  const s = Math.max(0, Math.floor(ms / 1000))
  return s < 60 ? `${s}s` : `${Math.floor(s / 60)}m ${s % 60}s`
}

// Kitty graphics: Ghostty or kitty run directly; tmux, screen, herdr and zellij don't pass them through.
export function hasGraphics(env: Record<string, string | undefined>): boolean {
  if (env.TMUX || env.STY || env.HERDR_ENV || env.ZELLIJ) return false
  return env.TERM_PROGRAM === 'ghostty' || Boolean(env.KITTY_WINDOW_ID)
}
