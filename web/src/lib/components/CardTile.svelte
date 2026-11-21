<script lang="ts" module>
  const STYLES: Record<string, [string, string, string]> = {
    person: ['PERSON', '#7A4E2D', '#C08A55'],
    ort: ['ORT', '#2D5E6E', '#6FA3A8'],
    ereignis: ['EREIGNIS', '#6B2F4F', '#B0698A'],
  }
  export const cardStyle = (type: string) => STYLES[type] ?? ['BEGRIFF', '#2F6B4F', '#7FB08A']
</script>

<script lang="ts">
  import type { Card } from '../data/plan.ts'
  import { hashCode } from '../util/random.ts'

  /** A collectible card: colored band by type, an ornamental pattern, name and short text. */
  let { card }: { card: Card } = $props()
  const st = $derived(cardStyle(card.type))
  const seed = $derived(hashCode(card.id))
  const cx = $derived(62 + ((seed & 0xff) / 255) * 30)
  const cy = $derived(20 + (((seed >> 8) & 0xff) / 255) * 60)
</script>

<div class="card-tile" style="border-color:{st[1]}59">
  <div class="band" style="background:linear-gradient(135deg, {st[1]}, {st[2]})">
    <svg class="orn" preserveAspectRatio="none" aria-hidden="true">
      {#each [1, 2, 3, 4, 5, 6] as i (i)}
        <circle cx="{cx}%" cy="{cy}%" r={i * 16} fill="none" stroke="rgba(255,255,255,0.10)" stroke-width="1.2" />
      {/each}
    </svg>
    <span class="label">{st[0]}</span>
    <span class="name">{card.name}</span>
  </div>
  <div class="text stack-6">
    <p class="t-bm">{card.text}</p>
    {#if card.refs}<p class="t-ls muted">{card.refs}</p>{/if}
  </div>
</div>

<style>
  .card-tile { width: 100%; border-radius: 18px; overflow: hidden; background: var(--surface); border: 1px solid; }
  .band { position: relative; height: 64px; overflow: hidden; }
  .orn { position: absolute; inset: 0; width: 100%; height: 100%; }
  .label { position: absolute; left: 16px; top: 10px; color: rgba(255, 255, 255, 0.85); font-size: 11px; font-weight: 700; letter-spacing: 1.6px; }
  .name { position: absolute; left: 16px; top: 28px; color: #fff; font-family: var(--bible-font); font-weight: 600; font-size: 22px; line-height: 28px; white-space: nowrap; }
  .text { padding: 16px; }
  .stack-6 { display: flex; flex-direction: column; gap: 6px; }
</style>
