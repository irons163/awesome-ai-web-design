# Expo｜2026-10-10 畫面校正紀錄

來源：https://expo.dev/。目前重製檔 SHA-256：`c81b3aad7dd173067205cbc81e5670646ff747e5475709e46c631a218a39d5d2`。

**accepted=false，不宣稱與官方一致。** 主代理已實際檢視全部7張對照接觸圖及原生 Stitch 圖；本補充整理保存證據，沒有宣稱子代理獨立檢視了未觀看的畫面。

| 實際取樣 | 頁高 | 分段數 | 全頁覆蓋 | 對應目前檔案 |
|---|---:|---:|---|---|
| official_desktop | 8436 | 12 | 是 | 官方取樣 |
| official_narrow | 10998 | 14 | 是 | 官方取樣 |
| local_desktop | 8436 | 12 | 是 | 是 |
| local_narrow | 10998 | 14 | 是 | 是 |

桌面12個、窄版14個保存捲動位置均與來源對應；量測沒有可見破圖候選或橫向溢位。詳細幾何與對照圖清單見 expo-oct10-layout-comparison.json。

The metallic SDK canvas motion is absent; the underlying original static Expo artwork remains. A44px footer canvas gradient is missing.

Hero app-icon ribbon, native-code carousel, testimonials and dark CTA orb phases are not synchronized with the source. The official desktop phase8 usage/community reveal was blank while the local static content was visible.

Building blocks preserves the sampled active pause icon, but pause/tab behavior is unverified. Menus, theme controls, account/contact/services, real devices and deployed-site behavior are unverified.

Desktop one recorded heading has a20px Y difference; narrow heading geometry has no recorded differences. Equal page height and matching heading geometry do not establish visual consistency.
