/**
 * The garden: every completed section lets a tree grow. A tree is fully grown after
 * FIRST sections (the first one) or NEXT sections (all others). Then it moves into the
 * garden and the reader picks the next tree from up to three offers. After the twelve garden
 * trees the tree of life grows at the water (Offb 22,2). After that, every PER_FRUIT
 * sections a fruit ripens, and the golden city at the horizon comes down a bit (Offb 21,2).
 *
 * Everything is derived from the number of completed sections – nothing can shrink.
 * The only stored state is which tree was planted at which position. (Port of data/garden/Garden.kt.)
 */
export const FIRST = 30
export const NEXT = 40
export const TREES = 12
export const PER_FRUIT = 4
export const CITY_STEPS = 36
export const LIFE = 'leben'

/** The twelve garden trees; the first one is always the mustard tree. */
export const ORDER = ['senf', 'oel', 'feige', 'mandel', 'palme', 'zeder', 'wasser', 'granat', 'maulbeer', 'tamariske', 'terebinthe', 'akazie']

/** Sections needed for tree [i] (0-based; 12 = tree of life). */
export const need = (i: number) => (i === 0 ? FIRST : NEXT)

/** Sections until the tree of life is fully grown. */
export const AFTER_LIFE = FIRST + TREES * NEXT

export interface GardenProgress {
  /** fully grown trees (0..13, 13 = tree of life grown too) */
  done: number
  /** sections (may be fractional while animating) into the growing tree */
  inTree: number
  /** sections the growing tree needs */
  need: number
  /** ripe fruits on the tree of life */
  fruits: number
  /** growth 0..1 of the tree that is growing now */
  t: number
}

export function progress(total: number): GardenProgress {
  let i = 0
  let left = Math.max(0, total)
  while (i <= TREES && left >= need(i)) {
    left -= need(i)
    i++
  }
  const fruits = total < AFTER_LIFE ? 0 : Math.floor((total - AFTER_LIFE) / PER_FRUIT)
  const inTree = i > TREES ? 0 : left
  const n = need(Math.min(i, TREES))
  return { done: i, inTree, need: n, fruits, t: i > TREES ? 1 : Math.min(1, Math.max(0, inTree / n)) }
}

/** True when a tree is grown but the next one has not been chosen yet. [planted] starts with the mustard tree. */
export function choicePending(total: number, planted: string[]): boolean {
  const done = progress(total).done
  return planted.length <= done && planted.length <= TREES
}

/**
 * Up to three trees to choose from. When fewer are left, fewer are offered; after the twelve
 * garden trees only the tree of life. Rotates with every choice, so a tree not taken comes back later.
 */
export function offers(planted: string[]): string[] {
  const rest = ORDER.filter((id) => !planted.includes(id))
  if (rest.length === 0) return planted.includes(LIFE) ? [] : [LIFE]
  const offset = planted.length - 1
  return Array.from({ length: Math.min(3, rest.length) }, (_, k) => rest[(offset + k) % rest.length])
}
