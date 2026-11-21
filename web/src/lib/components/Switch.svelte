<script lang="ts">
  let { checked, disabled = false, onchange, label }: { checked: boolean; disabled?: boolean; onchange: (v: boolean) => void; label: string } = $props()
</script>

<button class="switch" class:on={checked} role="switch" aria-checked={checked} aria-label={label} {disabled} onclick={() => onchange(!checked)}>
  <span class="thumb"></span>
</button>

<style>
  .switch {
    flex: none; width: 52px; height: 32px; border-radius: 16px; border: 2px solid var(--outline); background: var(--surface-variant);
    position: relative; cursor: pointer; padding: 0; transition: background 0.2s, border-color 0.2s;
  }
  .switch.on { background: var(--primary); border-color: var(--primary); }
  .switch:disabled { opacity: 0.38; cursor: default; }
  .thumb {
    position: absolute; top: 50%; left: 6px; width: 16px; height: 16px; border-radius: 50%; background: var(--outline);
    transform: translateY(-50%); transition: all 0.2s;
  }
  .on .thumb { left: 22px; width: 24px; height: 24px; background: var(--on-primary); }
</style>
