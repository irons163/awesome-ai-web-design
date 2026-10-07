# Mastercard Stitch mobile response

Native generation output is preserved below. Fidelity claims and the separate generated design system have not been accepted as measured comparisons with the official site.

Here is the faithful, dated mobile study of the actually rendered Mastercard Taiwan Traditional Chinese homepage (https://www.mastercard.com/tw/zh.html) observed on 2026-10-07, tailored strictly for a 390px mobile viewport (390×844 base, ~8,800px full scrolling layout).

### Key Architectural & Design Decisions

1. **Mobile Layout & Viewport Geometry**:
   - Fixed viewport width to `390px` with 20px edge margins and 350px core content blocks, preventing any horizontal overflow.
   - Set major titles to `48px` with `52.8px` line-height and `-0.96px` tracking, exactly wrapping as observed. Feature and service headings render at `24px / 28.8px`.

2. **Brand Visual Foundation & Typography**:
   - Integrated the official `mccom` font-face (`@font-face` pointing to Mastercard’s public CDN font resources) with SofiaSans/Arial/sans-serif fallbacks.
   - Built with the exact warm cream `#F3F0EE` background, near-black `#141413` text and footer, crisp white capsule cards, and brand orange/red accent markers (`#FF5F00` / `#EB001B`).
   - Integrated the official Mastercard double-circle brand symbol (`ma_symbol.svg`).

3. **Faithful Section Structure & Authentic Content**:
   - **Hero Welcome Video (`0,0,390,693.328`)**: Integrated the portrait `9:16` video stream (`homepage-video-zh-TW_9x16_.mp4`) with inline autoplay, muted status, 13.86s native duration, and interactive Play/Pause/Replay and Unmute/Mute controls. No redundant overlay CTA was added.
   - **News Carousel (驅動經濟，賦能民眾)**: Features the 3 observed slides (*梅西交換球衣*, *Mastercard 影響報告*, *新旅行方案*) using mobile dynamic media assets (`width=480&quality=82&preferwebp=true`), with frosted title capsules, touch/swipe handling, play/pause, and pill indicators.
   - **Solutions Hierarchy (共創無價可能)**: Stacked the 6 service items (*觀點洞察*, *個人消費與商務支付*, *資金流動*, *資訊安全與詐欺防制*, *消費者拓展與互動經營*, *開放式金融*) into an organic, alternating sequence of circle and vertical capsule shapes with asymmetric offsets and orange category dots.
   - **Cards & Benefits (支持您實現目標的權益與服務)**: Centered artwork within tall outlined white capsules for both *尋找適合您的卡片* (with realistic Touch Card) and *隨心支付*.
   - **Priceless Experiences (點燃熱情的精彩體驗)**: 16:9 video-poster player utilizing the official Messi priceless poster asset, paired with *Priceless Specials* and *Travel Rewards* feature capsules linking to official endpoints.
   - **Near-Black Accessible Footer**: Collapsible accordion navigation for all four groups (*需要幫助嗎？*, *公司*, *法律與隱私*, *萬事達卡網站*), brand social icons, localized Taiwan country selector, and official legal disclaimer row.
   - **Accessible Drawer & Dismissible Cookie Notice**: Header hamburger opens a slide-over mobile navigation menu, and the bottom cookie banner provides functional *接受cookies* / *全部拒絕* controls.

"Add interactive drawer navigation animation"

"Inspect Touch Card tactile detail on mobile"

"Preview dark-mode variant for the mobile viewport"

