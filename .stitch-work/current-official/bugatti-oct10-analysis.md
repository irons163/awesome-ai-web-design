# Bugatti 目前公開首頁設計分析

來源 https://www.bugatti.com/，觀察2026-10-11。當日仍為Destrier電影主視覺，Menu/BUGATTI/Store透明導覽、原始Destrier手寫SVG、等寬宣傳文字與桌面描邊/窄版底線CTA。三種原始字型Bugatti Display/Text/Monospace，黑色頁底；桌面48px邊距、60px大標，窄版12px邊距、36px大標與直排內容。招聘提示經可見Close關閉後比較，初始實拍另保存。

完整順序為La Maison三卡、Programme Solitaire與Sur Mesure兩支原始影片、HONMA/C SEED當日生活風格卡、六車型Tourbillon/W16 Mistral/Bolide/Chiron/Divo/Centodieci網格、BUGATTI Live、原始手寫引言與四欄完整頁尾。當日社群格沒有文章，桌面顯示Load more、窄版隱藏；未加入虛構社群內容。

官方GSAP平滑捲動會讓scrollY先改變而可見內容尚未到位；一般截圖在這個網站不構成完整可靠證據。已保留錯誤步距/未穩定的早期資料，校正為半量wheel並逐段讀取smooth-content矩陣，直到translationY≈-scrollY誤差小於0.15px且連續三次穩定才拍攝。來源主標docY於整頁約0.06px內穩定，完整桌面10段7112px、窄版11段8584px；真實1280×720/390×844尺寸、連續覆蓋、完整來源長度/hash/結尾均檢查。

genuine Google Stitch MCP新桌面稿保留完整指令/回應/rawHTML/未改縮圖/fullPNG；具體成品再用完整當日DOM/CSS與107份原始素材校正，匯出/傳輸失敗分別保留並補回，最終素材失敗0。取消來源固定平滑容器，改為原生文件捲動，照片採原始scale1.1靜態裁切。三支主頁影片實測readyState4，兩支同畫面可見影片已播放超過1秒；所有20張DOM圖片與字型載入、無溢位，16個主要標題座標/尺寸在兩寬均誤差不超過0.01px。全部4張桌面與5張窄版比較圖目視核對；成品頁尾總長仍比來源多7/8px，保留差異。

- The preview restores native document scrolling from the official fixed smooth-wrapper/translated smooth-content. Official source was explicitly allowed to settle before every screenshot. Exact smooth scrolling, reveal/blur timing, parallax positions and image crop movement differ; source composites visibly contain changing parallax crops between phases.
- The original3public main-page videos load and play (readyState4; two visible videos observed progressing above1s). Their frames and initial playback timing differ. No frame-by-frame, model hover-video or desktop/narrow movie synchronization is accepted.
- Source/corrected page heights are7112/7119px desktop (+7) and8584/8592px narrow (+8). All16main H1/H2/H3 texts and bounds match within0.01px at both widths; the remaining footer/end-canvas geometry is not accepted as exact parity.
- Recruitment toast was dismissed through its public Close button before full-page review; its actual initial screenshot is preserved. Menu/drawer, category/hover model states, social Load more, privacy/cookie and language controls, full keyboard/focus behavior and destination/service routes are not implemented or accepted by this static correction. The source social grid had no posts, with a desktop Load more button and hidden narrow grid; no invented posts were added.
- Fresh genuine Stitch edit is DESKTOP only. Prior original DESKTOP/MOBILE/DESIGN.md/design-md remain preserved. Other sizes, real phone hardware, locales/routes and published deployment are not reviewed.

accepted=false；未付費、未部署、未提交帳戶/表單，帳戶計費未稽核。
