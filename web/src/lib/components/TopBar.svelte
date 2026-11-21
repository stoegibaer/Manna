<script lang="ts">
  import type { Snippet } from 'svelte'
  import Icon from './Icon.svelte'

  let { title = '', onback, close = false, actions }: { title?: string; onback: () => void; close?: boolean; actions?: Snippet } = $props()
</script>

<header class="bar">
  <button class="icon-btn" onclick={onback} aria-label={close ? 'Schließen' : 'Zurück'}>
    <Icon name={close ? 'close' : 'back'} />
  </button>
  <h1 class="title" class:small={close}>{title}</h1>
  {#if actions}{@render actions()}{/if}
</header>

<style>
  .bar {
    position: sticky; top: 0; z-index: 5; display: flex; align-items: center; gap: 4px;
    padding: calc(var(--safe-top) + 4px) 8px 4px 4px; min-height: 64px; background: var(--background);
  }
  .title { flex: 1; min-width: 0; margin: 0 0 0 4px; font-size: 22px; line-height: 28px; font-weight: 400; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .title.small { font-size: 16px; font-weight: 500; color: var(--on-surface-variant); }
</style>
