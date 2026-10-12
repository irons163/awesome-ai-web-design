"""Normalize only the eight assigned dated studies; never edit global progress."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import re
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'
NOTES = {
    'clickhouse': {
        'title': 'ClickHouse', 'url': 'https://clickhouse.com/',
        'design': [
            '現行首頁以深炭黑、白字與亮黃色構成。首屏置中大標「The leading database for AI」，Basier 字體、毫秒查詢／PB 規模說明、Start free cloud trial 與 Contact sales；下方保留 Langfuse 與 Managed Postgres 10X 公告。',
            '完整內容依序包含客戶品牌、四種用途、黃色客戶故事、Why ClickHouse 的優點與五張卡、整合、行列式資料庫說明、亮黃色 Deploy your way 三種部署、開發者社群、FAQ、試用 CTA、安裝指令與密集頁尾。390px 窄版改為堆疊。',
            '已另送真實 Google Stitch MCP 修正，保留原始輸出，再以日期限定官網完整 DOM、有效 CSSOM、樣式表、原始圖片與字型具體校正。早期桌面部分整合／資料庫動畫尚未顯示，另保留該歷史取樣；目前完整桌面來源已暖機重拍，不能以早期留白冒充目前完整畫面。',
            '最新校正還原官網桌面 --header-height:76px，避免客戶故事側欄被導覽蓋住；頁尾 50px 電子報區由真正公開 iframe DOM 與實測樣式重建。原 Latin Inter 字型宣告保留，表單移除隱藏追蹤、腳本及送出 action，按鈕不提交；訂閱功能與離線字型忠實度尚未驗證。',
            '10 月 11 日 root 已實際查看目前雜湊的完整桌面 14 段、390px 窄版 15 段及全部 8 張比較拼圖；頁高 9819／12542px 與目前來源相同，兩尺寸各 28 個可見標題幾何無量測差、無可見壞圖候選或水平溢位。這些只支持已取樣的主要靜態畫面比對，不支持動態或服務完全一致。',
        ],
        'limits': [
            'Canonical desktop reference was freshly warmed and recaptured in14 complete phases; earlier blank/load phases are retained separately under clickhouse-oct11-official-1280-before-warm-*. The invalid333px desktop diagnostic is excluded from current visual evidence.',
            'Marquees, counters, row/column chart GIF phases and FAQ left-side motion differ by time. Navigation, filters, FAQ, video controls and actual services remain unverified. Counts and customer wording are dated samples.',
            'The actual public newsletter iframe was reconstructed from saved DOM/computed styles. Hidden tracking fields, scripts and submit action are removed; button type=button. Subscription, validation and backend are not implemented or verified.',
            'Optional stylesheet3jrdzpyzqpmrl.css and a separate2c55 Cyrillic font subset returned ordinaryHTTP403 and were not retried or fetched by another route. Original external Latin Inter remains; the English form does not use that Cyrillic subset. Complete external CSS/offline font fidelity is unverified.',
        ],
    },
    'cohere': {
        'title': 'Cohere', 'url': 'https://cohere.com/',
        'design': [
            '現行企業 AI 首頁使用白色、米色、黑色與森林綠。頁首為 North2 公告與膠囊按鈕，首屏大標「Your AI. Your rules.」與 North 介面圖。一般動畫模式實測文字祖先 opacity 為 0、捲動往返仍留白；另以官網 prefers-reduced-motion: reduce 模式實際取得完整大標與 North 說明，這是目前靜態校正的明確範圍。',
            '後續可見 AI for Empowerment 大圖、Purpose-built AI、North 黑色產品卡、模型資料圖、Model Vault、安全部署、產業、客戶故事、NVIDIA 引言、安全標誌、海景 CTA 與黑色多欄頁尾。來源故事文案含 CoreWeave 90 天、Draftwise 30% 與 Fujitsu Takane，皆為當日原文。',
            '已透過新原生 Stitch 編輯，再依官網減少動態模式的完整 DOM、字型、圖片及有效樣式校正。此模式實際桌面頁高 8947px、窄版 10516px；原一般模式 8437px／9097px 留白證據另存。重製頁明確啟用來源 reduce CSS 分支，不宣稱一般動畫模式已驗證。',
            '桌面三張產品卡在來源會隨捲動堆疊，僅保留頁尾 DOM 的終點 transform 會讓 North／模型主文留白。本次追加真正可見的 2160／2880 捲動相位與 pin spacer 樣式，恢復卡片原文、素材、堆疊位置及首屏 48px 公告。來源取樣之間採位置投影，不宣稱 GSAP 時序相同。',
            '追加校正移除 North／Our models 內層文字的頁尾 translateY(-110.195px)，分別依 canonical 2160／2880 的實際標題位置投影，完整 active DOM 的內層樣式另存；Model Vault 原本沒有此偏移。窄版首屏還原 80px 公告下方原有 60px 標誌／選單列，離開首屏保留來源隱藏狀態。取樣之間的位移與導覽隱藏時間仍未驗證。',
            'root 已實際查看目前雜湊的桌面／窄版各 13 段、全部 8 張比較圖。26 個捲動位置對應、兩尺寸各 14 個標題幾何無量測差、頁高 8947／10516px 相同，無可見壞圖、溢位或覆蓋缺口；首屏窄版導覽與 2160／2880 的卡片文字均已複查。官網參照為減少動態模式，本機一般瀏覽器則顯示明確套用該可見 CSS 分支的靜態研究，不能延伸宣稱官網預設動畫模式一致。',
        ],
        'limits': [
            'Readable static reference is the actual official prefers-reduced-motion: reduce mode (D8947/N10516). Normal no-preference hero/headline reveals remained blank; those original captures are retained and normal animation parity remains unverified.',
            'Desktop stacked-card and announcement correction uses fresh actual2160/2880 active styles; fresh source body8867 differs from canonical8947. Canonical full evidence is retained. Between-sample timing and inferred65px last-card pin increment remain unverified.',
            'Independent inner-text translation is projected from actual canonical2160/2880 heading samples, with fresh active ancestor styles retained. Narrow scroll0 original logo/hamburger nav is restored below the80px announcement; nav-hide timing, Rive/video and logo carousel phases remain unverified.',
            'North video and logo carousel phases differ. Menus, industry/customer selections, industry/footer accordion behavior, forms, demo/sign-in and backend services are unverified.',
        ],
    },
    'mintlify': {
        'title': 'Mintlify', 'url': 'https://www.mintlify.com/',
        'design': [
            '現行首頁改為「The intelligent documentation platform」，使用近黑背景、薄荷綠流線、Arizona Flare 襯線標題與小型白色按鈕。左側主文、Agent traffic 標籤、文件介面圖與右下 Ask assistant 為目前來源；舊的 knowledge infrastructure 主標不可沿用。',
            '完整順序為 20,000+ 公司、六張 knowledge stack／24×7 agents 功能卡、Anthropic／Coinbase／HubSpot／AT&T 企業案例、300M+／2B+／99.99% 當日數字、Lovable／Kalshi／Decagon／Replit、新創與見證、三張最新文章、襯線收尾 CTA 及頁尾。窄版保留側邊露出的輪播卡。',
            '本次重新送交原生 Stitch；提供者草稿加入的辦公室照片與通用示範，不能當官網資產。來源校正改回原始文件／品牌圖與字型。流線與多個卡片實際是 canvas，僅複製 DOM 會丟失可見像素，需有原始像素或明確限定的靜態相位證據。',
            '每個尺寸保留 13 個初始可見 canvas 的實際像素作為靜態影格；水平隱藏的顧客卡 10／11 未曾露出，不能宣稱全部 15 個位置完成。Latest updates 三張則是原始 WebP 圖，不是 canvas；初次瀏覽器已有解碼尺寸但仍未繪出的黑畫面另存診斷，未改 HTML，暖機後重新拍攝才確認圖片正常。',
            'root 已實際查看目前雜湊的桌面 12 段、390px 窄版 15 段及全部 7 張新比較圖。頁高 8457／12555px 與來源相同，兩尺寸各 24 個標題幾何無量測差、無可見壞圖或水平溢位；此為暖機後主要靜態畫面的限定比對。',
        ],
        'limits': [
            'Thirteen actual initial-visible canvas bitmap phases per width (indices0..9,12..14) are preserved and displayed on original canvas boxes. Hidden horizontal customer-card slots10/11 remain unseen;26 static bitmap phases do not prove live canvas animation parity.',
            'Latest updates uses original WebP images. Initial decoded-but-unpainted black frames are preserved privately as mintlify-oct11-first-paint-* diagnostics; unchanged current HTML was fully recaptured after warming and the actual images then inspected. Cold first-paint timing is unverified.',
            'Frozen canvas wave, desktop brand/logo rotation, live counters/agent statistics and testimonial phases differ by time. Menus, carousels, Ask assistant, forms, Google sign-in, tabs and backend remain unverified; no paid account backend is used.',
        ],
    },
    'elevenlabs': {
        'title': 'ElevenLabs', 'url': 'https://elevenlabs.io/',
        'design': [
            '現行首頁為白／灰白、細格線與小交點，搭配精簡黑字、按鈕及淺色圓角卡。Elevenv4 公告下方主標「Bringing technology to life」，首屏 Creative／Agents／API 展示含彩色球體、語音範例、播放控制與產品分頁。',
            '下方保留 ElevenCreative／ElevenAgents、創作編輯與 Music／SFX／Voices／Image & Video、代理程式的全通路／分析／測試／防護／工作流、三種 API 程式碼、影響力、研究時間線至 Elevenv4／Dubbingv2／Musicv2、安全三卡、Flows／Government／Expressive Mode 更新及完整頁尾。',
            '已新送原生 Stitch，再依目前來源圖片、CSSOM 與完整內容校正。390px 原站有水平溢位與橫向卡列，不能把來源本身標成無溢位；音訊、API 與研究動態並未呼叫外部付費服務來假裝可用。',
        ],
        'limits': [
            'Official narrow capture has document overflow; horizontal card rows and all overflow causes must be judged from actual rasters, not an automatic zero-overflow claim.',
            'Audio playback/synthesis, Creative/Agents/API tabs, research canvases, exact timed phases and all signup/API services remain unverified.',
        ],
    },
    'miro': {
        'title': 'Miro', 'url': 'https://miro.com/',
        'design': [
            '現行首頁使用灰白留白、黃色 Miro 標誌、淡藍 CTA、細框圓角圖卡。「Human collaboration at the speed of AI」置中，搭配 email／Get Started Free、真正的研究／流程／圖表截圖與品牌列。',
            '下方是 Research／Roadmap & Planning／Diagrams／Workshops、Flow from idea to outcome、PepsiCo／ASOS／KW 當日案例、100M+／250+／6,000+、Innovation Workspace 六卡、AI platform for teamwork、六張入門資源與深色完整頁尾。',
            '已另送原生 Stitch 並改回來源原始圖與三段公開影片。Framer 同時保留多種響應式 DOM，不能將重複標題當成三套可見內容；桌面部分圖形顯示過渡留白，窄版則可見原圖，需以實際截圖辨認。',
            '首屏新增桌面與窄版真正顯示時的完整 hero 原始 DOM，保留裝飾圖祖先，避免頁尾擷取的退出 transform 讓 Customer Feedback／Flow Process 蓋住標題與表單。桌面六張功能卡依實際 track box 的 2880／3600／4320 捲動位置投影，不再以標題位置推測全部卡片；相位之間的 Framer spring 與收尾切換仍未驗證。',
            'root 已實際查看目前雜湊的桌面／窄版各 11 段及全部 6 張比較圖；桌面 3600／4320 的 Formats／Blueprints／Security／Integrations 另直接比對真正 active 官網圖。首屏大標與 CTA 均完整露出，頁高 7703／8910px 相同，無可見壞圖、溢位或覆蓋缺口；桌面仍保留 7 個幾何診斷差異，不能把主要畫面已比對改稱完全一致。',
        ],
        'limits': [
            'Framer responsive variants duplicate DOM headings while CSS controls actual visibility. Hidden/reveal desktop artwork and canvas/video phases are not established by total DOM heading counts.',
            'Active hero ancestors and measured desktop card-track boxes supplement the canonical first pass. Fresh settled3600/4320 spring phases differ slightly from canonical images; interpolation and final-phase transition remain static projections, not exact motion parity.',
            'Current desktop retains7 canonical heading geometry deltas: three40px entry-motion y shifts and four offscreen phase0 AI-platform heading geometry differences. Narrow heading deltas are zero. Early desktop lazy-image blanks are historical; fresh actual active reference images support the restored visible sections.',
            'Brie cursor/local overlay y, PepsiCo case videos, carousel and logo phases differ by time. Menus, product tabs, forms, signup/backend and actual team/agent services remain unverified.',
        ],
    },
    'opencode.ai': {
        'title': 'OpenCode', 'url': 'https://opencode.ai/',
        'design': [
            '現行 OpenCode 採棕黑底、細分隔線、Berkeley／IBM Plex 等寬字與像素字標。主標為「The open source AI coding agent」，下有 curl／npm／bun／brew／paru 安裝列、複製控制與原始示範影片區。',
            '完整內容包含 LSP／multi-session／share links／模型供應商等功能、社群圖與當日數字、Privacy、FAQ、Zen 模型、電子報、分格頁尾與 Anomaly 法律連結。後載入的來源為 200,000 stars、750 contributors、13,000 commits、10M monthly developers；不得把較早快速讀取的 150k／11k／6M 混入現行頁。',
            '已另送真實 Stitch 修正，再保留來源完整文字、字型、公開 demo MP4 與 poster 原始位元組。來源一開始頁高 3314px，後續長到 4209px；初次影片區留白與動態載入限制均保留，不把影片 URL 的存在當成播放驗證。',
        ],
        'limits': [
            'Source height changed from3314 to4209 during loading. Later source metrics/text are dated samples, not live GitHub/provider guarantees.',
            'Original demo/poster bytes are preserved; exact playback, copy/install tabs, FAQ, newsletter, desktop downloads and coding-agent services are unverified.',
        ],
    },
    'voltagent': {
        'title': 'VoltAgent', 'url': 'https://voltagent.dev/',
        'design': [
            '現行首頁以近黑點陣網格、薄荷綠、細邊程式碼／產品卡構成，頁首有開源公告。10 月 11 日新參照的桌面導覽包含 GitHub 10.8K、Discord 圖示與 Try VoltOps，已保留其完整原始 SVG／導覽內容，首屏及捲動導覽皆完成實際複查；數字僅代表取樣當時。首屏為 The end-to-end／AI Agent Engineering Platform、企業多代理說明、Get Started、npm 指令與右側原始連線圖。初次桌面文字留白，已另以真正顯示的官網桌面相位校正，不將舊留白當成完整首屏。',
            '完整順序為 Core Framework／VoltOps Console、程式碼與 console、公司列、Tool calling／Unified API／Dynamic Prompting／Persistent Memory 四卡、見證、Supervisor agent orchestration、Chain API 工作流、RAG／context 四卡、40+ apps、贊助者、社群三卡及完整頁尾。',
            '已新送原生 Stitch 並以真實來源素材校正。見證在離開區域後會從 DOM 卸載，另保留桌面／窄版可見時的完整 wrapper、62 張圖片元素與真實引言，並追加 9 個原始公開圖檔。Seth Rose 頭像在官網實際也 broken／404，保留原 URL，不製作虛構頭像。',
            '主代理已逐段檢查目前雜湊的桌面 14 段與窄版 14 段，並實際查看全部 8 張對照圖與桌面頁首；9755／11459px 範圍完整、沒有橫向溢位。Seth 頭像在來源與本機各有兩個取樣相位仍破圖，不能寫成零破圖。桌面首屏五個後段標題下移 25.890625px，與來源見證延遲掛載有關；已掛載的 26 個見證 h3 也造成初始 DOM 標題數不同。',
        ],
        'limits': [
            'Fresh settled desktop hero and mounted desktop/narrow testimonials supplement older full-page phases. Desktop official body changed from9729 to9755 when active content mounted; carousel/diagram/reveal phases are not synchronized.',
            'One exact Twitter avatar URL returned404 and remains unavailable; no substitute was invented. Diagram motion, code/console tabs, GitHub counts, menus and services remain unverified.',
        ],
    },
    'posthog': {
        'title': 'PostHog', 'url': 'https://posthog.com/',
        'design': [
            '現行 PostHog 為綠色草地插畫桌面、周圍 app 圖示、頂部功能列與淡綠應用程式視窗。RoundHog 黑字、橘黃按鈕及紫色頁籤構成「Your product’s context layer」首頁；不能換成通用紫色 SaaS 模板。',
            '視窗內依序有免費 setup 卡、Ask PostHog anything／Give agents product context／Ship with PostHog、Social proof、彩色客戶 logo、All your data、Usage-based pricing 表、Why PostHog、Bedtime reading、Shameless CTA，以及復古軟體盒 PostHog Web 廣告。setup 的 97% 與定價文內的 98% 原文矛盾分別保留。',
            '主要內容在 .app-scroll-viewport 內捲動；桌面內容 extent 4679／可見 629，窄版 extent 7725／可見 787，不能以 bodyHeight 720／844 判定全頁。早期 JPEG 窄版實際只有 390×219，已排除作完整證據；重新以明確 clip 取得 390×844 原始 PNG 後才可檢查。',
        ],
        'limits': [
            'Coverage must use element-scroll offsets/extent/visible_extent, not document bodyHeight. Superseded390x219 JPEGs are not complete narrow evidence.',
            'Tabs, dock/window actions, menus, cloud choices, MCP install actions, live counts and signup/account services remain unverified.',
        ],
    },
}


def read(name):
    return json.loads((WORK / name).read_text())


def digest(path):
    data = path.read_bytes()
    return {'path': str(path.relative_to(WORK)), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def image_size(raw):
    if raw.startswith(b'\x89PNG'):
        return struct.unpack('>II', raw[16:24])
    if raw.startswith(b'\xff\xd8'):
        offset = 2
        while offset < len(raw):
            if raw[offset] != 255:
                offset += 1
                continue
            marker = raw[offset + 1]
            offset += 2
            if marker in [216, 217]:
                continue
            length = int.from_bytes(raw[offset:offset+2], 'big')
            if marker in [192, 193, 194, 195, 197, 198, 199, 201, 202, 203, 205, 206, 207]:
                return (int.from_bytes(raw[offset+5:offset+7], 'big'), int.from_bytes(raw[offset+3:offset+5], 'big'))
            offset += length
    return None


def evidence(brand, role, width, current_hash):
    stem = f'{brand}-oct10-{role}-{width}'
    if brand == 'cohere' and role == 'official':
        stem = f'cohere-reduced-oct10-official-{width}'
    phases_path = WORK / (stem + '-phases.json')
    if not phases_path.exists():
        return {'phase_records': stem + '-phases.json', 'available': False, 'whole_page_covered': False,
                'proves_latest_draft': False, 'evidence_status': 'pending_actual_browser_capture'}
    frames = read(phases_path.name)
    expected = (width, 720 if width == 1280 else 844)
    shape_errors = []
    for index, frame in enumerate(frames):
        raw = (WORK / frame['screenshot']).read_bytes()
        size = image_size(raw)
        if size != expected:
            shape_errors.append({'phase': index, 'screenshot': frame['screenshot'], 'physical_dimensions': size})
    nested = frames[0].get('coverage', {}).get('coordinate_space') == 'element_scroll'
    extent = frames[-1]['coverage']['extent'] if nested else frames[-1]['bodyHeight']
    intervals = [(max(0, f['coverage']['offset']), f['coverage']['visible_extent']) if nested
                 else (max(0, f['scrollY']), f['viewport']['height']) for f in frames]
    end, gaps = 0, []
    for start, visible in sorted(intervals):
        if start > end + 1:
            gaps.append([end, start])
        end = max(end, min(extent, start + visible))
    if end < extent - 1:
        gaps.append([end, extent])
    hashes = {f.get('draft_sha256') for f in frames}
    bound = hashes == {current_hash}
    result = {'available': True, 'reference': stem + '-reference.json', 'phase_records': phases_path.name,
              'viewport': frames[0]['viewport'], 'physical_screenshot_dimensions_checked': True,
              'physical_dimension_errors': shape_errors, 'screenshots': len(frames),
              'coordinate_space': 'element_scroll' if nested else 'document_scroll',
              'initial_extent': frames[0]['coverage']['extent'] if nested else frames[0]['bodyHeight'],
              'settled_extent': extent, 'coverage_gaps': gaps,
              'whole_page_covered': not gaps and not shape_errors,
              'screenshot_files': [f['screenshot'] for f in frames],
              'captured_at_utc': [f['observed_at'] for f in frames],
              'visible_broken_image_candidates': max(len(f.get('brokenVisibleImages', [])) for f in frames),
              'horizontal_document_overflow_observed': any(f['bodyWidth'] > width for f in frames),
              'measurement_note': 'Coverage and zero broken-image candidates are diagnostics; only actual raster inspection supports visible-content conclusions.'}
    if nested:
        result['selector'] = frames[0]['coverage']['selector']
        result['visible_extent'] = frames[0]['coverage']['visible_extent']
    if role == 'local':
        result.update(proves_latest_draft=bound, draft_sha256_at_capture=list(hashes),
                      evidence_status='current_hash' if bound else 'prior_revision_not_latest_proof')
    return result


brands = sys.argv[1:] or list(NOTES)
assert set(brands) <= set(NOTES)
for brand in brands:
    meta = NOTES[brand]
    if not (WORK / f'{brand}-oct10-build-record.json').exists() or not (WORK / f'{brand}-oct10-native-original-downloads.json').exists():
        print(json.dumps({'brand': brand, 'pending': 'fresh native original exports/source build'}))
        continue
    now = datetime.now(timezone.utc).isoformat()
    preview = digest(WORK / f'{brand}.html')
    native = read(f'{brand}-oct10-native-original-downloads.json')
    assert native['native_screens'] and native['exports']
    for item in native['exports']:
        assert digest(WORK / item['path'])['sha256'] == item['sha256']
    assets = read(f'{brand}-oct10-assets.json')
    for item in assets['assets']:
        assert digest(WORK / item['path'])['sha256'] == item['sha256']
    original = []
    for name in ['DESIGN.md', 'PROMPTS.md', 'STITCH-PROMPT.md']:
        relative = f'design-md/{brand}/{name}'
        file = ROOT / relative
        if not file.exists():
            continue
        data = file.read_bytes()
        head = subprocess.run(['git', 'show', f'HEAD:{relative}'], cwd=ROOT, capture_output=True)
        original.append({'path': relative, 'sha256': hashlib.sha256(data).hexdigest(),
                         'unchanged_from_HEAD': head.returncode == 0 and head.stdout == data})
    assert all(x['unchanged_from_HEAD'] for x in original)
    proof = {}
    source_hashes = {}
    for width, mode in [(1280, 'desktop'), (390, 'narrow')]:
        source = read(f'cohere-reduced-oct10-official-{width}-reference.json' if brand == 'cohere' else f'{brand}-oct10-official-{width}-reference.json')
        html = ''.join(source['htmlParts'])
        # Browser JavaScript string length is UTF-16 code units, including emoji.
        assert len(html.encode('utf-16-le')) // 2 == source['html_length'] and hashlib.sha256(html.encode()).hexdigest() == source['html_sha256']
        assert html.endswith('</html>') and source['url'] == meta['url']
        source_hashes[str(width)] = {'html_sha256': source['html_sha256'], 'captured_at_utc': source['observed_at']}
        for role in ['official', 'local']:
            proof[f'{role}_{mode}'] = evidence(brand, role, width, preview['sha256'])
    local = [proof[f'local_{mode}'] for mode in ['desktop', 'narrow']]
    inspection_name = f'{brand}-oct10-raster-inspection.json'
    inspection = read(inspection_name) if (WORK / inspection_name).exists() else {}
    inspected = inspection.get('preview_sha256') == preview['sha256'] and inspection.get('all_latest_local_phases_visually_inspected') is True
    remaining = list(meta['limits'])
    if inspection.get('preview_sha256') == preview['sha256']:
        remaining.extend(inspection.get('remaining_differences_and_limits', []))
    if not inspected:
        remaining.append('Current preview still requires complete actual desktop/narrow raster inspection. Source reconstruction and provider output alone do not establish visual acceptance.')
    remaining.append('Other widths, physical devices, regions, complete interaction/motion and the published deployment are unverified.')
    result = {
        'brand': brand, 'inspection_date_local': '2026-10-11', 'normalized_at_utc': now,
        'accepted': False, 'official_consistency_claim': False, 'static_visual_acceptance': False,
        'status': 'in_visual_review' if any(x.get('proves_latest_draft') for x in local) else 'awaiting_actual_local_visual_review',
        'reference_url': meta['url'], 'scope': {'public_anonymous': True, 'service_actions_performed': False,
            'desktop': {'width': 1280, 'height': 720, 'dpr': 1},
            'narrow': {'width': 390, 'height': 844, 'dpr': 1, 'mobile': False, 'description': 'Responsive narrow desktop-UA browser, not a physical phone.'}},
        'preview': preview['path'], 'preview_sha256': preview['sha256'], 'preview_bytes': preview['bytes'],
        'method': 'Fresh genuine Google Stitch MCP edit retained unmodified, followed by current public DOM/effective CSSOM/stylesheet/original asset correction. Official scripts, tracking and service frames are excluded; forms are readonly.',
        'native_stitch': {'current_screens': native['native_screens'], 'original_downloads': f'{brand}-oct10-native-original-downloads.json',
            'request': f'{brand}-oct10-stitch-current-correction-request.json', 'full_response': f'{brand}-oct10-stitch-current-correction-response.json',
            'dispatch_result': f'{brand}-oct10-native-dispatch-result.json', 'original_exports_preserved': True, 'provider_images_are_not_browser_QA': True},
        'design_analysis_and_original_prompts': original,
        'public_assets': {'manifest': f'{brand}-oct10-assets.json', 'count': len(assets['assets']), 'failures': assets['failures'], 'tracking_excluded': True},
        'source_provenance': source_hashes, 'evidence': proof,
        'latest_draft_actual_browser_capture_available': any(x.get('proves_latest_draft') for x in local),
        'latest_draft_full_desktop_and_narrow_coverage': all(x.get('proves_latest_draft') and x['whole_page_covered'] for x in local),
        'actual_raster_inspection': inspection_name if inspection else None,
        'actual_raster_inspection_bound_to_current_preview': inspected,
        'remaining_differences_and_limits': remaining,
        'browser_connection': {'subagent_inventory': 'Chrome id1 only; direct createBrowserTab(iab, URL) without visible option returns Browser is not available: iab.',
            'root_iab_capture_used_where_present': True, 'bypass_used': False},
        'free_study': {'no_paid_runtime_dependencies': True, 'purchases_or_subscriptions_performed': False},
    }
    external_name = f'{brand}-oct10-external-css-assets.json'
    if (WORK / external_name).exists():
        external = read(external_name)
        result['public_assets']['remaining_external_css_dependencies'] = {
            'manifest': external_name, 'count': external['count'], 'hosts': external['hosts'],
            'note': 'Original public CSS references, primarily font variants; not all are used by these visible English phases. No claim that every CSS resource is locally preserved or rendered.'}
    if brand == 'cohere':
        result['scope']['prefers_reduced_motion'] = True
        result['scope']['static_motion_note'] = 'Official reduced-motion mode is the readable static reference; source reduce CSS branch is explicitly applied to this study. Original no-preference blank captures retained separately.'
        result['scope']['local_runtime_mode'] = 'Ordinary desktop-UA browser showing an explicitly applied static visible reduce-CSS branch; this is not evidence for default official motion.'
        result['scope']['default_official_motion_verified'] = False
    corrections = [f.name for f in WORK.glob(f'{brand}-oct11-*correction.json')]
    if corrections:
        result['source_corrections'] = corrections
    if brand == 'posthog':
        result['scope']['main_content_coordinate_space'] = 'element_scroll'
        result['scope']['main_content_selector'] = '.app-scroll-viewport'
        result['source_capture_note'] = 'Earlier390x219 JPEG exports superseded by explicit-clip PNGs; only current PNGs referenced by phases count as screenshot evidence.'
    design_name, prompt_name, review_name = [f'{brand}-oct10-{s}.md' for s in ['design-analysis', 'rewritten-prompts', 'visual-review']]
    (WORK / design_name).write_text(
        f'# {meta["title"]}｜2026-10-11 公開官網設計分析\n\n來源：{meta["url"]}。原始取樣時間保留於 UTC 紀錄，oct10 工作檔名不表示所有檢查都在 10 月 10 日完成。\n\n'
        + '\n\n'.join(meta['design'])
        + '\n\n保留原有 DESIGN.md、PROMPTS.md、STITCH-PROMPT.md；本檔為目前官網的日期限定補充。研究頁免費瀏覽、無付費執行時依賴，未執行購買或訂閱。\n\n'
        '驗證範圍為匿名公開首頁、1280×720 與 390×844、DPR 1、桌面 UA。實體手機、其他地區、完整互動與部署尚未驗證；accepted=false，不宣稱與官方一致。\n')
    request = read(f'{brand}-oct10-stitch-current-correction-request.json')
    dispatch = read(f'{brand}-oct10-native-dispatch-result.json')
    (WORK / prompt_name).write_text(
        f'# {meta["title"]}｜實際送交 Google Stitch MCP 的重寫指令\n\n'
        f'Project：`{request["projectId"]}`；selected screens：`{", ".join(request["selectedScreenIds"])}`；device：`{request["deviceType"]}`。\n\n'
        f'實際送出：{dispatch["started_at"]}；返回：{dispatch["completed_at"]}。完整原始回應、HTML、提供者 PNG 與下載雜湊另存。\n\n'
        '```text\n' + request['prompt'] + '\n```\n\n'
        '後續校正以實際官網截圖、完整 DOM、有效 CSSOM 與原始素材為依據。不得臆造圖片、數字或不可見動畫；每次修改都需以當前 SHA-256 重新驗證桌面及窄版。提供者生成圖、頁高相等或 DOM 中存在文字均不能替代實際畫面。\n')
    if brand == 'posthog':
        with (WORK / prompt_name).open('a') as output:
            output.write('\n指令轉錄更正：實際送出的原文誤把最後廣告的「$0 FREE」寫為「60 FREE」。目前來源 DOM 與完整 PNG 明確為刪除線 $0 加 FREE，來源校正保留 $0；不把誤寫內容帶入重製頁。原始送出指令保留供追溯。\n')
    if brand in ['clickhouse', 'cohere', 'mintlify', 'miro', 'voltagent']:
        correction_instruction = (
            '保留目前暖機後的完整官網參照與原始 Basier／Latin Inter 字型，桌面 html 的 --header-height 必須為 76px，使客戶故事側欄不與導覽重疊。頁尾必須保留真正公開 iframe 原文及實測樣式所重建的 50px Email／Sign up 區；不加入隱藏追蹤欄位、腳本或送出 action，按鈕為 type=button。外部 stylesheet3jrdzpyzqpmrl.css 與另一 Cyrillic 字型403原樣記錄，不重試、不換路；不能因此宣稱離線字型完整。使用當前雜湊的桌面14段與窄版15段實際畫面，將跑馬燈、計數器、圖表GIF、FAQ動態、表單及服務限制明寫；頁高與標題幾何相同不是完全一致。'
            if brand == 'clickhouse' else
            '保留黑底、薄荷綠流線、Arizona Flare襯線標題、完整知識與企業案例。依各尺寸實際canvas selector/index保留13個原始靜態影格（0..9、12..14），不可宣稱水平隱藏10/11已驗證或把靜態圖說成可播放動畫。Latest updates必須使用原始mintlify-index、state-of-docs-traffic、agent-score WebP；它們是IMG而非canvas，解碼尺寸或complete=true不代表已實際繪出。先暖機，逐段查看當前雜湊的完整桌面12段及窄版15段；保留first-paint黑畫面診斷、靜態canvas波形、logo與counter/testimonial時間相位、Ask／表單與服務未驗證限制。不得將來源匿名ajs_aid/_gl帶入公開導航；固定公開marketing參數可保留。'
            if brand == 'mintlify' else
            '以官網實際 prefers-reduced-motion: reduce 模式為靜態參照，保留一般模式留白證據。桌面公告在首屏為 48px，導覽位於公告下；捲動後導覽置頂。窄版首屏保留 80px 公告下的原60px Cohere標誌／hamburger。North、Our models、Model Vault 必須保留原始內容與素材，依已保存的 2160／2880 官網 active pin spacer／fixed top／scale 恢復堆疊，不可凍結頁尾 transform 造成空白；North／Models 內層文字另有 translateY 動作，必須參照 canonical標題位置與fresh完整祖先，不能全程保留終點 -110.195px。完整 canonical 8947／10516px 證據原樣保留；fresh active8867px 的差異及插值時序須公開限定。'
            if brand == 'cohere' else
            '使用已保存的桌面／390px active hero 完整祖先 DOM 與真實原始 SVG；Customer Feedback／Flow Process 圖不可蓋住大標、email 或 CTA。桌面 Innovation Workspace 保留原始六卡，依實測 card track box 2880px→x160.867、3600px→x-1340.001、4320px→x-2840.569 投影，不能只用標題 x 猜所有圖卡位置。新 settled 與 canonical spring 相位均保留，插值與進入 AI platform 的切換不宣稱精確動畫一致。'
            if brand == 'miro' else
            '保留近黑點陣、薄荷綠、真實連線圖與完整產品內容。桌面原始導覽必須包含取樣當時 GitHub 10.8K、Discord 圖示與 Try VoltOps，首屏及捲動版皆以 fresh official 完整 nav／SVG 為依據，不可只保留一枚 GitHub badge。保留實際 mounted 的桌面與窄版見證全文及原始頭像；Seth 頭像原 URL 在官網與本機均 404，不得虛構替代圖或聲稱零破圖。以目前雜湊的兩尺寸各14段完整畫面逐段檢查；來源初始9729px到見證掛載9755px、五個下方標題25.890625px差與26個見證標題掛載差須明列。Logo、見證、YouTube 卡、整合圖示、流程點與Discord文字動作、程式碼與console、導覽、剪貼簿及服務均不得僅依靜態圖宣稱已驗證。')
        with (WORK / prompt_name).open('a') as output:
            output.write('\n## 新增來源校正規格（供後續重製使用；此段尚未重送 Stitch）\n\n' + correction_instruction
                         + '\n\n保持研究免費，不加入付費執行時依賴或虛構後端。修改後以目前檔案雜湊重新拍攝並逐段查看完整桌面及窄版，列出可見差異、其他尺寸與互動限制；未實際查看的畫面不得宣稱與官方一致。\n')
    table = ['| 取樣 | 座標範圍 | 實際影像數 | 完整範圍 | 目前重製檔 |', '|---|---|---:|---|---|']
    for name, item in proof.items():
        if not item['available']:
            table.append(f'| {name} | 尚待實際取樣 | 0 | 否 | 否 |')
            continue
        table.append(f'| {name} | {item["coordinate_space"]}：{item["settled_extent"]}px | {item["screenshots"]} | '
                     + ('是' if item['whole_page_covered'] else '否') + ' | '
                     + ('官網來源' if name.startswith('official') else '是' if item['proves_latest_draft'] else '否；較早修訂') + ' |')
    (WORK / review_name).write_text(
        f'# {meta["title"]}｜2026-10-11 畫面校正紀錄\n\n來源：{meta["url"]}。目前重製檔 SHA-256：`{preview["sha256"]}`。\n\n'
        '**accepted=false；不宣稱與官方一致。** 已完成新原生 Stitch 編輯與具體來源校正；實際畫面證據與未完成項目分別記錄。\n\n'
        + '\n'.join(table) + '\n\n'
        + ('已逐段查看對應目前檔案的所有本機截圖；仍須遵守下列可見差異與限制。' if inspected else '目前檔案尚未完成桌面及窄版所有本機畫面的實際逐段檢查；不能把來源截圖或提供者生成圖當成本機驗證。')
        + '\n\n' + '\n'.join('- ' + x for x in remaining)
        + '\n\n量測為輔助診斷，零壞圖候選或頁高相同不代表像素、文字、版面、動畫或服務完全一致。\n')
    result.update(design_analysis=design_name, rewritten_prompts=prompt_name, visual_review=review_name,
                  provenance=f'{brand}-oct10-provenance.json', publication_manifest=f'{brand}-oct10-publication-manifest.json')
    result_path = WORK / f'{brand}-oct10-result.json'
    backup = WORK / f'{brand}-oct10-pre-current-result.json'
    if result_path.exists() and not backup.exists():
        backup.write_bytes(result_path.read_bytes())
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    refs = {f['screenshot'] for role in ['official', 'local'] for width in [1280, 390]
            if (WORK / f'{brand}-oct10-{role}-{width}-phases.json').exists()
            for f in read(f'{brand}-oct10-{role}-{width}-phases.json')}
    refs.update(f'{brand}-oct10-{role}-{width}-{kind}.json' for role in ['official', 'local'] for width in [1280, 390]
                for kind in ['reference', 'phases'] if (WORK / f'{brand}-oct10-{role}-{width}-{kind}.json').exists())
    direct_assets = sorted(set(re.findall(re.escape(brand) + r'-assets/[a-zA-Z0-9._/-]+', (WORK / preview['path']).read_text())))
    assert all((WORK / name).is_file() for name in direct_assets)
    auxiliary = [f for f in [*WORK.glob(f'{brand}-oct10-*'), *WORK.glob(f'{brand}-oct11-*'), *WORK.glob(f'{brand}-reduced-oct10-*')] if f.is_file() and f.suffix in ['.json', '.md', '.png', '.jpg', '.html']
                 and f.name not in [f'{brand}-oct10-provenance.json', f'{brand}-oct10-publication-manifest.json', f'{brand}-oct10-result.json']]
    provenance = {'brand': brand, 'accepted': False, 'official_consistency_claim': False,
                  'normalized_at_utc': now, 'preview': preview,
                  'historical_analysis_and_prompts': original, 'source_provenance': source_hashes,
                  'native_originals': native, 'public_original_asset_manifest': f'{brand}-oct10-assets.json',
                  'evidence_and_instruction_files': [digest(f) for f in sorted(auxiliary)],
                  'source_and_provider_originals_unmodified': True,
                  'note': 'Raw full-source HTML, captures and bundles are private provenance. Do not recursively stage or publish the work directory.'}
    (WORK / result['provenance']).write_text(json.dumps(provenance, ensure_ascii=False, indent=2) + '\n')
    manifest = {'brand': brand, 'accepted': False, 'official_consistency_claim': False,
                'preview': preview, 'study_text': [design_name, prompt_name, review_name],
                'public_asset_manifest': f'{brand}-oct10-assets.json',
                'required_local_assets': [digest(WORK / name) for name in direct_assets],
                'publish_allowlist': [preview['path'], design_name, prompt_name, review_name] + direct_assets,
                'native_original_exports': [item['path'] for item in native['exports']],
                'native_export_note': 'Preserve originals as provenance. These are provider drafts, not actual browser QA.',
                'evidence_references': sorted(refs),
                'exclude_from_recursive_publication': ['*-asset-bundle.json', '*-reference.json', '*-phases.json',
                    '*-phase-*.png', '*-phase-*.jpg', '*-response.json', '*-pre-*.html'],
                'publication_note': 'Root owns source synchronization, global review and deployment. This manifest does not claim publication.'}
    (WORK / result['publication_manifest']).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'brand': brand, 'sha256': preview['sha256'], 'source_full': all(proof[f'official_{m}']['whole_page_covered'] for m in ['desktop', 'narrow']),
                      'latest_local_full': result['latest_draft_full_desktop_and_narrow_coverage'],
                      'actual_local_rasters_inspected': inspected, 'required_assets': len(direct_assets), 'accepted': False}))
