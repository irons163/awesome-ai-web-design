# Warp 目前公開首頁設計分析

來源 https://www.warp.dev/，2026-10-11實際觀察。當前首頁已新增「Your software factory, defined in code.」完整配置區，不能沿用舊版頁面。白色與淡紫紙張背景、細黑線、技術等寬字體、74px桌面邊距、56px兩行主標、皇家藍#2818F4和淡黃色Book a demo共同構成新版。英雄區8×28任務格、17個當日品牌證明、八個配置類別及23行factory.yaml、六項SDLC、三個品質指標、藍色成本案例、企業故事、四層開放架構、治理圖表、三項產品、九項FAQ和完整2026頁尾均保留。

新版已透過 genuine Google Stitch MCP 產生獨立校正候選。原始完整工具回應、供應者HTML、全尺寸PNG和縮圖，以及舊候選/DESIGN.md/design-md均分別保留。以完整分塊官方DOM、CSS和84份公開原始素材進行實際頁面校正；成本圖表另保存兩份官方實際視窗擷取，明確標記為靜態canvas記錄。

桌面1280×720與窄版390×844各14與17段實際JPEG，完整覆蓋9395px與14041px頁高。PIL逐張確認影像尺寸，檢查頂部、頁尾、連續捲動和HTML SHA256；5張桌面與8張窄版比較圖均已目視檢查。兩尺寸各70張本機DOM圖片全部載入，字型完成且無水平溢位。最後只移除兩張圖表誤套的圖片外框，另附確切hash差異證明與兩尺寸實際補拍。

- The 224 task-grid statuses, PR counts, live roster, logo marquee position, section boot text and reveal opacity differ by captured animation phase. The corrected page retains observed static task/roster states and CSS motion. Exact timing is not accepted; the official narrow source itself was captured with several headings mid-fade.
- The cost-per-PR canvas is represented by dated crops of actual official desktop/narrow screenshots, with provenance and independent bounds. It is a static drawing without hover, scrubbing or live recomputation. The computer-use story is a captured illustrative state, not a working browser or sales form.
- The header is restored at scrollY0 and blue desktop section navigation appears after scrolling. The 64px local swap threshold was not independently established as the exact official threshold; transitional positions are not accepted.
- Configuration directory tabs, folder expansion, SDLC switchers, the mobile menu, sign-in/get-started popovers, FAQ expansion, operating-system switchers, copy/download actions and sound controls were not implemented or accepted as complete official interaction parity. Public destination links are retained; no account action, form submission, command execution or download installation was performed.
- The fresh native Stitch output is DESKTOP only. Its declared 2560×16384 screenshot exports as an actual 2560×16383 PNG; no fresh native MOBILE output is claimed. Provider assertions of authenticity, a live stdout runner stream and +3.7x are not validation; the source-corrected page retains the observed SDLC image and +3.7.
- Other pages, account/product services, real phone hardware, untested widths and published deployment are outside this review. accepted=false; no comprehensive official-equivalence claim.

未購買、未付費升級或部署；帳戶計費未稽核。

## 2026-10-12 驗證版本綁定校正

完整整頁比較屬8a483c…歷史稿；目前65894e…只有兩個圖表class不同，逆替換已精確還原舊SHA；圖表局部補驗另列，補圖無原始capture-time HTML SHA，未宣稱目前稿整頁重拍。

Full current-SHA D/N page recapture was not performed. Historical full-page screenshots bind to8a483c…; exact two-class normalization proves unchanged bytes elsewhere. Final chart-only screenshots were associated with65894e… in the subsequent result/diff proof; their original metadata does not record capture-time HTML SHA.

完整歷史phase JSON未改寫，也沒有補造capture-time SHA。`currentFullPageCaptureComplete=false`、`currentFullPageComparisonComplete=false`；歷史完整觀察與精確未變範圍/局部補驗分開記錄，accepted=false。
