#!/usr/bin/env bash
# katana_workflow_v2.sh
# Riferimento operativo completo. Solo target autorizzati.
# Le note spiegano il perché e il quando, non solo il cosa.

TARGET="<HOST_O_URL>"
TARGETS_FILE="<FILE_CON_LISTA_TARGET>"
OUT="<PREFISSO_OUTPUT>"

# ---------------------------------------------------------------
# Prerequisiti per headless (-hl)
# Katana bundled include Chromium, ma in alcuni ambienti
# (VPS minimal, container senza browser) non parte.
# Se hai Chrome installato sul sistema, usa -sc per evitare
# di scaricare il bundle. Se sei in container, -nos è
# obbligatorio: Chrome non parte come root senza --no-sandbox.
# Su desktop, NON mettere -nos: disabilita una protezione
# di sicurezza senza motivo.
# ---------------------------------------------------------------

# Desktop con Chrome di sistema (consigliato se hai Chrome).
# -sc evita il download del bundle bundled Chromium.
# katana -u "$TARGET" -hl -sc -jc -d 3 -silent -o "$OUT.headless.txt"

# Container / VPS minimal: -nos obbligatorio.
# katana -u "$TARGET" -hl -nos -jc -d 3 -silent -o "$OUT.headless.txt"

# ---------------------------------------------------------------
# Crawl base (standard mode)
# HTTP client Go. Legge HTML, segue href. NON esegue JS.
# ---------------------------------------------------------------
katana -u "$TARGET" -d 3 -silent -o "$OUT.base.txt"

# ---------------------------------------------------------------
# JS-aware crawl (-jc)
# Parsa i file JavaScript e estrae stringhe che sembrano URL.
# È l'unico modo per trovare endpoint definiti nei bundle
# (React, Vue, Angular) che non compaiono mai nell'HTML statico.
# ---------------------------------------------------------------
katana -u "$TARGET" -d 3 -jc -silent -o "$OUT.jc.txt"

# -jsl (jsluice) è il parser più profondo. Più memoria, più
# finding, ma non sempre necessario. Usalo quando -jc non basta
# e il target è una SPA pesante.
katana -u "$TARGET" -d 4 -jc -jsl -rl 50 -silent -o "$OUT.jsl.txt"

# ---------------------------------------------------------------
# Headless crawl (-hl)
# Avvia Chromium, esegue JS, renderizza il DOM. Trova endpoint
# che esistono solo dopo l'esecuzione (path costruiti a runtime,
# lazy loading, client-side routing).
#
# ATTENZIONE: headless NON sostituisce -jc. Test controllati
# mostrano che -headless da solo perde gli endpoint nei file JS,
# mentre -jc da solo perde quelli runtime. Per copertura completa
# servono DUE crawl e un merge.
# ---------------------------------------------------------------

# Headless con Chrome di sistema (desktop).
# -sc usa Chrome installato, evita il bundle.
katana -u "$TARGET" -hl -sc -jc -d 3 -silent -o "$OUT.headless.txt"

# Headless in container: -nos obbligatorio.
# katana -u "$TARGET" -hl -nos -jc -d 3 -silent -o "$OUT.headless.txt"

# Merge dei due risultati per copertura completa.
sort -u "$OUT.jc.txt" "$OUT.headless.txt" > "$OUT.endpoints.txt"

# ---------------------------------------------------------------
# Deduplica URL simili (-fsu)
# Su un'app con ID numerici, Katana produce /users/1, /users/2,
# /users/3... centinaia di URL che sono lo stesso endpoint.
# -fsu collassa gli URL strutturalmente identici e tiene solo
# un rappresentante.
#
# Meccanismo: regex euristica per ID numerici, UUID, hash, date;
# poi un trie adattivo per host che impara le posizioni dei
# parametri a runtime. Senza -fsu, l'output è inutilizzabile
# su qualsiasi target con parametri numerici.
# ---------------------------------------------------------------
katana -u "$TARGET" -d 3 -jc -fsu -silent -o "$OUT.fsu.txt"

