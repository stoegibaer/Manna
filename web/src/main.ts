import { mount } from 'svelte'
import './app.css'
import App from './App.svelte'
import { store } from './lib/data/store.svelte.ts'
import { unlockAudioOnFirstTouch } from './lib/audio/feedback.ts'
import { update } from './lib/ui/update.svelte.ts'

void store.init()
unlockAudioOnFirstTouch()
// ask the browser to keep Manna's data (it may still decide on its own)
void navigator.storage?.persist?.().catch(() => {})
if (import.meta.env.PROD) update.start()

mount(App, { target: document.getElementById('app')! })
