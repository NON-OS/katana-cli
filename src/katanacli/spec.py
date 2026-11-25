"""Descrizione di katana: profili, flag vietati, formato dei risultati."""

from __future__ import annotations

from urllib.parse import urlsplit

from katanacli.profili import Profilo
from katanacli.risultati import Voce, righe_json, sotto_dict

NOME = "katana"
BINARIO = "katana"
DESCRIZIONE = "Crawling web con scope validato, dry-run di default e audit a catena di hash."
MODO = "url"
PASSA = ("file", "-list")
UNO_EXTRA: tuple[str, ...] = ()  # solo ffuf lavora "un comando per target"
USCITA = "-o"
VERSIONE = ("-version",)
RICONOSCI = "current version"  # testo che il binario vero stampa con {VERSIONE}: distingue da programmi omonimi
INSTALLAZIONE = "Kali/Debian: sudo apt install katana. Ovunque con Go: go install github.com/projectdiscovery/katana/cmd/katana@latest"
SEGRETI = frozenset({"h", "headers", "al", "auto-login"})
GRUPPO = "Host"
NOTA_ATTIVITA = (
    "il crawling invia molte richieste. Ogni profilo usa '-fs fqdn': il crawler resta sull'host esatto "
    "e non segue i link verso altri sottodomini."
)

_SCOPE = ("-fs", "fqdn")

PROFILI = {
    p.nome: p
    for p in (
        Profilo("base", "Crawling a profondità 3.", ("-d", "3", *_SCOPE, "-silent"), "medio",
                "Primo giro su un'applicazione web."),
        Profilo("js", "Come base, ma legge anche i file JavaScript.", ("-d", "3", "-jc", *_SCOPE, "-silent"),
                "medio", "Le applicazioni moderne nascondono gli endpoint nei bundle JS."),
        Profilo("profondo", "Profondità 4 con analisi JS estesa.",
                ("-d", "4", "-jc", "-jsl", "-rl", "50", *_SCOPE, "-silent"), "alto",
                "Per applicazioni grandi. Limitato a 50 richieste al secondo."),
        Profilo("headless", "Usa un browser vero (Chrome di sistema).",
                ("-hl", "-sc", "-jc", "-d", "3", *_SCOPE, "-silent"), "alto",
                "Per le single page app che non mostrano nulla senza JavaScript. In container serve -nos "
                "(passalo dopo --), ma su desktop non metterlo."),
        Profilo("robots-sitemap", "Parte da robots.txt e sitemap.xml.",
                ("-d", "3", "-jc", "-kf", "robotstxt,sitemapxml", *_SCOPE, "-silent"), "medio",
                "Per scoprire percorsi che il sito dichiara da solo."),
        Profilo("url", "Solo gli URL, uno per riga.", ("-d", "3", "-jc", "-f", "url", *_SCOPE, "-silent"),
                "medio", "Per alimentare httpx o nuclei."),
        Profilo("query", "Solo gli URL con parametri.", ("-d", "3", "-jc", "-f", "qurl", *_SCOPE, "-silent"),
                "medio", "Per trovare i punti dove l'applicazione accetta input."),
        Profilo("xhr", "Richieste XHR in JSON.", ("-d", "3", "-jc", "-xhr", *_SCOPE, "-jsonl"), "alto",
                "Per mappare le chiamate API di una single page app.", uscita="jsonl"),
        Profilo("prudente", "Con limiti su concorrenza e frequenza.",
                ("-d", "3", "-jc", "-c", "10", "-p", "10", "-rl", "50", "-timeout", "10", "-retry", "1",
                 *_SCOPE, "-silent"), "medio",
                "Il profilo da usare di default su infrastrutture di clienti."),
    )
}  # fmt: skip

