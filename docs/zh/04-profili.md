# 配置与被禁标志

🌐 [Italiano](../04-profili.md) · [English](../en/04-profili.md) · **中文**

> ⚠️ 本页为机器翻译草稿，正式发布前需母语者校对。

| 配置 | 作用 | 噪声 | Root |
|---|---|---|---|
| `base` | 深度为 3 的爬取。 | 中 | 否 |
| `js` | 与 base 相同，但也会读取 JavaScript 文件。 | 中 | 否 |
| `profondo` | 深度为 4，并带扩展的 JS 分析。 | 高 | 否 |
| `headless` | 使用真实浏览器（系统的 Chrome）。 | 高 | 否 |
| `robots-sitemap` | 从 robots.txt 和 sitemap.xml 出发。 | 中 | 否 |
| `url` | 仅 URL，每行一个。 | 中 | 否 |
| `query` | 仅带参数的 URL。 | 中 | 否 |
| `xhr` | XHR 请求，以 JSON 输出。 | 高 | 否 |
| `prudente` | 带并发数和频率限制。 | 中 | 否 |

`katana-cli profili` 会打印每个配置的具体标志。

## 各配置的作用

**base** (`-d 3 -fs fqdn -silent`). 深度为 3 的爬取。 对 Web 应用的第一轮侦察。

**js** (`-d 3 -jc -fs fqdn -silent`). 与 base 相同，但也会读取 JavaScript 文件。 现代应用会把接口隐藏在 JS 打包文件中。

**profondo** (`-d 4 -jc -jsl -rl 50 -fs fqdn -silent`). 深度为 4，并带扩展的 JS 分析。 用于大型应用。限制为每秒 50 个请求。

**headless** (`-hl -sc -jc -d 3 -fs fqdn -silent`). 使用真实浏览器（系统的 Chrome）。 用于不运行 JavaScript 就什么都不显示的单页应用。在容器中需要 -nos（在 -- 之后传入），但在桌面环境中不要加它。

**robots-sitemap** (`-d 3 -jc -kf robotstxt,sitemapxml -fs fqdn -silent`). 从 robots.txt 和 sitemap.xml 出发。 用于发现网站自行声明的路径。

**url** (`-d 3 -jc -f url -fs fqdn -silent`). 仅 URL，每行一个。 用于给 httpx 或 nuclei 提供输入。

**query** (`-d 3 -jc -f qurl -fs fqdn -silent`). 仅带参数的 URL。 用于找到应用接受输入的位置。

**xhr** (`-d 3 -jc -xhr -fs fqdn -jsonl`). XHR 请求，以 JSON 输出。 用于梳理单页应用的 API 调用。

**prudente** (`-d 3 -jc -c 10 -p 10 -rl 50 -timeout 10 -retry 1 -fs fqdn -silent`). 带并发数和频率限制。 在客户基础设施上默认使用的配置。

## 手动传入标志

`--` 之后写的所有内容都会追加在配置标志之后传给 katana，前提是不在被禁清单中。比对时不区分大小写，`-flag valore` 和 `-flag=valore` 两种写法都能识别，一个或两个短横线均可。

```sh
katana-cli lancia prudente https://app.example.org --scope scope.toml -- -timeout 5
```

## 被禁标志清单

| 标志 | 原因 |
|---|---|
| `-u`, `-list` | 目标来自经过作用域校验的文件 |
| `-o`, `-output` | 输出由 katana-cli 管理 |
| `-fs`, `-field-scope`, `-cs`, `-crawl-scope` | 爬取范围由配置（fqdn）固定 |
| `-ns`, `-no-scope` | 会关闭所有作用域限制 |
| `-resume` | 会恢复一次未经过作用域检查的任务 |
| `-aff`, `-automatic-form-fill` | 自动填写并提交表单：这是会对目标产生影响的操作 |
| `-al`, `-auto-login` | 自动登录：凭据会出现在命令行参数中 |
| `-rf`, `-recorded-flow` | 会重放包含任意操作的浏览器录制 |
| `-up`, `-update` | 程序更新应单独进行，而不是在一次授权任务中进行 |

## 过滤器做不到的事

它不是沙箱。想绕过它并不难，比如直接调用 `katana`。它的作用是拦住失误和坏习惯，而不是拦住一个已经能访问你终端的恶意人员。如果某项与客户约定好的活动需要用到被禁标志，请直接使用 katana，并在项目记录中注明这一选择。
