# Clay Global｜2026-10-10 畫面校正紀錄

來源：https://clay.global/；1280×720 桌面及390×844窄版桌面 UA，匿名公開首頁。目前重製檔 SHA-256：`0233496e15c11e3b6549933876ddb38953123416d2ae99e1ccca282f361c2950`。

**accepted=false，不宣稱與官方一致。** 實際畫面最終判讀由主代理負責；此補充整理保存的量測與主代理回報，沒有將未檢視的畫面稱為已通過。

| 實際證據 | 頁高 | 分段數 | 保存範圍完整 |
|---|---:|---:|---|
| official_desktop | 15667 | 22 | 是 |
| official_narrow | 15618 | 19 | 是 |
| local_desktop | 15667 | 22 | 是 |
| local_narrow | 15618 | 22 | 是 |

保存量測中沒有矩形可見破圖候選或橫向溢位，桌面與窄版來源／重製總頁高分別同為15667／15618px。這些數字只支持所列取樣，不能證明畫面一致。最新本地分段記錄綁定目前重製檔雜湊。主代理檢視11張較早完整對照圖，以及最後修正影響的桌面／窄版頁首與 Fintech 對照。窄版17個捲動位置配對，另2個官方位置因實際平滑捲動時間點未配對，不宣稱41張精確配對或像素一致。詳細幾何差異與接觸圖清單見 clay-oct10-layout-comparison.json；若目前分段數與該較早比較檔不同，應以最新 phase 清單為範圍紀錄。

Root actual review found differences in public video frames, logo/reveal timing and3D states. Desktop hero and fintech artwork use explicitly observed static cropped-region fallbacks; these do not reproduce live3D motion.

The footer3D artwork is missing. Header/menu, service accordions, FAQ, contact actions and other UI behavior have not been fully verified.

Narrow sampled reveal/heading states differ; recorded heading Y positions differ by up to843.812px. Reveal/timing/static-state effects remain scoped limits; equal total height is not visual acceptance.

Root reviewed all11 earlier final comparison sheets and latest affected top/fintech desktop/narrow sheets after the header-filter/fintech-background corrections. The latest local phases embed the current draft hash. Narrow has17 matched source/local scroll positions and2 unpaired official positions caused by actual smooth-scroll phase; this is not41 exact paired screenshots or pixel parity.
