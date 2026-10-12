# Uber 目前公開首頁設計分析

來源 https://www.uber.com/ca/en/，觀察2026-10-11。加拿大英文網址在本次公開工作階段自動顯示Taipei, CA / Taipei，頁尾為Uber Formosa公開登記文字；沒有要求或授予定位權限，也不推定使用者精確位置。新版已替換10月5日舊稿的account/Reserve段落，採黑白大區塊、64px固定黑導覽、UberMove/UberMoveText字型、52px/64桌面Go anywhere與32px/40窄版主標。桌面hero左右欄各459px，保留真實旅遊拼貼、取車/下車欄與Pickup now、Schedule ahead。

完整順序為六種服務卡、How to request a ride步驟圖庫、City Hub、More ways三卡、Uber Eats大圖與餐食/寵物卡、Uber One、家庭車輛大圖、Earn圖庫、Business、雙App下載與完整公司/產品/公民/旅遊/社群/商店/法律頁尾。保留當日真實官方照片、車輛圖示、SVG、QR與影片，未沿用生成稿的虛構會員優惠或錯誤App名稱。

genuine Google Stitch MCP新增當日桌面校正屏幕，完整指令、回應、原始HTML/縮圖/fullPNG分開保留；具體頁面再以完整當日官方DOM/CSS及154份公開素材校正。pageAssets有30項匯出失敗，精確已觀察公開網址下載補齊後素材失敗0。已修正窄版頂部固定價格列的顯示，來源與成品桌面11段7540px、窄版10段7860px完整實拍；真實尺寸、連續覆蓋、hash及完整來源長度/結尾檢查通過。全部4張桌面與4張窄版比較圖已目視核對，修正後頂部再核對。桌面66張、窄版78張DOM圖片載入、字型完成、無溢位；52個H1/H2/H3文字與座標尺寸逐項相合。主標桌面x64/y160/459×64、窄版x24/y136/342×40。

- The Canadian-English URL automatically rendered Taipei, CA / Taipei and Uber Formosa public footer content. Only this observed regional variant is reviewed; no location permission or geographic variant change was performed.
- City Hub video and animated Journey-line frame timing differs; original media is retained. Sticky header/bottom CTA repeat in sequential composites and can obscure a strip of content; these composites are not single full-page screenshots. Narrow top CTA visibility was corrected and rechecked, but exact transition thresholds/timing are not accepted.
- The captured initial galleries are retained (desktop ride steps1/2; narrow ride steps1/5 and other galleries1/3). Gallery paging, menus/mobile drawer, language/city/pickup date controls, autocomplete/location permission, full keyboard/focus, ride requests/reservations, authentication, earning and membership/service flows are not implemented or accepted. Route inputs are readonly in the static source correction; action links lead to observed official services. No account/location/form submission occurred.
- Fresh genuine native correction is DESKTOP only. Prior original native desktop/mobile/DESIGN.md/design-md remain preserved. Other sizes, real phone hardware, other routes/locales and published deployment are not reviewed.

accepted=false；未付費、未部署，帳戶計費未稽核。
