# Profiles and forbidden flags

🌐 [Italiano](../04-profili.md) · **English** · [中文](../zh/04-profili.md)

| Profile | What it does | Noise | Root |
|---|---|---|---|
| `base` | Crawling at depth 3. | medium | no |
| `js` | Like base, but it also reads JavaScript files. | medium | no |
| `profondo` | Depth 4 with extended JS analysis. | high | no |
| `headless` | Uses a real browser (the system's Chrome). | high | no |
| `robots-sitemap` | Starts from robots.txt and sitemap.xml. | medium | no |
| `url` | URLs only, one per line. | medium | no |
| `query` | Only URLs with parameters. | medium | no |
| `xhr` | XHR requests in JSON. | high | no |
| `prudente` | With concurrency and rate limits. | medium | no |

`katana-cli profili` prints the exact flags of each one.

## What each profile does

**base** (`-d 3 -fs fqdn -silent`). Crawling at depth 3. First pass on a web application.

**js** (`-d 3 -jc -fs fqdn -silent`). Like base, but it also reads JavaScript files. Modern applications hide endpoints in JS bundles.

**profondo** (`-d 4 -jc -jsl -rl 50 -fs fqdn -silent`). Depth 4 with extended JS analysis. For large applications. Capped at 50 requests per second.

**headless** (`-hl -sc -jc -d 3 -fs fqdn -silent`). Uses a real browser (the system's Chrome). For single-page apps that show nothing without JavaScript. In a container you need -nos (pass it after --), but on desktop don't set it.

**robots-sitemap** (`-d 3 -jc -kf robotstxt,sitemapxml -fs fqdn -silent`). Starts from robots.txt and sitemap.xml. To discover paths the site declares itself.

**url** (`-d 3 -jc -f url -fs fqdn -silent`). URLs only, one per line. To feed httpx or nuclei.

**query** (`-d 3 -jc -f qurl -fs fqdn -silent`). Only URLs with parameters. To find the points where the application takes input.

**xhr** (`-d 3 -jc -xhr -fs fqdn -jsonl`). XHR requests in JSON. To map a single-page app's API calls.

**prudente** (`-d 3 -jc -c 10 -p 10 -rl 50 -timeout 10 -retry 1 -fs fqdn -silent`). With concurrency and rate limits. The default profile on client infrastructure.

## Passing flags by hand

Everything you write after `--` goes to katana, after the profile flags, provided it is not on the forbidden list. The check is case-insensitive and accepts both `-flag valore` and `-flag=valore`, with one or two dashes.

```sh
katana-cli lancia prudente https://app.example.org --scope scope.toml -- -timeout 5
```

## Forbidden list

| Flag | Why |
|---|---|
| `-u`, `-list` | targets come from the file validated against the scope |
| `-o`, `-output` | output is handled by katana-cli |
| `-fs`, `-field-scope`, `-cs`, `-crawl-scope` | the crawling perimeter is fixed by the profiles (fqdn) |
| `-ns`, `-no-scope` | disables every scope limit |
| `-resume` | resumes a run that didn't go through the scope check |
| `-aff`, `-automatic-form-fill` | fills in and submits forms on its own: actions with effects on the target |
| `-al`, `-auto-login` | automatic login: the credentials would end up among the arguments |
| `-rf`, `-recorded-flow` | replays a browser recording with arbitrary actions |
| `-up`, `-update` | updating the program is done separately, not inside an authorized run |

## What the filter does not do

It is not a sandbox. If you want to get around it you can, for example by calling `katana` directly. It is there to stop mistakes and bad habits, not an attacker who already has access to your terminal. If you need a forbidden flag for an activity agreed with the client, use katana directly and record the decision in the engagement.
