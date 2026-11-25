# Profili e flag vietati

🌐 **Italiano** · [English](en/04-profili.md) · [中文](zh/04-profili.md)

| Profilo | Cosa fa | Rumore | Root |
|---|---|---|---|
| `base` | Crawling a profondità 3. | medio | no |
| `js` | Come base, ma legge anche i file JavaScript. | medio | no |
| `profondo` | Profondità 4 con analisi JS estesa. | alto | no |
| `headless` | Usa un browser vero (Chrome di sistema). | alto | no |
| `robots-sitemap` | Parte da robots.txt e sitemap.xml. | medio | no |
| `url` | Solo gli URL, uno per riga. | medio | no |
| `query` | Solo gli URL con parametri. | medio | no |
| `xhr` | Richieste XHR in JSON. | alto | no |
| `prudente` | Con limiti su concorrenza e frequenza. | medio | no |

`katana-cli profili` stampa i flag esatti di ciascuno.

## Cosa fa ciascun profilo

**base** (`-d 3 -fs fqdn -silent`). Crawling a profondità 3. Primo giro su un'applicazione web.

**js** (`-d 3 -jc -fs fqdn -silent`). Come base, ma legge anche i file JavaScript. Le applicazioni moderne nascondono gli endpoint nei bundle JS.

**profondo** (`-d 4 -jc -jsl -rl 50 -fs fqdn -silent`). Profondità 4 con analisi JS estesa. Per applicazioni grandi. Limitato a 50 richieste al secondo.

**headless** (`-hl -sc -jc -d 3 -fs fqdn -silent`). Usa un browser vero (Chrome di sistema). Per le single page app che non mostrano nulla senza JavaScript. In container serve -nos (passalo dopo --), ma su desktop non metterlo.

**robots-sitemap** (`-d 3 -jc -kf robotstxt,sitemapxml -fs fqdn -silent`). Parte da robots.txt e sitemap.xml. Per scoprire percorsi che il sito dichiara da solo.

**url** (`-d 3 -jc -f url -fs fqdn -silent`). Solo gli URL, uno per riga. Per alimentare httpx o nuclei.

**query** (`-d 3 -jc -f qurl -fs fqdn -silent`). Solo gli URL con parametri. Per trovare i punti dove l'applicazione accetta input.

**xhr** (`-d 3 -jc -xhr -fs fqdn -jsonl`). Richieste XHR in JSON. Per mappare le chiamate API di una single page app.

**prudente** (`-d 3 -jc -c 10 -p 10 -rl 50 -timeout 10 -retry 1 -fs fqdn -silent`). Con limiti su concorrenza e frequenza. Il profilo da usare di default su infrastrutture di clienti.

## Passare flag a mano

Tutto ciò che scrivi dopo `--` finisce a katana, dopo i flag del profilo, a patto che non sia nell'elenco dei vietati. Il confronto non distingue maiuscole e minuscole e accetta sia `-flag valore` sia `-flag=valore`, con uno o due trattini.

```sh
katana-cli lancia prudente https://app.example.org --scope scope.toml -- -timeout 5
```

## Elenco dei vietati

| Flag | Perché |
|---|---|
| `-u`, `-list` | i target arrivano dal file validato contro lo scope |
| `-o`, `-output` | l'output lo gestisce katana-cli |
| `-fs`, `-field-scope`, `-cs`, `-crawl-scope` | il perimetro del crawling è fissato dai profili (fqdn) |
| `-ns`, `-no-scope` | disattiva ogni limite di scope |
| `-resume` | riprende un lancio che non è passato dal controllo dello scope |
| `-aff`, `-automatic-form-fill` | compila e invia i form da solo: azioni con effetti sul bersaglio |
| `-al`, `-auto-login` | login automatico: le credenziali finirebbero tra gli argomenti |
| `-rf`, `-recorded-flow` | riproduce una registrazione del browser con azioni arbitrarie |
| `-up`, `-update` | l'aggiornamento del programma si fa a parte, non dentro un lancio autorizzato |

## Quello che il filtro non fa

Non è una sandbox. Se vuoi aggirarlo ci riesci, per esempio chiamando `katana` direttamente. Serve a fermare gli errori e le abitudini sbagliate, non un malintenzionato che ha già accesso al tuo terminale. Se ti serve un flag vietato per un'attività concordata con il cliente, usa katana direttamente e annota la scelta nell'ingaggio.
