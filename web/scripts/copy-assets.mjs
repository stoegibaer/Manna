// Copies the app's content (Bible, plans, map, sounds) from the Android project into public/,
// so both apps always share the same JSON files. Output is git-ignored.
import { cpSync, mkdirSync, readdirSync, rmSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = join(dirname(fileURLToPath(import.meta.url)), '..')
const assets = join(root, '..', 'app', 'src', 'main', 'assets')
const raw = join(root, '..', 'app', 'src', 'main', 'res', 'raw')
const data = join(root, 'public', 'data')
const sounds = join(root, 'public', 'sounds')

rmSync(data, { recursive: true, force: true })
rmSync(sounds, { recursive: true, force: true })
mkdirSync(data, { recursive: true })
mkdirSync(sounds, { recursive: true })
for (const name of ['bible', 'plans', 'map.json', 'places.json']) {
  cpSync(join(assets, name), join(data, name), { recursive: true })
}
for (const f of readdirSync(raw).filter((f) => f.endsWith('.wav'))) cpSync(join(raw, f), join(sounds, f))
console.log('assets copied')
