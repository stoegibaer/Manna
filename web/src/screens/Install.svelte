<script lang="ts">
  import TopBar from '../lib/components/TopBar.svelte'
  import Icon from '../lib/components/Icon.svelte'
  import { install } from '../lib/ui/install.svelte.ts'
  import { router } from '../lib/router.svelte.ts'
</script>

<div class="page">
  <TopBar title="Als App installieren" onback={() => router.back()} />
  <div class="content stack-16" style="padding-bottom:40px">
    {#if install.standalone}
      <div class="ok">Manna ist schon installiert – du nutzt gerade die App.</div>
    {/if}
    <p class="muted" style="margin:0">
      Manna ist eine Web-App: Sie braucht keinen App Store. Auf dem Home-Bildschirm startet sie wie eine normale App,
      funktioniert ohne Internet, und dein Fortschritt bleibt dauerhaft gespeichert.
    </p>

    <h2 class="t-tl">iPhone und iPad</h2>
    <ol class="steps">
      <li>Öffne Manna in <b>Safari</b>.</li>
      <li>Tippe unten auf <span class="ic"><Icon name="share" size={18} /></span> <b>Teilen</b>.</li>
      <li>Wähle <span class="ic"><Icon name="addBox" size={18} /></span> <b>Zum Home-Bildschirm</b> und tippe auf <b>Hinzufügen</b>.</li>
    </ol>

    <h2 class="t-tl">Android und Computer</h2>
    {#if install.prompt}
      <button class="btn" onclick={async () => { await install.prompt?.prompt(); install.prompt = null }}>Jetzt installieren</button>
    {:else}
      <p class="muted" style="margin:0">Im Browser-Menü <b>App installieren</b> oder <b>Zum Startbildschirm hinzufügen</b> wählen.</p>
    {/if}

    <div class="hint t-bm">
      Wichtig: Safari löscht die Daten von Webseiten, die man länger nicht öffnet. Als installierte App passiert das nicht.
      Zur Sicherheit kannst du in den Einstellungen jederzeit eine Sicherung speichern.
    </div>
  </div>
</div>

<style>
  .steps { margin: 0; padding-left: 22px; display: flex; flex-direction: column; gap: 10px; }
  .ic { display: inline-flex; vertical-align: -3px; color: var(--primary); }
</style>
