import type { Place, Plan, PlanIndex } from './plan.ts'

/** Content files copied from the Android app's assets (scripts/copy-assets.mjs). */
const BASE = import.meta.env.BASE_URL + 'data/'

export const TRANSLATION = 'elbbk'

export interface BookInfo { nr: number; name: string; abbr: string; chapters: number }
export interface TranslationInfo { id: string; name: string; license?: string; books: BookInfo[] }
export interface Verse { book: number; chapter: number; verse: number; text: string }

export interface MapData { bbox: number[]; land: number[][][]; lakes: number[][][]; rivers: { name: string; line: number[][] }[] }

const cache = new Map<string, Promise<unknown>>()

function load<T>(path: string): Promise<T> {
  let p = cache.get(path)
  if (!p) {
    p = fetch(BASE + path).then((r) => {
      if (!r.ok) throw new Error(`${path}: ${r.status}`)
      return r.json()
    })
    p.catch(() => cache.delete(path))
    cache.set(path, p)
  }
  return p as Promise<T>
}

export const bibleInfo = () => load<TranslationInfo>(`bible/${TRANSLATION}/books.json`)

const book = (nr: number) => load<{ chapters: string[][] }>(`bible/${TRANSLATION}/${String(nr).padStart(2, '0')}.json`)

export async function bookNames(): Promise<Map<number, string>> {
  return new Map((await bibleInfo()).books.map((b) => [b.nr, b.name]))
}

/** Verses [from]..[to] of a chapter; blank = verse omitted in this translation (e.g. Apg 8,37). */
export async function verses(bookNr: number, chapter: number, from: number, to: number): Promise<Verse[]> {
  const ch = (await book(bookNr)).chapters[chapter - 1] ?? []
  const out: Verse[] = []
  for (let v = from; v <= Math.min(to, ch.length); v++) if (ch[v - 1]?.trim()) out.push({ book: bookNr, chapter, verse: v, text: ch[v - 1] })
  return out
}

export async function chapterVerses(bookNr: number, chapter: number): Promise<Verse[]> {
  const ch = (await book(bookNr)).chapters[chapter - 1] ?? []
  return ch.map((text, i) => ({ book: bookNr, chapter, verse: i + 1, text })).filter((v) => v.text.trim())
}

export const planIndex = () => load<PlanIndex>('plans/index.json')
export const plan = (id: string) => load<Plan>(`plans/${id}.json`)

let placesMap: Promise<Map<string, Place>> | null = null
export function places(): Promise<Map<string, Place>> {
  placesMap ??= load<{ places: Place[] }>('places.json').then((p) => new Map(p.places.map((x) => [x.id, x])))
  return placesMap
}

export const mapData = () => load<MapData>('map.json')

/** All available plans (for the album and the atlas). */
export async function availablePlans(): Promise<Plan[]> {
  const index = await planIndex()
  return Promise.all((index.plans ?? []).filter((p) => p.available).map((p) => plan(p.id)))
}
