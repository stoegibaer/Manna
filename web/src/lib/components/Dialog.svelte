<script lang="ts">
  import type { Snippet } from 'svelte'

  let { onclose, children, wide = false }: { onclose: () => void; children: Snippet; wide?: boolean } = $props()
  function key(e: KeyboardEvent) { if (e.key === 'Escape') onclose() }
</script>

<svelte:window onkeydown={key} />

<div class="scrim" onclick={onclose} role="presentation"></div>
<div class="wrap" role="presentation" onclick={(e) => { if (e.target === e.currentTarget) onclose() }}>
  <div class="dialog" class:wide role="dialog" aria-modal="true">{@render children()}</div>
</div>

<style>
  .scrim { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.32); z-index: 40; }
  .wrap {
    position: fixed; inset: 0; z-index: 41; display: flex; align-items: center; justify-content: center;
    padding: calc(16px + var(--safe-top)) 16px calc(16px + var(--safe-bottom));
  }
  .dialog {
    background: var(--surface); border-radius: 28px; max-height: 100%; overflow-y: auto; width: min(100%, 400px);
    animation: pop 0.2s ease-out;
  }
  .dialog.wide { width: min(100%, 520px); }
  @keyframes pop { from { transform: scale(0.94); opacity: 0; } }
</style>
