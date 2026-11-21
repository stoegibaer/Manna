import { LIFE, ORDER } from '../data/garden.ts'
import { branchy, cedar, mustard, palm, type Model } from './treeModel.ts'

/** Colors of one tree species. */
export interface TreeColors {
  trunk: string; leaf: string; leafDark: string; leafLight?: string
  flower?: string; flowerCenter?: string
  fruit?: string; fruitDark?: string; ripe?: string; trunkDark?: string
}

export type LeafShape = 'ELLIPSE' | 'LOBED' | 'ROUND' | 'NONE'
/** CROSS = four petals as the mustard tree has always had them. */
export type FlowerKind = 'BLOSSOM' | 'BALL' | 'PLUME' | 'CROSS'
export type FruitKind = 'ROUND' | 'OVAL' | 'PEAR' | 'CROWN'
export type Finale = 'BIRDS_NEST' | 'DOVE' | 'FIGS' | 'PETALS' | 'PALM_BIRDS' | 'CEDAR_BIRDS' | 'SPARKLE_WHITE' | 'SPARKLE_GOLD' | 'ZACCHAEUS' | 'SPARKLE_PINK' | 'TENT'

/** One tree species with its verse (port of ui/garden/Trees.kt). */
export interface TreeSpecies {
  id: string
  name: string
  /** „Dein“/„Deine“ for „Dein Senfbaum ist gewachsen“ */
  article: string
  ref: string
  verse: string
  finaleText: string
  finale: Finale | null
  build: () => Model
  light: TreeColors
  dark: TreeColors
  leafShape?: LeafShape
  leafW?: number
  flat?: number
  petals?: number
  flowerKind?: FlowerKind
  fruitKind?: FruitKind
  strandW?: number
  /** Shows a little brook at its foot when shown alone (Ps 1,3). */
  water?: boolean
}

const models = new Map<string, Model>()
export function modelOf(sp: TreeSpecies): Model {
  let m = models.get(sp.id)
  if (!m) { m = sp.build(); models.set(sp.id, m) }
  return m
}

const h = (v: number) => '#' + v.toString(16).padStart(6, '0').toUpperCase()

