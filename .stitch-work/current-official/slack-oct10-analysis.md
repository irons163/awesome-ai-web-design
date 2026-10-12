# Slack：目前公開首頁設計分析

官方來源：https://slack.com/，觀察日期2026-10-10。

保留白色首頁、Slack 官方字型、目前 AI 主標與六個客戶商標、五組產品示範、紫色六組 AI 示範、八則目前更新、Knowledge／People／Process／Platform 四段 UI、四個客戶故事、業務數字、六個 G2 徽章、四張深入資源卡、五條註腳與完整六欄頁尾。

Slack最終窄版高度12366px與官方相同。桌面11532px與官方最終11534px有2px示範影片相位差。90%指保持連結、43指團隊平均使用App數、87%指更有效協作；700M為每日訊息、4M為每週外部協作人數、3M為每日Workflows、1.7M為每週活躍Apps。不得改成供應商生成的其他定義。

完整官方頁面先以分段DOM保存，原生Google Stitch重新生成的結果與供應商說法保留。接著以今天官方的完整渲染DOM/CSS、字型與公開照片修正具體頁面；舊草稿及原生生成未被覆寫。

實際於1440×1000及390×844 CSS像素、DPR1、相同桌面UA逐段捲動、截圖與比較；390px是響應式窄版證據，並非真實手機硬體測試。兩尺寸均無水平溢位，已觀察的本地圖片皆載入，字型完成載入。已逐段檢視全部比較圖；影片時間、轉場及部分互動不同，不能推論全面官方一致。

## 仍有差異

- Desktop source height was11532px in an earlier captured phase and11534px in the final Ask Slackbot phase; local captured Plan launches phase is11532px. Different official video aspect metadata changes hero height by about2px. Narrow source/local are12366px.
- Original public videos are used but their frame times are not synchronized. Hero/AI text activation works locally; native Swiper pagination, swipe/drag, automatic cycling and all pillar option states are not fully implemented or verified.
- The latest-news Next control and footer Product expansion were activated and checked. This does not establish all carousel endpoints, disabled-state parity or every footer interaction.
- The current public menu main endpoint, Features expansion, Back and Escape were verified at390px. All desktop hover/focus/transition states and keyboard focus trapping remain outside this scoped review.
- The original cookie-vendor interface is excluded; Cookie Preferences opens an educational local dialog. Region/search and account/demo/sign-in services are not verified as official services.
- Two public asset fetches failed (an unused blob decoration and excluded cookie vendor icon); every observed local image in both final widths loaded. Real devices, other widths and final published deployment remain unverified.

驗收維持accepted=false。沒有採購、付費升級或部署；後續整合與正式網站驗證由主代理執行。

2026-10-11導覽識別清理：僅兩筆href移除_gl query key，其他視覺內容/CSS/runtime/assets逐位元保持不變。完整主頁比較hash及最終hash差異證明與桌面/窄版實際補拍分別保存；識別值不列於報告。accepted=false及先前差異維持。
