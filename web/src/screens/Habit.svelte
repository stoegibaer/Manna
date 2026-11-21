<script lang="ts">
  import TopBar from '../lib/components/TopBar.svelte'
  import Icon from '../lib/components/Icon.svelte'
  import { store } from '../lib/data/store.svelte.ts'
  import { router } from '../lib/router.svelte.ts'

  /**
   * „Nach dem ___ lese ich einen Vers.“ – the if-then plan, a plan B and the weekly goal.
   * (The web app sends no reminders; the plan is shown on the home screen until you have read.)
   */
  const ANCHORS = ['dem Aufstehen', 'dem ersten Kaffee', 'dem Frühstück', 'der Mittagspause', 'dem Heimkommen', 'dem Abendessen', 'dem Zähneputzen am Abend']
  const PLAN_B = ['vor dem Schlafengehen', 'direkt nach dem Abendessen', 'bevor ich das Handy weglege']

  let anchor = $state(store.settings.anchorText || 'dem ersten Kaffee')
  let planB = $state(store.settings.planB)
  let goal = $state(store.settings.weeklyGoal)

  function save() {
    store.updateSettings((s) => ({ ...s, anchorText: anchor.trim(), planB: planB.trim(), weeklyGoal: goal, reminderSetupSeen: true }))
    router.back()
  }
</script>

<div class="page">
  <TopBar title="Wenn-dann-Plan" onback={() => router.back()} />
  <div class="content stack-12" style="padding-bottom:calc(32px + var(--safe-bottom))">
    <p class="muted" style="margin:0">Ein Vers am Tag reicht. Verknüpf das Lesen mit etwas, das du sowieso jeden Tag tust – dann vergisst man es seltener.</p>

    <p class="t-ll primary" style="padding-top:12px">Nach …</p>
    <div class="chips">
      {#each ANCHORS as a (a)}
        <button class="chip" class:on={anchor === a} onclick={() => (anchor = a)}>{#if anchor === a}<Icon name="check" size={18} />{/if}{a}</button>
      {/each}
    </div>
    <input type="text" bind:value={anchor} placeholder="oder eigener Anker" aria-label="Eigener Anker" />

    <p class="t-ll primary" style="padding-top:12px">Plan B – wenn ich es verpasse, dann …</p>
    <div class="chips">
      {#each PLAN_B as b (b)}
        <button class="chip" class:on={planB === b} onclick={() => (planB = planB === b ? '' : b)}>{#if planB === b}<Icon name="check" size={18} />{/if}{b}</button>
      {/each}
    </div>
    <input type="text" bind:value={planB} placeholder="oder eigener Plan B" aria-label="Eigener Plan B" />

    <!-- the if-then sentence – said out loud it sticks better -->
    <div class="ok stack-6" style="border-radius:16px;padding:16px;margin-top:4px">
      <p style="margin:0;font-weight:600">Nach {anchor.trim() || '…'} lese ich einen Vers.</p>
      {#if planB.trim()}<p style="margin:0">Wenn ich es verpasse, dann {planB.trim()}.</p>{/if}
      <p class="t-bs" style="margin:0">Manna zeigt dir den Satz auf der Startseite, bis du heute gelesen hast.</p>
    </div>

    <p class="t-ll primary" style="padding-top:12px">Wochenziel</p>
    <p class="t-tm">{goal === 7 ? 'Jeden Tag' : `${goal} von 7 Tagen`}</p>
    <input type="range" min="1" max="7" step="1" bind:value={goal} aria-label="Wochenziel" />
    <p class="t-bs muted">Verpasste Tage zählen nicht gegen dich – jede Woche fängt neu an.</p>

    <div style="height:8px"></div>
    <button class="btn" onclick={save}>Speichern</button>
  </div>
</div>

<style>
  .stack-6 { display: flex; flex-direction: column; gap: 6px; }
</style>
