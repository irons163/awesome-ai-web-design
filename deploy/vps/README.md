# VPS 部署

部署包的 `www/` 是可以直接託管的靜態網站，包含主站、74 份預覽、分析、指令及已保存的圖片、影片、字型。原先由 Cloudflare Worker 轉送的 GitHub 素材已還原為本機檔案，並依既有 SHA-256 清單核對。

VPS 不需要 Node.js、pnpm、Wrangler 或資料庫。目錄、搜尋、收藏與複製在瀏覽器執行；收藏存在各使用者的瀏覽器，切換網域後不會自動轉移。完整品牌服務、即時資料與影片／動畫的既有未驗收範圍保持相同。

## 目前部署（2026-10-21）

公開入口為 [webdesign.zero2codex.dev](https://webdesign.zero2codex.dev/)，DNS 的 `webdesign` A 紀錄指向 `178.105.116.16`，使用 DNS only。既有 `zero2codex.dev` 首頁保留。

目前版本位於 `/var/www/awesome-ai-web-design/releases/2026-10-21-downloads`；`current` 以相對連結指向 `releases/2026-10-21-downloads`。網站共 6,356 個公開檔案、1,244,555,774 bytes。原始碼以 commit `1a783491c9539c3153c2fc96c16d59131e024f4e` 為基底，本次變更另以版本清單及內容摘要核對；該 commit 不代表已包含所有更新。版本目錄的 `MANIFEST.json` 與 `RELEASE-VERIFICATION.json` 保存在 webroot 之外。

執行設定位於 `/var/www/awesome-ai-web-design/ops/`，服務容器為 `awesome-ai-web-design`。既有入口容器 `hetzner-caddy-1` 透過 `xai-proxy` 網路轉送流量，並自動申請及更新 Let's Encrypt 憑證；檢查用的 `18080` 只綁定本機。

入口 Caddy 設定為 `/opt/xai-dating/deploy/hetzner/Caddyfile`。本次變更前的備份為 `/var/www/awesome-ai-web-design/ops/Caddyfile.edge.before`，啟用紀錄為 `EDGE-ACTIVATION.json`。入口設定以單一檔案掛載到容器，後續修改須保留原檔 inode，寫入後驗證並執行 `caddy reload`；不可用重新命名取代檔案，以免掛載仍讀取舊內容。回復時也應以最新設定為基礎處理，避免覆蓋其他網站之後的更新。

部署狀態與公開網址驗證紀錄保存在同一 `ops/` 目錄；更新內容前先建立及驗證新的版本目錄，再切換 `current`，保留上一版供回復。

繁體中文內容含 74 組主要規格與指令、59 份比對紀錄、388 條差異說明、74 份延伸規格、222 則任務指令及 74 份中文生成參考。2026-10-20 主要規格再補齊完整實作數值、CSS、元件行為與無圖做法；整包共 448 個檔案，另有 74 個單品牌包，每包 10 個檔案，與主要分頁內容相同。原始預覽與素材位元組保留。`ops/FINAL-ACCEPTANCE-DEPLOYMENT.json`、`FINAL-ACCEPTANCE-BACKEND-VERIFICATION.json` 與 `FINAL-ACCEPTANCE-PUBLIC-VERIFICATION.json` 記錄目前版本及驗證；先前各版本保留供回復。

## 準備部署包

在原始碼電腦執行，VPS 只需接收產出的壓縮檔：

```sh
node scripts/build_site.mjs --output public
python3 scripts/package_vps.py --output .test-artifacts/vps-ready
```

使用新或空的輸出目錄。內容或來源素材雜湊不符時會停止；不會改寫原始素材、既有發布檔或正式網站。

包內包含 `www/`、Nginx 與 Caddy 設定、這份說明與 `MANIFEST.json`。清單記錄每個公開檔案的大小與 SHA-256。Git 歷史、開發依賴、研究截圖、私人匯出及 Sites 的部署身分不包含在內。素材來源網址仍保留作為溯源資料；網站中的外部連結與第三方服務仍使用原來的目的地。

## 上傳與切換版本

下方 `your-user@your-vps` 是待替換的 SSH 連線位置。先上傳及驗證，再設定網域。保留既有版本可供回復。

```sh
scp .test-artifacts/vps-ready.tar.gz your-user@your-vps:/tmp/awesome-ai-web-design.tar.gz
ssh your-user@your-vps
```

在 VPS 選擇一個尚不存在的版本目錄：

```sh
site_release=/var/www/awesome-ai-web-design/releases/2026-10-15-v115
sudo mkdir -p "$(dirname "$site_release")"
sudo mkdir "$site_release"
sudo tar -xzf /tmp/awesome-ai-web-design.tar.gz -C "$site_release" --no-same-owner
```

先比對上傳檔案的 `sha256sum` 與本機產出的摘要。需要逐檔核對時，可使用包內 `MANIFEST.json`，並檢查檔案位元組數及 SHA-256。

網站檔案可供 Nginx 使用者讀取後，將 `current` 符號連結指向該版本。已有網站時先保留原來的連結目標，僅切換這個網站：

```sh
sudo ln -s "releases/$(basename "$site_release")" /var/www/awesome-ai-web-design/current.next
sudo mv -Tf /var/www/awesome-ai-web-design/current.next /var/www/awesome-ai-web-design/current
```

## Nginx 與網域

套用包內 `nginx.conf` 的 server block，將 `your-domain.example` 換成實際網域，並確認 `root` 路徑。此範本先提供 HTTP；既有 HTTPS 反向代理可直接使用這個 webroot，或在網域解析完成後設定 TLS 憑證。

不要覆寫 VPS 上其他網站的設定。先執行 `sudo nginx -t`，成功後再重載 Nginx。實際放置設定及重載指令依 VPS 的作業系統與既有安裝方式而定。

範本支援 `/official-progress` 與 `.html` 路徑；HTML、指令與程式碼會重新驗證快取，圖片等素材保留七天快取。Markdown 以 UTF-8 純文字提供，下載仍由主站按鈕指定檔名。Nginx 靜態檔案服務也能處理影片的 Range 請求。

Nginx 文件：[root、try_files 與靜態檔案設定](https://nginx.org/en/docs/http/ngx_http_core_module.html)。

## 已有 Docker 與 Caddy 的 VPS

可使用獨立靜態服務，讓既有 Caddy 繼續管理網域與 HTTPS。將 `Caddyfile` 和 `compose.caddy.yaml` 放在 `/var/www/awesome-ai-web-design/ops/`；`current` 需以相對路徑指向驗證完成的版本，讓主機與容器都能解析連結。舊部署包若只有 Nginx 範本，另從原始碼複製這兩份設定即可，不需重新上傳網站素材。

確認 Docker 的代理網路名稱，並以 `PROXY_NETWORK` 設定；範本預設為此 VPS 既有的 `xai-proxy`。先檢查 `18080` 未被占用，再執行：

```sh
cd /var/www/awesome-ai-web-design/ops
docker compose -f compose.caddy.yaml config --quiet
docker compose -f compose.caddy.yaml run --rm --no-deps awesome-ai-web-design caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile
docker compose -f compose.caddy.yaml up -d
curl -f http://127.0.0.1:18080/official-progress
```

容器僅在本機 `127.0.0.1:18080` 開放檢查用連接埠；代理網路內使用 `awesome-ai-web-design:8080`。正式入口需在既有 Caddy 加入所選網域的 `reverse_proxy awesome-ai-web-design:8080`，驗證完整設定後再平順重載。若網域已有網站，先確認使用子網域或替換首頁，並保留原設定供回復。

網站容器以非 root 使用者讀取唯讀檔案，設定 128 MiB 記憶體上限與健康檢查。切換 `current` 後無需重新建立容器；代理與其他網站不需重新啟動。

Caddy 文件：[靜態檔案](https://caddyserver.com/docs/caddyfile/directives/file_server)、[路徑對應](https://caddyserver.com/docs/caddyfile/directives/try_files)。

## 上線確認

以新網域確認設計目錄、搜尋、收藏、主預覽、分析與指令複製、單份和整包下載。另開啟幾份不同品牌的完整預覽、製作紀錄與圖片／影片，確認資源來自 VPS 的同源路徑。檢查 `/official-progress`、不存在路徑的 404，以及憑證與 HTTPS。

只有新網址確認可用後，才調整對外分享的網址。原有 Sites 版本仍可使用，這份部署包不會自動修改它。

## 2026-10-20 公開預覽說明

74 個品牌的預覽僅顯示參考日期、官網連結與簡短示範說明。`reference-sources.html` 提供公開來源清單；`official-progress.html` 保留開發比對紀錄。該次調整沿用當時的規格與指令；之後由上述實作規格版本更新下載內容。該次部署與驗證紀錄位於 `ops/PUBLIC-PREVIEW-NOTES-DEPLOYMENT.json` 及 `PUBLIC-PREVIEW-NOTES-VERIFICATION.json`。

## 2026-10-20 實作資料更新

全數主要規格可獨立使用，補充檔為 `TOKENS.json`、`starter.css`、`ASSETS.md`、`ASSETS.json`。同一助理使用 Starbucks、Stripe、Linear 三份凍結下載包實作前端案例，完成 24 項真實瀏覽器檢查；這不是獨立模型盲測或 74 種介面的完整驗收。

本次以約 2.9 MB 差異包建立新版本，未變動的檔案以硬連結保留；寫入變更時先建立新檔再原子替換，避免修改舊版內容。切換前核對全部 6,356 個檔案的大小與 SHA-256；網站容器與入口 Caddy 設定不需重新載入。

## 2026-10-20 功能驗收補強

修正 10 個品牌沿用舊版明暗分類的問題，讓篩選與色票依目前實作規格產出；調整兩處品牌摘要、收藏按鈕的 44px 觸控範圍及下載說明。每個 ZIP 補入 `LICENSE`、`ATTRIBUTION.md`。本次約 2.34 MB 差異包更新 83 個檔案，原始預覽與素材保持相同位元組。

25 項 Python 與 38 項 Node.js 檢查通過，另在正式框架建置後確認 27 項目錄與路由檢查通過。伺服器端逐一確認全部 6,356 個公開檔案可讀取且 Content-Length 與清單一致，不存在及隱藏路徑回傳 404。瀏覽器存取於 2026-10-21 恢復後，已完成下節的正式版操作驗收。

## 2026-10-21 最後驗收與下載修正

修正 320px 首頁示意圖造成的 18px 水平溢位。正式版的目錄、來源清單與三個詳細內容分頁已在 320、390、768、1280px 實際確認。公開頁面的搜尋、複合篩選、收藏重整與跨分頁同步、鍵盤、複製、下載及歷史預覽共 46 項瀏覽器檢查通過。

單份 Markdown 與歷史 HTML 的下載連結加入 `?download=1`；Caddy 僅對此查詢回傳 `Content-Disposition: attachment`，一般閱讀與 JavaScript 讀取仍維持原來的回應。已實際下載設計規格、AI 指令、歷史 HTML、單品牌 ZIP 與全部 ZIP，並核對檔案內容。所有 74 組規格／指令的附件回應及 75 個 ZIP 也通過公開 HTTPS 核對。

Caddy 候選設定先經驗證，保留設定檔 inode 後僅重新啟動本網站的靜態容器；共用入口設定未變更。設定更新與備份記錄在 `ops/EXPLICIT-DOWNLOADS-CONFIG.json` 及 `Caddyfile.before-explicit-downloads-2026-10-21`。目前設定摘要為 `2445e8cfc3094fece1e6c887da4eccad7dc20811041bb454874751dc65a9cec1`。

最終驗收含 737 個公開路徑的 HEAD 檢查及 235 個 GET／附件／ZIP 檢查；品牌檔案位元組與先前 737 份完整 GET 核對保持一致。主站沒有執行錯誤；保存的原始 Stitch iframe 會產生 Tailwind CDN 的開發使用警告，未改寫該原始匯出。