export const ALL: TreeSpecies[] = [
  {
    id: 'senf', name: 'Senfbaum', article: 'Dein', ref: 'Mk 4,32',
    verse: '… und große Zweige treibt, so dass unter seinem Schatten die Vögel des Himmels sich niederlassen können.',
    finaleText: 'Die Vögel kommen und bauen ein Nest.', finale: 'BIRDS_NEST',
    build: mustard,
    light: { trunk: h(0x7a5c3e), leaf: h(0x5e9e62), leafDark: h(0x3f7a4a), flower: h(0xe8b931) },
    dark: { trunk: h(0xb08a63), leaf: h(0x7fbf84), leafDark: h(0x5a9b66), flower: h(0xf2c94c) },
    flowerKind: 'CROSS',
  },
  {
    id: 'oel', name: 'Ölbaum', article: 'Dein', ref: 'Ps 52,10',
    verse: 'Ich aber bin wie ein grüner Olivenbaum im Haus Gottes; ich vertraue auf die Güte Gottes immer und ewiglich.',
    finaleText: 'Die Taube kommt mit dem Olivenblatt (1 Mo 8,11).', finale: 'DOVE',
    build: () => branchy({ seed: 33, depth: 5, trunkLen: 0.28, trunkW: 0.05, trunkCurve: 18, spread: [16, 34], leaf: true, leafCount: 5, leafLen: 0.038, fruit: { p: 0.6, r: 0.01, from: 0.72 } }),
    light: { trunk: h(0x7c6a55), leaf: h(0x8fa587), leafDark: h(0x5f7a5e), fruit: h(0x7e9a3c) },
    dark: { trunk: h(0xa8957c), leaf: h(0x9db394), leafDark: h(0x6f8c6c), fruit: h(0xa9c266) },
    leafW: 0.16, fruitKind: 'OVAL',
  },
  {
    id: 'feige', name: 'Feigenbaum', article: 'Dein', ref: 'Mi 4,4',
    verse: 'Und sie werden sitzen, jeder unter seinem Weinstock und unter seinem Feigenbaum, und niemand wird sie aufschrecken.',
    finaleText: 'Die Feigen reifen.', finale: 'FIGS',
    build: () => branchy({ seed: 5, depth: 4, trunkLen: 0.16, trunkW: 0.06, trunkKids: 3, spread: [30, 62], lenF: [0.75, 0.9], sideBoost: 1.2, leaf: true, leafCount: 3, leafLen: 0.085, fruit: { p: 0.9, r: 0.016, from: 0.7 } }),
    light: { trunk: h(0x8a8073), leaf: h(0x6fa35a), leafDark: h(0x4c7f42), fruit: h(0x9db35a), ripe: h(0x6e4a7a) },
    dark: { trunk: h(0xb3a898), leaf: h(0x8cc077), leafDark: h(0x649a58), fruit: h(0xb6c977), ripe: h(0xa07ab0) },
    leafShape: 'LOBED', fruitKind: 'PEAR',
  },
  {
    id: 'mandel', name: 'Mandelbaum', article: 'Dein', ref: 'Jer 1,11–12',
    verse: 'Ich sehe einen Mandelstab. Und der HERR sprach zu mir: Du hast recht gesehen; denn ich werde über mein Wort wachen, es auszuführen.',
    finaleText: 'Er blüht als Erster, Blütenblätter fallen leise.', finale: 'PETALS',
    build: () => branchy({ seed: 27, depth: 5, trunkLen: 0.26, trunkW: 0.045, curve: 22, spread: [20, 40], leaf: true, leafFrom: 2, leafCount: 3, leafLen: 0.04, flower: { p: 0.7, r: 0.018, from: 0.4, spread: 0.4, along: 3 }, fruit: { p: 0.35, r: 0.012, from: 0.85 } }),
    light: { trunk: h(0x5a463a), leaf: h(0x8dba6e), leafDark: h(0x6e9a55), flower: h(0xfbeff2), flowerCenter: h(0xd07a8c), fruit: h(0xa4b27a) },
    dark: { trunk: h(0x9a8072), leaf: h(0x9fcb82), leafDark: h(0x7daa66), flower: h(0xf5e6ea), flowerCenter: h(0xd77a90), fruit: h(0xb8c690) },
    leafW: 0.22, petals: 5, fruitKind: 'OVAL',
  },
  {
    id: 'palme', name: 'Palme', article: 'Deine', ref: 'Ps 92,13',
    verse: 'Der Gerechte wird sprossen wie der Palmbaum, wie eine Zeder auf dem Libanon wird er emporwachsen.',
    finaleText: 'Zwei Vögel setzen sich in die Krone.', finale: 'PALM_BIRDS',
    build: () => palm({ seed: 4, height: 0.8, lean: 0.08, trunkW: 0.032, fronds: 11, frondLen: 0.3, droop: 0.4 }),
    light: { trunk: h(0x9a7b55), leaf: h(0x6e9e4e), leafDark: h(0x4e7d3c), trunkDark: h(0x7a5f40) },
    dark: { trunk: h(0xc2a27c), leaf: h(0x8dbf6c), leafDark: h(0x6a9a55), trunkDark: h(0x9c805e) },
  },
  {
    id: 'zeder', name: 'Zeder', article: 'Deine', ref: 'Ps 104,16–17',
    verse: 'Es werden gesättigt die Bäume des HERRN, die Zedern des Libanon, die er gepflanzt hat, worin die Vögel nisten …',
    finaleText: 'Vögel nisten in den Zweigen.', finale: 'CEDAR_BIRDS',
    build: () => cedar({ seed: 6, height: 0.85, trunkW: 0.04, tiers: 8, span: 0.34, sag: 0.03, pad: 0.05, flat: 0.55 }),
    light: { trunk: h(0x6e5241), leaf: h(0x4f7a62), leafDark: h(0x355c4a), leafLight: h(0x6f977d) },
    dark: { trunk: h(0xa68a74), leaf: h(0x6e9c82), leafDark: h(0x4f7c66), leafLight: h(0x8db59c) },
  },
  {
    id: 'wasser', name: 'Baum am Wasser', article: 'Dein', ref: 'Ps 1,3',
    verse: 'Und er ist wie ein Baum, gepflanzt an Wasserbächen, der seine Frucht bringt zu seiner Zeit und dessen Blatt nicht verwelkt.',
    finaleText: 'Das Wasser glitzert, und er trägt Frucht zu seiner Zeit.', finale: 'SPARKLE_WHITE',
    build: () => branchy({ seed: 19, depth: 4, trunkLen: 0.26, trunkW: 0.055, spread: [24, 48], leaf: true, leafCount: 4, leafLen: 0.04, clumpAlong: 1, clumpR: 0.06, tipClump: 0.065, fruit: { p: 0.9, r: 0.014, from: 0.72 } }),
    light: { trunk: h(0x6f5a47), leaf: h(0x5e9e62), leafDark: h(0x3f7a4a), leafLight: h(0x7db57e), fruit: h(0xc2493a) },
    dark: { trunk: h(0xa8917a), leaf: h(0x7fbf84), leafDark: h(0x5a9b66), leafLight: h(0x9bd0a0), fruit: h(0xe0735f) },
    leafShape: 'ROUND', water: true,
  },
  {
    id: 'granat', name: 'Granatapfel', article: 'Dein', ref: '5 Mo 8,8',
    verse: 'ein Land von Weizen und Gerste und Weinstöcken und Feigenbäumen und Granatbäumen; ein Land von ölreichen Olivenbäumen und Honig;',
    finaleText: 'Die Früchte werden rot.', finale: 'SPARKLE_GOLD',
    build: () => branchy({ seed: 37, depth: 5, trunkLen: 0.22, trunkW: 0.04, spread: [20, 42], leaf: true, leafCount: 4, leafLen: 0.03, flower: { p: 0.9, r: 0.016, from: 0.5, along: 3 }, fruit: { p: 0.5, r: 0.02, from: 0.78 } }),
    light: { trunk: h(0x6e5a4b), leaf: h(0x5e9a4e), leafDark: h(0x3f7a3c), flower: h(0xe8743a), flowerCenter: h(0xf2c94c), fruit: h(0xc0392b), fruitDark: h(0x8e2a1f) },
    dark: { trunk: h(0xa8917f), leaf: h(0x7db86b), leafDark: h(0x5c9a55), flower: h(0xf08a55), flowerCenter: h(0xf2c94c), fruit: h(0xe05a48), fruitDark: h(0xb04436) },
    leafW: 0.3, petals: 5, fruitKind: 'CROWN',
  },
  {
    id: 'maulbeer', name: 'Maulbeerfeigenbaum', article: 'Dein', ref: 'Lk 19,4',
    verse: 'Und er lief voraus und stieg auf einen Maulbeerfeigenbaum, damit er ihn sähe; denn er sollte dort durchkommen.',
    finaleText: 'Zachäus sitzt im Baum.', finale: 'ZACCHAEUS',
    build: () => branchy({ seed: 23, depth: 4, trunkLen: 0.16, trunkW: 0.08, trunkKids: 4, spread: [30, 54], lenF: [0.74, 0.86], sideBoost: 1.1, squash: 0.75, leaf: true, leafCount: 3, leafLen: 0.035, clumpAlong: 2, clumpR: 0.065, tipClump: 0.07, fruit: { p: 0.4, r: 0.01, from: 0.75 } }),
    light: { trunk: h(0x8c7b66), leaf: h(0x6b9a52), leafDark: h(0x4d7b40), leafLight: h(0x88b26c), fruit: h(0xc98a5a) },
    dark: { trunk: h(0xb5a48e), leaf: h(0x88b86e), leafDark: h(0x669757), leafLight: h(0xa3ca88), fruit: h(0xe0a878) },
    leafShape: 'ROUND', flat: 0.6,
  },
  {
    id: 'tamariske', name: 'Tamariske', article: 'Deine', ref: '1 Mo 21,33',
    verse: 'Und Abraham pflanzte eine Tamariske in Beerseba und rief dort den Namen des HERRN, des ewigen Gottes, an.',
    finaleText: 'Rosa Blütenrispen erscheinen.', finale: 'SPARKLE_PINK',
    build: () => branchy({ seed: 16, depth: 5, trunkLen: 0.22, trunkW: 0.045, curve: 30, spread: [20, 44], strands: 3, strandFrom: 3, strandLen: 0.08, droop: 0.4, flower: { p: 0.7, r: 0.02, from: 0.6, along: 4 } }),
    light: { trunk: h(0x6b5a50), leaf: h(0x8fa89a), leafDark: h(0x6e8a7c), flower: h(0xd98aae) },
    dark: { trunk: h(0xa39187), leaf: h(0xa3bdb0), leafDark: h(0x7f9c8e), flower: h(0xe7a6c0) },
    leafShape: 'NONE', flowerKind: 'PLUME', strandW: 0.004,
  },
  {
    id: 'terebinthe', name: 'Terebinthe', article: 'Deine', ref: '1 Mo 18,1',
    verse: 'Und der HERR erschien ihm bei den Terebinthen Mamres; und er saß an dem Eingang des Zeltes bei der Hitze des Tages.',
    finaleText: 'Ein Zelt steht in ihrem Schatten.', finale: 'TENT',
    build: () => branchy({ seed: 31, depth: 4, trunkLen: 0.2, trunkW: 0.09, spread: [28, 50], lenF: [0.74, 0.88], gnarl: 14, leaf: true, leafCount: 3, leafLen: 0.03, clumpAlong: 2, clumpR: 0.075, tipClump: 0.085, fruit: { p: 0.3, r: 0.007, from: 0.8 } }),
    light: { trunk: h(0x6a5644), leaf: h(0x6a8f4e), leafDark: h(0x4b6e3a), leafLight: h(0x87a86a), fruit: h(0xb0475a) },
    dark: { trunk: h(0xa89278), leaf: h(0x86ad69), leafDark: h(0x638c52), leafLight: h(0xa2c485), fruit: h(0xd06a7c) },
    leafShape: 'ROUND',
  },
  {
    id: 'akazie', name: 'Akazie', article: 'Deine', ref: 'Jes 41,19',
    verse: 'Ich werde Zedern in die Wüste setzen, Akazien und Myrten und Olivenbäume …',
    finaleText: 'Gelbe Blütenkugeln leuchten.', finale: 'SPARKLE_GOLD',
    build: () => branchy({ seed: 13, depth: 4, trunkLen: 0.24, trunkW: 0.045, trunkKids: 3, spread: [22, 34], up: 0.05, lenF: [0.82, 0.95], squash: 0.6, tipClump: 0.09, clumpAlong: 1, clumpFrom: 3, clumpR: 0.07, flower: { p: 0.9, r: 0.016, from: 0.7 } }),
    light: { trunk: h(0x6e5a48), leaf: h(0x7e9a4e), leafDark: h(0x5c7a3a), leafLight: h(0x9ab46a), flower: h(0xe8b931) },
    dark: { trunk: h(0xa8927e), leaf: h(0x9ab66a), leafDark: h(0x789655), leafLight: h(0xb3cb86), flower: h(0xf2c94c) },
    leafShape: 'NONE', flat: 0.38, flowerKind: 'BALL',
  },
]

