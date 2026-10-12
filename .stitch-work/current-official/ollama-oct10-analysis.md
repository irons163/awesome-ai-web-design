# Ollama 目前公開首頁設計分析

來源 https://ollama.com/，實際觀察及最後校正2026-10-11。官方已從舊版長頁改為精簡白色首頁：細黑線羊駝、右側導覽與182.7K GitHub顯示值、22px主標、20/28px說明、黑色 Get started 圓角按鈕。保留當日官方宣稱的9M+、1B+、200T+，只作有日期的版面內容記錄；十二個灰色公開品牌商標、寬敞右側留白與完整頁尾來自目前官方DOM/CSS/資產。窄版商標改為三欄四列，並有五個連結的全白選單。

新版與原保存設計不同，因此透過 genuine Google Stitch MCP 新增校正屏幕。原候選、完整工具回應、供應者文字/建議與新原始HTML/全尺寸PNG/縮圖分別保留。以完整官方來源及19份公開原資產校正可操作本機頁面，未將供應者的精確性宣稱當成驗證。

1280×720與390×844各兩張實際視窗截圖完整覆蓋786px與1000px頁高；PIL確認實際影像尺寸、頂部/底部與捲動覆蓋。四張逐視窗比較圖與窄版開啟選單圖均已目視檢查。兩尺寸各13張DOM圖片均載入、字型完成、無水平溢位。文字、商標、主要區塊及頁尾位置相合；細線與選單捲軸差異列於下方。

- The narrow captured end-state header retains data-scrolled at the top, so a one-pixel gray bottom rule is visible locally at scrollY0 while the source top screenshot has no rule. The source and local rule agree after scrolling.
- The native CSS narrow menu opens and closes with the same five links. The local open-menu screenshot retains a visible vertical scrollbar; the source open-menu screenshot hides it. Scroll locking and full keyboard/focus parity were not accepted.
- The fresh Stitch output is a DESKTOP candidate (2560×2048), and its provider response omits the current Meetups footer link. The source-corrected preview retains the actual public link. No new native MOBILE screen was generated.
- Sign-in, account creation, model downloads, other pages, real phone hardware, other viewport widths and published deployment are outside this review. No account forms were submitted.

accepted=false，沒有宣稱全面官方一致。沒有購買、付費升級或部署；帳戶計費未稽核。
