// claude plugin test <mod> — the brand spinner.
import { describe, expect, mock, test } from 'claude-code/testing'

import { BRAND } from './brand'
import { glintPos, hasGraphics, shimmerAt, square } from './spinner'

const SPIN = { component: 'Spinner', props: { word: 'Baking', message: null, suffix: '…', mode: 'tool-use' } } as const

function world(on: any, env: Record<string, string> = {}) {
  mock.clock(on)
  const stored = new Map<string, unknown>()
  on('store.get', ($: any, e: any) => ({ value: stored.get(e.key) }))
  on('store.set', ($: any, e: any) => {
    stored.set(e.key, e.value)
    return { value: undefined }
  })
  mock.env(on, env)
  on('command.register', ($: any, e: any) => ({ value: { command: e.name } }))
  on('session.start', ($: any, e: any) => ({ cwd: e.cwd }))
  on('ui.render', () => <Box key="engine" />)
  return stored
}
const Box = 'Box' as any
const start = ($: any) => $.session.start({ cwd: '/w', surface: 'terminal', isInteractive: true })
const mount = ($: any, surface: 'terminal' | 'desktop' = 'terminal') =>
  $.ui.mount({ plugin: `${BRAND.slug}-spinner`, surface, ...SPIN } as any)

describe('brand spinner', () => {
  test('the hole turns clockwise every 150 ms', () => {
    const at = (ms: number) => square(ms, -99).map(c => c.ch).join('')
    expect([0, 150, 300, 450, 600].map(at)).toEqual(['▄▀', '▀▄', '▀▀', '▀▀', '▄▀'])
  })

  test('one glint: the square, then the word', () => {
    expect(square(450, -3)[0]?.color).toBe('#FFFFFF')
    expect(shimmerAt('Hola', 2).map(c => c.color).indexOf('#FFFFFF')).toBe(2)
    expect(glintPos(8, 0)).toBe(-5)
  })

  test('graphics only in Ghostty or kitty run directly', () => {
    expect(hasGraphics({ TERM_PROGRAM: 'ghostty' })).toBe(true)
    expect(hasGraphics({ TERM_PROGRAM: 'ghostty', HERDR_ENV: '1' })).toBe(false)
    expect(hasGraphics({ TERM_PROGRAM: 'Apple_Terminal' })).toBe(false)
  })

  test('replaces the engine spinner in the terminal and the desktop app', async ($, on) => {
    world(on)
    await start($)
    for (const surface of ['terminal', 'desktop'] as const) {
      const ui = await mount($, surface)
      expect(await ui.find({ type: 'Box', key: 'engine' })).toBeUndefined()
      await ui.unmount()
    }
  })

  test('/<brand>-spinner off restores the engine spinner and is remembered', async ($, on) => {
    const stored = world(on)
    await start($)
    await $.command.run({ command: BRAND.command, args: 'off' } as any)
    expect(stored.get('spinner')).toBe('off')
    await start($)
    const ui = await mount($)
    expect(await ui.find({ type: 'Box', key: 'engine' })).toBeDefined()
    await ui.unmount()
  })
})
