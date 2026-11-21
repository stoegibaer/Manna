<script lang="ts">
  import type { Snippet } from 'svelte'

  /** Bottom sheet (like Material's ModalBottomSheet). */
  let { onclose, children }: { onclose: () => void; children: Snippet } = $props()

  function key(e: KeyboardEvent) { if (e.key === 'Escape') onclose() }
</script>

<svelte:window onkeydown={key} />

<div class="scrim" onclick={onclose} role="presentation"></div>
<div class="sheet" role="dialog" aria-modal="true">
  <div class="handle"></div>
  <div class="body">{@render children()}</div>
</div>

<style>
  .scrim { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.32); z-index: 40; animation: fade 0.2s; }
  .sheet {
    position: fixed; left: 0; right: 0; bottom: 0; z-index: 41; margin: 0 auto; max-width: var(--page-max);
    max-height: 88dvh; display: flex; flex-direction: column;
    background: var(--surface); border-radius: 28px 28px 0 0; animation: up 0.25s ease-out;
  }
  .handle { width: 32px; height: 4px; border-radius: 2px; background: var(--outline); margin: 16px auto 12px; flex: none; }
  .body { overflow-y: auto; padding: 0 24px calc(32px + var(--safe-bottom)); -webkit-overflow-scrolling: touch; }
  @keyframes up { from { transform: translateY(40%); opacity: 0.4; } to { transform: none; opacity: 1; } }
  @keyframes fade { from { opacity: 0; } }
</style>