VIETATI = {
    "u": "i target arrivano dal file validato contro lo scope",
    "list": "i target arrivano dal file validato contro lo scope",
    "o": "l'output lo gestisce katana-cli",
    "output": "l'output lo gestisce katana-cli",
    "fs": "il perimetro del crawling è fissato dai profili (fqdn)",
    "field-scope": "il perimetro del crawling è fissato dai profili (fqdn)",
    "cs": "il perimetro del crawling è fissato dai profili (fqdn)",
    "crawl-scope": "il perimetro del crawling è fissato dai profili (fqdn)",
    "ns": "disattiva ogni limite di scope",
    "no-scope": "disattiva ogni limite di scope",
    "resume": "riprende un lancio che non è passato dal controllo dello scope",
    "aff": "compila e invia i form da solo: azioni con effetti sul bersaglio",
    "automatic-form-fill": "compila e invia i form da solo: azioni con effetti sul bersaglio",
    "al": "login automatico: le credenziali finirebbero tra gli argomenti",
    "auto-login": "login automatico: le credenziali finirebbero tra gli argomenti",
    "rf": "riproduce una registrazione del browser con azioni arbitrarie",
    "recorded-flow": "riproduce una registrazione del browser con azioni arbitrarie",
    "up": "l'aggiornamento del programma si fa a parte, non dentro un lancio autorizzato",
    "update": "l'aggiornamento del programma si fa a parte, non dentro un lancio autorizzato",
}

ESEMPI_VIETATI = [
    ["-u", "x"],
    ["-list", "x"],
    ["-fs", "rdn"],
    ["-ns"],
    ["-cs=.*"],
    ["-aff"],
    ["-resume", "x"],
    ["-al", "a:b"],
]
ESEMPI_AMMESSI = [["-d", "2"], ["-nos"], ["-H", "X-A: b"]]


def voci(testo: str) -> list[Voce]:
    out = []
    for r in righe_json(testo):
        if isinstance(r, dict):
            req = sotto_dict(r.get("request"))
            url = str(req.get("endpoint", ""))
            metodo = str(req.get("method", ""))
            if url:
                out.append(Voce(url, f"{metodo} {url}".strip(), urlsplit(url).hostname or ""))
        else:
            url = r.split()[0]
            out.append(Voce(url, url, urlsplit(url).hostname or ""))
    return out