export const LIFE_TREE: TreeSpecies = {
  id: LIFE, name: 'Baum des Lebens', article: 'Dein', ref: 'Offb 22,2',
  verse: '… der Baum des Lebens, der zwölf Früchte trägt und jeden Monat seine Frucht gibt; und die Blätter des Baumes sind zur Heilung der Nationen.',
  finaleText: 'Ab jetzt reift alle 4 Abschnitte eine Frucht.', finale: 'SPARKLE_GOLD',
  build: () => branchy({ seed: 77, depth: 5, trunkLen: 0.26, trunkW: 0.07, spread: [24, 46], leaf: true, leafCount: 3, leafLen: 0.04, clumpAlong: 1, clumpR: 0.06, tipClump: 0.07, fruit: { p: 1, r: 0.024, from: 0.6 } }),
  light: { trunk: h(0x7a5c3e), leaf: h(0x4f9e6a), leafDark: h(0x2f7d4f), leafLight: h(0x7cc28f), fruit: h(0xc0392b) },
  dark: { trunk: h(0xb08a63), leaf: h(0x6fbf88), leafDark: h(0x4f9e6a), leafLight: h(0x9ad6aa), fruit: h(0xe05a48) },
}

/** Twelve fruits for twelve months (Offb 22,2). */
export const LIFE_FRUITS = [0xc0392b, 0xe8b931, 0x8e44ad, 0xe67e22, 0xd35482, 0x7e9a3c, 0x2e86ab, 0xc98a2e, 0xb04436, 0xf2c94c, 0x6e4a7a, 0xe05a48].map(h)

const byIdMap = new Map([...ALL, LIFE_TREE].map((s) => [s.id, s]))
export const treeById = (id: string): TreeSpecies => byIdMap.get(id) ?? ALL[0]

/** „Dein Senfbaum“, „Deine Palme“ … */
export const treeTitle = (id: string) => { const s = treeById(id); return `${s.article} ${s.name}` }
export const treeName = (id: string) => treeById(id).name

export { ORDER }
