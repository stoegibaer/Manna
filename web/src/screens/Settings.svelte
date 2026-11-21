<script lang="ts">
  import TopBar from '../lib/components/TopBar.svelte'
  import Switch from '../lib/components/Switch.svelte'
  import { store } from '../lib/data/store.svelte.ts'
  import type { Settings, ThemeMode } from '../lib/data/types.ts'
  import { BackupError, WEB_VERSION, importBackup, saveBackup } from '../lib/data/backup.ts'
  import { canSpeak } from '../lib/audio/speaker.svelte.ts'
  import { install } from '../lib/ui/install.svelte.ts'
  import { router } from '../lib/router.svelte.ts'

  const s = $derived(store.settings)
  const set = (f: (s: Settings) => Settings) => store.updateSettings(f)
  let message = $state<string | null>(null)
  let busy = $state(false)
  let fileInput: HTMLInputElement

  async function job(f: () => Promise<string>) {
    busy = true
    try { message = await f() }
    catch (e) { message = e instanceof BackupError ? e.message : `Das hat nicht geklappt: ${(e as Error).message}` }
    busy = false
  }

  const modes: [ThemeMode, string][] = [['SYSTEM', 'System'], ['LIGHT', 'Hell'], ['DARK', 'Dunkel']]
</script>

{#snippet group(title: string)}
  <p class="t-ll primary" style="padding:20px 0 4px">{title}</p>
{/snippet}

{#snippet toggle(title: string, subtitle: string | null, checked: boolean, onchange: (v: boolean) => void, disabled = false)}
  <div class="row" style="padding:8px 0;gap:12px">
    <div class="grow">
      <p class="t-tm" style="color:{disabled ? 'var(--on-surface-variant)' : 'var(--on-surface)'}">{title}</p>
      {#if subtitle}<p class="t-bm muted">{subtitle}</p>{/if}
    </div>
    <Switch {checked} {disabled} {onchange} label={title} />
  </div>
{/snippet}

<div class="page">
  <TopBar title="Einstellungen" onback={() => router.back()} />
  <div class="content stack-4" style="padding-bottom:calc(32px + var(--safe-bottom))">
    {@render group('Gewohnheit')}
    <button class="tile" style="border-radius:14px;padding:16px" onclick={() => router.go('habit')}>
      <span class="t-tm" style="display:block">Wenn-dann-Plan & Wochenziel</span>
      <span class="t-bm muted">{s.anchorText.trim() ? `Nach ${s.anchorText.trim()} · ` : ''}Ziel {s.weeklyGoal} Tage pro Woche</span>
    </button>

    {@render group('Lesen')}
    {@render toggle('Fokusmodus', 'Immer nur ein Vers ist hell – tippen zum Weiterlesen.', s.focusMode, (v) => set((x) => ({ ...x, focusMode: v })))}
    <p class="t-tm" style="padding-top:12px">Textgröße</p>
    <input type="range" min="0.8" max="1.6" step="0.1" value={s.textScale} aria-label="Textgröße"
      oninput={(e) => { const v = Number((e.target as HTMLInputElement).value); set((x) => ({ ...x, textScale: Math.round(v * 10) / 10 })) }} />
    <p class="bible" style="margin:0">Der Gerechte aber wird durch seinen Glauben leben.</p>

    {#if canSpeak}
      <p class="t-tm" style="padding-top:12px">Vorlese-Tempo</p>
      <input type="range" min="0.7" max="1.4" step="0.1" value={s.ttsRate} aria-label="Vorlese-Tempo"
        oninput={(e) => { const v = Number((e.target as HTMLInputElement).value); set((x) => ({ ...x, ttsRate: Math.round(v * 10) / 10 })) }} />
      <p class="t-bs muted">{s.ttsRate < 0.95 ? 'Etwas langsamer' : s.ttsRate > 1.05 ? 'Etwas schneller' : 'Normal'}</p>
    {/if}

    {@render group('Rückmeldung')}
    {@render toggle('Ruhiger Modus', 'Keine Animationen, kein Konfetti, keine Töne.', s.calm, (v) => set((x) => ({ ...x, calm: v })))}
    {@render toggle('Töne', null, s.sound, (v) => set((x) => ({ ...x, sound: v })), s.calm)}
    {@render toggle('Konfetti', null, s.confetti, (v) => set((x) => ({ ...x, confetti: v })), s.calm)}

    {@render group('Darstellung')}
    <div class="segmented" role="radiogroup" aria-label="Darstellung">
      {#each modes as [mode, label] (mode)}
        <button role="radio" aria-checked={s.theme === mode} class:on={s.theme === mode} onclick={() => set((x) => ({ ...x, theme: mode }))}>{label}</button>
      {/each}
    </div>

    {@render group('Daten sichern')}
    <p class="t-bm muted">
      Speichert Fortschritt, Karten, Verse, Tagebuch und Einstellungen in einer Datei – etwa für ein neues Handy.
      Die Datei passt auch zur Android-App. Beim Einlesen wird zusammengeführt: Was schon da ist, bleibt erhalten.
    </p>
    {#if !store.persistent}
      <p class="t-bm" style="color:var(--error)">Dieser Browser speichert gerade nichts dauerhaft (z. B. privates Fenster). Sichere deinen Fortschritt vor dem Schließen.</p>
    {/if}
    <button class="btn tonal" style="margin-top:8px" disabled={busy} onclick={() => job(saveBackup)}>Sicherung speichern</button>
    <button class="btn outline" style="height:48px" disabled={busy} onclick={() => fileInput.click()}>Sicherung einlesen</button>
    <input bind:this={fileInput} type="file" accept=".json,application/json,text/plain" hidden
      onchange={(e) => { const f = (e.target as HTMLInputElement).files?.[0]; (e.target as HTMLInputElement).value = ''; if (f) void job(() => importBackup(f)) }} />
    {#if message}<p class="t-bm secondary" style="padding-top:4px">{message}</p>{/if}

    {#if !install.standalone}
      {@render group('App')}
      <button class="tile" style="border-radius:14px;padding:16px" onclick={() => router.go('install')}>
        <span class="t-tm" style="display:block">Auf den Home-Bildschirm</span>
        <span class="t-bm muted">So startet Manna wie eine App und funktioniert ohne Internet.</span>
      </button>
    {/if}

    <hr class="divider" style="margin:16px 0" />
    <p class="t-bs muted">
      Bibeltext: Elberfelder Übersetzung, Edition bibelkommentare.de. © 2019 Verbreitung des christlichen Glaubens e.V.,
      lizenziert unter <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/deed.de" target="_blank" rel="noopener">CC BY-NC-ND 4.0</a>.
      Karte: Natural Earth (gemeinfrei). Manna Web {WEB_VERSION} – deine Daten bleiben auf diesem Gerät.
    </p>
  </div>
</div>

<style>
  .segmented { display: flex; border: 1px solid var(--outline); border-radius: 100px; overflow: hidden; margin: 8px 0; }
  .segmented button { flex: 1; height: 40px; border: 0; background: transparent; cursor: pointer; font-size: 14px; font-weight: 500; }
  .segmented button + button { border-left: 1px solid var(--outline); }
  .segmented button.on { background: var(--secondary-container); color: var(--on-secondary-container); }
  a { color: var(--primary); }
</style>
