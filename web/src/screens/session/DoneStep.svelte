<script lang="ts">
  import Icon from '../../lib/components/Icon.svelte'
  import { REFLECTION_TAGS, type Session } from './session.svelte.ts'

  let { s, onclose, onchooseplan }: { s: Session; onclose: () => void; onchooseplan: () => void } = $props()
  const section = $derived(s.section)
  // svelte-ignore state_referenced_locally
  let writing = $state(s.reflectionNote.trim() !== '')
  const keepGoing = $derived(s.more && !!s.next && s.next.stage === section?.stage)
</script>

<div class="content enter done">
  <div class="badge"><Icon name="check" size={46} color="var(--primary)" /></div>

  {#if s.planFinished}
    <h2 class="t-hm center">{s.plan?.title} abgeschlossen</h2>
    <p class="muted center" style="margin:0">{s.nothingLeft ? 'Du hast alle Abschnitte dieses Plans gelesen.' : 'Du hast den ganzen Plan gelesen. Stark.'}</p>
  {:else}
    <h2 class="t-hm center">Für heute geschafft</h2>
    {#if section}<p class="muted" style="margin:0">„{section.title}“ gelesen.</p>{/if}
  {/if}

  {#if section && !s.nothingLeft}
    <!-- „Was nimmst du mit?“ – one tap is enough, a own thought is optional -->
    <div class="card stack-8" style="width:100%">
      <p class="t-ll secondary">Was nimmst du mit?</p>
      <div class="chips">
        {#each REFLECTION_TAGS as [id, label] (id)}
          <button class="chip" class:on={s.reflectionTags.has(id)} onclick={() => s.toggleTag(id)}>
            {#if s.reflectionTags.has(id)}<Icon name="check" size={18} />{/if}{label}
          </button>
        {/each}
        <button class="chip" class:on={writing} onclick={() => (writing = !writing)}>eigener Gedanke …</button>
      </div>
      {#if writing}
        <textarea rows="2" placeholder="Ein Satz reicht." bind:value={s.reflectionNote} onblur={() => s.saveReflection()}></textarea>
      {/if}
      <p class="t-bs muted">Wird in deinem Tagebuch gesammelt – nur für dich.</p>
    </div>
  {/if}

  {#if section?.try}
    <div class="card stack-6" style="width:100%">
      <p class="t-ll secondary">Heute ausprobieren</p>
      <p class="t-bl">{section.try}</p>
    </div>
  {/if}
  {#if section?.prayer && s.prayerText}
    <div class="card stack-8" style="width:100%">
      <p class="t-ll secondary">Als Gebet</p>
      <p class="t-bl serif italic">{s.prayerText}</p>
      <p class="t-bs muted">— {section.prayer.source}</p>
    </div>
  {/if}

  <div style="height:4px"></div>
  {#if s.planFinished}
    <button class="btn" onclick={onchooseplan}>Wohin als Nächstes?</button>
    <button class="btn text" onclick={onclose}>Fertig für heute</button>
  {:else if keepGoing}
    <!-- „Viel Energie“: keep going within the stage – but stopping is always fine -->
    <button class="btn" onclick={() => s.another()}>Nächster Abschnitt</button>
    <button class="btn text" onclick={onclose}>Für heute genug</button>
  {:else}
    <button class="btn" onclick={onclose}>Fertig</button>
  {/if}

  {#if !s.planFinished && s.next && !keepGoing}
    <hr class="divider" />
    {#if section?.teaser}<p class="t-bl serif italic muted center">{section.teaser}</p>{/if}
    <button class="btn text" onclick={() => s.another()}>Noch ein Abschnitt</button>
  {/if}
</div>

<style>
  .done { align-items: center; gap: 16px; padding-top: 20px; padding-bottom: 32px; }
  .badge { width: 84px; height: 84px; border-radius: 50%; background: var(--primary-container); display: flex; align-items: center; justify-content: center; }
  .stack-6 { display: flex; flex-direction: column; gap: 6px; }
</style>