# -- lingua -------------------------------------------------------------------
# Testi tradotti, generati da l10n/. L'italiano resta quello definito sopra.
_TR_TESTI: dict[str, dict[str, str]] = {
    "en": {
        "descrizione": "Web crawling with a validated scope, dry-run by default and a hash-chained audit.",
        "nota_attivita": "crawling sends many requests. Every profile uses '-fs fqdn': the crawler stays on the exact host and does not follow links to other subdomains.",
        "installazione": "Kali/Debian: sudo apt install katana. Anywhere with Go: go install github.com/projectdiscovery/katana/cmd/katana@latest",
        "gruppo": "Host",
    },
    "zh": {
        "descrizione": "Web 爬取，带作用域校验、默认 dry-run 以及哈希链审计。",
        "nota_attivita": "爬取会发送大量请求。每个配置都使用 '-fs fqdn'：爬虫只停留在精确的主机上，不会跟随指向其他子域名的链接。",
        "installazione": "Kali/Debian：sudo apt install katana。任何装了 Go 的环境：go install github.com/projectdiscovery/katana/cmd/katana@latest",
        "gruppo": "主机",
    },
}
_TR_PROFILI: dict[str, dict[str, list[str]]] = {
    "en": {
        "base": ["Crawling at depth 3.", "First pass on a web application."],
        "js": ["Like base, but it also reads JavaScript files.", "Modern applications hide endpoints in JS bundles."],
        "profondo": ["Depth 4 with extended JS analysis.", "For large applications. Capped at 50 requests per second."],
        "headless": [
            "Uses a real browser (the system's Chrome).",
            "For single-page apps that show nothing without JavaScript. In a container you need -nos (pass it after --), but on desktop don't set it.",
        ],
        "robots-sitemap": ["Starts from robots.txt and sitemap.xml.", "To discover paths the site declares itself."],
        "url": ["URLs only, one per line.", "To feed httpx or nuclei."],
        "query": ["Only URLs with parameters.", "To find the points where the application takes input."],
        "xhr": ["XHR requests in JSON.", "To map a single-page app's API calls."],
        "prudente": ["With concurrency and rate limits.", "The default profile on client infrastructure."],
    },
    "zh": {
        "base": ["深度为 3 的爬取。", "对 Web 应用的第一轮侦察。"],
        "js": ["与 base 相同，但也会读取 JavaScript 文件。", "现代应用会把接口隐藏在 JS 打包文件中。"],
        "profondo": ["深度为 4，并带扩展的 JS 分析。", "用于大型应用。限制为每秒 50 个请求。"],
        "headless": [
            "使用真实浏览器（系统的 Chrome）。",
            "用于不运行 JavaScript 就什么都不显示的单页应用。在容器中需要 -nos（在 -- 之后传入），但在桌面环境中不要加它。",
        ],
        "robots-sitemap": ["从 robots.txt 和 sitemap.xml 出发。", "用于发现网站自行声明的路径。"],
        "url": ["仅 URL，每行一个。", "用于给 httpx 或 nuclei 提供输入。"],
        "query": ["仅带参数的 URL。", "用于找到应用接受输入的位置。"],
        "xhr": ["XHR 请求，以 JSON 输出。", "用于梳理单页应用的 API 调用。"],
        "prudente": ["带并发数和频率限制。", "在客户基础设施上默认使用的配置。"],
    },
}
_TR_VIETATI: dict[str, dict[str, str]] = {
    "en": {
        "compila e invia i form da solo: azioni con effetti sul bersaglio": "fills in and submits forms on its own: actions with effects on the target",
        "disattiva ogni limite di scope": "disables every scope limit",
        "i target arrivano dal file validato contro lo scope": "targets come from the file validated against the scope",
        "il perimetro del crawling è fissato dai profili (fqdn)": "the crawling perimeter is fixed by the profiles (fqdn)",
        "l'aggiornamento del programma si fa a parte, non dentro un lancio autorizzato": "updating the program is done separately, not inside an authorized run",
        "l'output lo gestisce katana-cli": "output is handled by katana-cli",
        "login automatico: le credenziali finirebbero tra gli argomenti": "automatic login: the credentials would end up among the arguments",
        "riprende un lancio che non è passato dal controllo dello scope": "resumes a run that didn't go through the scope check",
        "riproduce una registrazione del browser con azioni arbitrarie": "replays a browser recording with arbitrary actions",
    },
    "zh": {
        "compila e invia i form da solo: azioni con effetti sul bersaglio": "自动填写并提交表单：这是会对目标产生影响的操作",
        "disattiva ogni limite di scope": "会关闭所有作用域限制",
        "i target arrivano dal file validato contro lo scope": "目标来自经过作用域校验的文件",
        "il perimetro del crawling è fissato dai profili (fqdn)": "爬取范围由配置（fqdn）固定",
        "l'aggiornamento del programma si fa a parte, non dentro un lancio autorizzato": "程序更新应单独进行，而不是在一次授权任务中进行",
        "l'output lo gestisce katana-cli": "输出由 katana-cli 管理",
        "login automatico: le credenziali finirebbero tra gli argomenti": "自动登录：凭据会出现在命令行参数中",
        "riprende un lancio che non è passato dal controllo dello scope": "会恢复一次未经过作用域检查的任务",
        "riproduce una registrazione del browser con azioni arbitrarie": "会重放包含任意操作的浏览器录制",
    },
}
_ORIGINALI = (DESCRIZIONE, NOTA_ATTIVITA, INSTALLAZIONE, GRUPPO, PROFILI, VIETATI)


def applica_lingua(lingua: str) -> None:
    """Passa testi, profili e motivi dei flag vietati alla lingua scelta. Ripartendo
    sempre dagli originali italiani, chiamarla più volte non accumula niente."""
    global DESCRIZIONE, NOTA_ATTIVITA, INSTALLAZIONE, GRUPPO, PROFILI, VIETATI
    from dataclasses import replace

    DESCRIZIONE, NOTA_ATTIVITA, INSTALLAZIONE, GRUPPO, PROFILI, VIETATI = _ORIGINALI
    testi = _TR_TESTI.get(lingua)
    if not testi:
        return
    DESCRIZIONE = testi["descrizione"] or DESCRIZIONE
    NOTA_ATTIVITA = testi["nota_attivita"] or NOTA_ATTIVITA
    INSTALLAZIONE = testi["installazione"] or INSTALLAZIONE
    GRUPPO = testi["gruppo"] or GRUPPO
    prof = _TR_PROFILI.get(lingua, {})
    PROFILI = {
        n: replace(p, descrizione=prof[n][0] or p.descrizione, quando=prof[n][1] or p.quando) if n in prof else p
        for n, p in PROFILI.items()
    }
    viet = _TR_VIETATI.get(lingua, {})
    VIETATI = {k: viet.get(v, v) for k, v in VIETATI.items()}
