<script lang="ts">
  import Confetti from './lib/components/Confetti.svelte'
  import Home from './screens/Home.svelte'
  import Session from './screens/session/Session.svelte'
  import Verse from './screens/Verse.svelte'
  import Plans from './screens/Plans.svelte'
  import Bible from './screens/Bible.svelte'
  import Album from './screens/Album.svelte'
  import Settings from './screens/Settings.svelte'
  import Habit from './screens/Habit.svelte'
  import Install from './screens/Install.svelte'
  import { store } from './lib/data/store.svelte.ts'
  import { theme } from './lib/ui/theme.svelte.ts'
  import { router } from './lib/router.svelte.ts'
  import { update } from './lib/ui/update.svelte.ts'

  $effect(() => {
    void theme.dark
    void store.settings.textScale
    theme.apply()
    document.documentElement.classList.toggle('calm', store.settings.calm)
  })

  const parts = $derived(router.path.split('/').filter(Boolean))
</script>

{#if !store.ready}
  <div class="spinner" style="margin-top:40dvh"></div>
{:else}
  {#key router.path}
    {#if parts[0] === 'session'}
      <Session more={parts[1] === 'more'} />
    {:else if parts[0] === 'verse'}
      <Verse />
    {:else if parts[0] === 'plans'}
      <Plans />
    {:else if parts[0] === 'bible'}
      <Bible book={parts[1] ? Number(parts[1]) : undefined} chapter={parts[2] ? Number(parts[2]) : undefined} />
    {:else if parts[0] === 'album'}
      <Album />
    {:else if parts[0] === 'settings'}
      <Settings />
    {:else if parts[0] === 'habit'}
      <Habit />
    {:else if parts[0] === 'install'}
      <Install />
    {:else}
      <Home />
    {/if}
  {/key}
{/if}

{#if update.needed}
  <div class="update" role="status">
    <span class="grow">Eine neue Version von Manna ist da.</span>
    <button class="btn text" style="color:inherit" onclick={() => update.apply()}>Neu laden</button>
  </div>
{/if}

<Confetti />

<style>
  .update {
    position: fixed; left: 12px; right: 12px; bottom: calc(12px + var(--safe-bottom)); z-index: 50; margin: 0 auto; max-width: 520px;
    display: flex; align-items: center; gap: 8px; padding: 6px 6px 6px 18px; border-radius: 14px;
    background: var(--on-surface); color: var(--surface); box-shadow: 0 6px 24px rgba(0, 0, 0, 0.2);
  }
</style>