# ---------------------------------------------------------------
# Known files: robots.txt e sitemap.xml
# Contengono path che non sono linkati nell'HTML.
# ATTENZIONE: -kf richiede -d >= 3. Sotto depth 3, i known
# files vengono ignorati silenziosamente.
#
# Nota operativa: su target IP-literal, il parser sitemap di
# Katana può non recuperare i <loc> per un problema di scope
# validation. Se -kf non produce risultati attesi, estrai i
# <loc> manualmente e passali come seed con -list.
# ---------------------------------------------------------------
katana -u "$TARGET" -d 3 -jc -kf robotstxt -silent -o "$OUT.robots.txt"
katana -u "$TARGET" -d 3 -jc -kf sitemapxml -silent -o "$OUT.sitemap.txt"

# ---------------------------------------------------------------
# Scope control
# Default -fs rdn: root domain + TUTTI i subdomini.
# Su target che carica risorse da CDN esterne, questo è troppo.
# ---------------------------------------------------------------

# Scope ristretto al dominio esatto (no subdomini).
katana -u "$TARGET" -fs fqdn -d 3 -jc -silent -o "$OUT.fqdn.txt"

# Scope custom con regex.
katana -u "$TARGET" -cs '.*target\.com/.*' -d 3 -jc -silent -o "$OUT.cs.txt"

# ---------------------------------------------------------------
# Rate limiting e performance
# -c: fetcher concorrenti per target (default 10)
# -p: target in parallelo (default 10)
# -rl: richieste al secondo (default 150)
#
# Ordine di tuning: abbassa -c prima, poi -p, poi -rl.
# Su produzione reale, -c 10 -rl 50 è conservativo.
# ---------------------------------------------------------------
katana -u "$TARGET" -d 3 -jc -c 10 -p 10 -rl 50 -timeout 10 -retry 1 -silent -o "$OUT.safe.txt"

# ---------------------------------------------------------------
# Output strutturato per pipeline
# JSONL è il formato per httpx e Nuclei. Ogni riga è un oggetto
# con .url, .method, .body, ecc.
# ---------------------------------------------------------------
katana -u "$TARGET" -d 3 -jc -jsonl -o "$OUT.jsonl"

# Solo URL, per passare a httpx.
katana -u "$TARGET" -d 3 -jc -f url -silent -o "$OUT.urls.txt"

# Solo URL con query parameter (utili per DAST/Nuclei).
katana -u "$TARGET" -d 3 -jc -f qurl -silent -o "$OUT.qurls.txt"

# XHR extraction: endpoint chiamati via XHR/fetch.
katana -u "$TARGET" -d 3 -jc -xhr -jsonl -o "$OUT.xhr.jsonl"

# ---------------------------------------------------------------
# Pipeline completa: Katana → httpx → Nuclei (eseguibile)
# Katana trova endpoint, httpx verifica quali rispondono,
# Nuclei testa vulnerabilità solo sui vivi.
# ---------------------------------------------------------------

# Step 1: crawl.
katana -u "$TARGET" -d 3 -jc -f url -silent -o /tmp/katana_urls.txt

# Step 2: verifica con httpx (opzionale, ma riduce il rumore).
if command -v httpx &>/dev/null; then
    cat /tmp/katana_urls.txt | httpx -silent -mc 200,401,403 -o /tmp/live_urls.txt
else
    echo "httpx non installato. Uso katana_urls.txt come input per Nuclei."
    cp /tmp/katana_urls.txt /tmp/live_urls.txt
fi

# Step 3: Nuclei sui soli URL vivi.
if command -v nuclei &>/dev/null; then
    nuclei -l /tmp/live_urls.txt -severity critical,high -exclude-tags intrusive,dos -jsonl -o /tmp/nuclei_findings.jsonl
else
    echo "nuclei non installato. Pipeline fermata a live_urls.txt."
fi

# ---------------------------------------------------------------
# Comando di produzione completo
# Depth 3, JS parsing, deduplica, known files, rate limitato, JSONL.
# ---------------------------------------------------------------
katana -u "$TARGET" \
  -d 3 \
  -jc \
  -fsu \
  -kf robotstxt,sitemapxml \
  -fs fqdn \
  -c 10 -p 10 -rl 50 -timeout 10 -retry 1 \
  -silent -jsonl -o "$OUT.jsonl"
