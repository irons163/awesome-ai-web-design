"""Self-contained implementation documents with explicit value provenance."""
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path

VERSION = '2026-11-01'
FONT = '"Noto Sans TC", "PingFang TC", "Microsoft JhengHei", system-ui, sans-serif'
PROPERTIES = {
    'accent': '主要操作背景', 'on-accent': '主要操作文字', 'canvas': '頁面背景',
    'ink': '主要文字', 'muted': '次要文字', 'surface': '內容卡片背景',
    'border': '分隔線及卡片邊框', 'focus': '鍵盤焦點外框',
}
COMPOSITIONS = {
    'colorful-creation': {'name':'視覺創作工具首頁','sections':['精簡導覽','置中漸層主視覺與兩排浮動圖形','工具分類與不等寬功能卡','雙欄產品介紹','雙排橫向範本展示','創意生態系統','漸層行動呼籲與頁尾'],'hero':'紫、藍、青綠垂直漸層搭配置中大標、白色按鈕與兩排漂浮圖形。後續工具區有五個可切換分類與四張不等寬圖片卡。','media_ratio':'4 / 3','image_count':12,'max':1360,'gap':16,'padding':24,'radius':24,'button_radius':10,'hero_desktop':64,'hero_mobile':38,'body':16},
    'career-explore': {'name':'職涯社群首頁','sections':['白底導覽與左文右插圖主視覺','熱門內容與職缺分類','刊登職缺','軟體工具與遊戲分類','職涯圖文介紹','人脈與學習插圖','適用對象','加入社群及多欄頁尾'],'hero':'白底左側大標及兩個上下排列的膠囊操作，右側大型人物插畫；手機改為上下排列。','media_ratio':'4 / 3','image_count':4,'max':1200,'gap':24,'padding':24,'radius':12,'button_radius':999,'hero_desktop':48,'hero_mobile':32,'body':16},
    'finance-intro': {'name':'支付服務首頁研究','sections':['白底導覽與淺藍主視覺','個人／公司切換與大幅圖片','交錯雙欄功能介紹','安全性大圖與說明','橫幅圖片','傳送／要求付款示意','應用程式與頁尾'],'hero':'大面積淺藍背景，上方置中個人與公司膠囊切換，接黑色兩行大標與白色圓角圖片卡；圖片僅作公開首頁參考，不提供付款服務。','media_ratio':'16 / 10','image_count':4,'max':1200,'gap':24,'padding':24,'radius':40,'button_radius':999,'hero_desktop':84,'hero_mobile':48,'body':16},
    'craft-market': {'name':'手作靈感市集','sections':['橘色識別與分類導覽','左右不等寬主題圖片磚','四欄精選主題','季節與節慶商品','禮物及熱門分類','居家指南','Etsy 介紹及頁尾'],'hero':'暖白底與橘色品牌字，下方使用不等寬雙欄主題磚；左磚再分文案與圖片，手機依閱讀順序堆疊。','media_ratio':'4 / 3','image_count':12,'max':1280,'gap':24,'padding':20,'radius':12,'button_radius':999,'hero_desktop':48,'hero_mobile':32,'body':16},
    'learning-paths': {'name':'學習角色與課程','sections':['白底導覽與學習角色主視覺','學習資料','課程分類','雙欄學習方式與技能介紹','角色切換','社群故事','非營利介紹','常見問題與頁尾'],'hero':'白底與紫藍操作，左側大標及說明、右側學生家長教師直排選擇卡；手機堆疊。','media_ratio':'4 / 3','image_count':4,'max':1200,'gap':24,'padding':24,'radius':8,'button_radius':8,'hero_desktop':48,'hero_mobile':32,'body':16},
    'creative-suite': {'name':'創意工具展示頁','sections':['深色全版影像主視覺','五項產品分類切換','產品圖片卡','最新資訊','創作者故事','工具清單與多欄頁尾'],'hero':'滿版影像上疊加白色左對齊大標與操作，下方呈現五個橫向分類；手機保留可捲動分類。','media_ratio':'16 / 9','image_count':7,'max':1280,'gap':24,'padding':24,'radius':16,'button_radius':999,'hero_desktop':56,'hero_mobile':36,'body':16},
    'news-grid': {'name':'新聞雜誌編輯網格','sections':['上方留白與置中刊名導覽','主次分明的三欄頭條','週末精選','音訊節目','更多新聞與編輯精選','新聞分類及頁尾'],'hero':'白底黑字、置中刊名與橫向導覽；首屏中間大圖、兩側新聞欄，手機依閱讀順序排列。','media_ratio':'16 / 9','image_count':10,'max':1200,'gap':24,'padding':20,'radius':2,'button_radius':2,'hero_desktop':48,'hero_mobile':32,'body':16},
    'live-directory': {'name':'直播內容瀏覽','sections':['深色頂部導覽與搜尋','推薦頻道側欄','大型直播畫面與資訊','直播卡片','分類封面','推薦頻道清單'],'hero':'深色介面搭配紫色重點；左側頻道欄，中央大幅直播畫面和資訊，後續為直播及分類卡片。','media_ratio':'16 / 9','image_count':8,'max':1440,'gap':16,'padding':16,'radius':8,'button_radius':6,'hero_desktop':40,'hero_mobile':30,'body':16},
    'meeting-suite': {'name':'協作工具介紹','sections':['深藍漸層導覽與置中主視覺','橫向產品圖片卡','My Notes 介紹','報告卡片','合作方式分頁','客戶案例','最新消息與頁尾'],'hero':'深藍至紫藍漸層、置中大標及圓角按鈕；下方依序是橫向產品卡、圖文區與合作方式分頁。','media_ratio':'16 / 10','image_count':6,'max':1200,'gap':24,'padding':24,'radius':16,'button_radius':999,'hero_desktop':56,'hero_mobile':36,'body':16},
    'travel-search': {'name':'旅遊探索與搜尋','sections':['深藍導覽與住宿搜尋列','四項服務優點','雙列新潮目的地','住宿和類型卡片','探索臺灣','住宿及週末優惠','旅遊規劃','目的地分類與頁尾'],'hero':'深藍主視覺搭配黃色外框搜尋列；後續包含服務優點、圖片目的地、住宿卡與旅遊分類。','media_ratio':'4 / 3','image_count':9,'max':1200,'gap':24,'padding':20,'radius':8,'button_radius':6,'hero_desktop':48,'hero_mobile':32,'body':16},
    'knowledge-portal': {
        'name': '多語言知識入口', 'sections': ['置中名稱與副標', '中央地球圖與兩側語言入口', '搜尋與語言選擇', '展開更多語言', '基金會、應用程式與相關專案', '授權與頁尾'],
        'hero': '以置中地球圖及兩側語言清單為焦點，搜尋框不超過 450px；依系統偏好提供深淺色版本。',
        'media_ratio': '1 / 1', 'image_count': 1, 'max': 960, 'gap': 24, 'padding': 20, 'radius': 4, 'button_radius': 4,
        'hero_desktop': 40, 'hero_mobile': 32, 'body': 16,
    },
    'marketplace': {
        'name': '商品探索型錄', 'sections': ['深色導覽與搜尋', '分類導覽', '橫向活動主視覺', '兩排商品分類卡片', '個人化推薦提示', '多欄頁尾'],
        'hero': '深色導覽與搜尋列下接四張直式活動圖；商品分類以四欄白色卡片及四宮格縮圖呈現。',
        'media_ratio': '4 / 3', 'image_count': 12, 'max': 1440, 'gap': 16, 'padding': 16, 'radius': 8, 'button_radius': 6,
        'hero_desktop': 40, 'hero_mobile': 30, 'body': 16,
    },
    'community': {
        'name': '社群聊天介紹頁', 'sections': ['深藍紫漸層導覽與左右主視覺', '群組聊天', '直播分享', '隨時加入', '社群揪團', '共同活動', '跨裝置及頁尾'],
        'hero': '深藍紫漸層搭配左側文字及右側裝置圖；下方以大型圓角交錯圖文區介紹六個功能。',
        'media_ratio': '16 / 10', 'image_count': 7, 'max': 1200, 'gap': 32, 'padding': 24, 'radius': 18, 'button_radius': 999,
        'hero_desktop': 56, 'hero_mobile': 36, 'body': 17,
    },
    'learning': {
        'name': '學習入口與練習', 'sections': ['白底導覽與左右主視覺', '橫向課程主題', '免費學習、教學、動力與個人化介紹', '行動應用程式', 'Super Duolingo', '英語測驗與頁尾'],
        'hero': '白底與鮮綠色按鈕搭配左側插畫、右側標題與操作；後續以交錯插圖和綠色標題介紹學習。',
        'media_ratio': '1 / 1', 'image_count': 7, 'max': 1100, 'gap': 24, 'padding': 24, 'radius': 18, 'button_radius': 14,
        'hero_desktop': 40, 'hero_mobile': 30, 'body': 17,
    },
    'home-inspiration': {
        'name': '居家靈感與商品', 'sections': ['公告與服務導覽', '搜尋和產品分類', '不等寬活動圖片磚', '系列推薦', '服務和安全資訊', '會員優惠', '佈置靈感與頁尾'],
        'hero': '白底、藍黃識別與大型搜尋框；主視覺採左大右小活動圖片磚，下方依序呈現系列與服務。',
        'media_ratio': '4 / 3', 'image_count': 10, 'max': 1280, 'gap': 20, 'padding': 20, 'radius': 8, 'button_radius': 999,
        'hero_desktop': 44, 'hero_mobile': 32, 'body': 16,
    },
    'search-home': {
        'name': '置中搜尋首頁', 'sections': ['精簡導覽', '置中品牌與搜尋欄', '搜尋按鈕', '地區與頁尾'],
        'hero': '以置中的品牌文字及搜尋框為焦點；桌面搜尋框最多 688px，窄版保留兩側空間，首頁不另加長頁內容。',
        'media_ratio': '16 / 9', 'image_count': 0, 'max': 680, 'gap': 24, 'padding': 20, 'radius': 24, 'button_radius': 8,
        'hero_desktop': 56, 'hero_mobile': 40, 'body': 16,
    },
    'video-results': {
        'name': '影音搜尋結果清單', 'sections': ['導覽與搜尋', '側邊導覽', '可水平捲動的分類', '影音結果清單', 'Shorts 短片區'],
        'hero': '以 design 搜尋結果頁為例：桌面結果以 16:9 縮圖與文字左右並列，窄版改上下排列；結果會隨時間改變。',
        'media_ratio': '16 / 9', 'image_count': 6, 'max': 1280, 'gap': 16, 'padding': 16, 'radius': 12, 'button_radius': 999,
        'hero_desktop': 32, 'hero_mobile': 26, 'body': 16,
    },
    'streaming': {
        'name': '串流內容介紹頁', 'sections': ['背景主視覺與導覽', '置中主標與主要操作', '十部熱門內容排行', '四項服務特色', '六項可展開的常見問題', '頁尾'],
        'hero': '深色大幅主視覺搭配置中標題與紅色重點操作，未提供授權圖片時以抽象色塊及文字替代。',
        'media_ratio': '2 / 3', 'image_count': 6, 'max': 1200, 'gap': 24, 'padding': 24, 'radius': 8, 'button_radius': 4,
        'hero_desktop': 56, 'hero_mobile': 36, 'body': 17,
    },
    'collaboration': {
        'name': '開發協作介紹頁', 'sections': ['精簡導覽', '置中標題與主要操作', '可切換的操作示意', '社群動態', '平台雙欄卡', '五項功能', '企業服務與客戶故事', '精選儲存庫與頁尾'],
        'hero': '白底、置中大標與綠色按鈕建立重點；程式碼面板可切換步驟，後續呈現平台、功能、企業與社群。',
        'media_ratio': '16 / 10', 'image_count': 0, 'max': 1200, 'gap': 24, 'padding': 24, 'radius': 8, 'button_radius': 6,
        'hero_desktop': 48, 'hero_mobile': 32, 'body': 16,
    },
    'product-catalog': {
        'name': '科技產品型錄', 'sections': ['精簡導覽', 'Microsoft 365 與 Surface 主視覺輪播', '三項快速連結', '四張個人產品卡', 'Microsoft Edge 橫幅', '四張商務產品卡', '社群連結與頁尾'],
        'hero': '桌面首張主視覺左圖右文，窄版改為上下排列；產品卡使用四欄，依序呈現 Xbox、Edge 及商務產品。',
        'media_ratio': '4 / 3', 'image_count': 4, 'max': 1280, 'gap': 24, 'padding': 24, 'radius': 4, 'button_radius': 4,
        'hero_desktop': 48, 'hero_mobile': 32, 'body': 16,
    },
    'campaign': {
        'name': '交錯雙欄活動頁', 'sections': ['導覽與主要入口', '一行活動公告', '四組照片與文案交錯區塊', '補充說明', '五組頁尾連結'],
        'hero': '首組以左側照片、右側置中文字呈現；下一組反向。每組各半，不另加右側儀表板。',
        'media_ratio': '12 / 7', 'image_count': 4, 'max': 1440, 'gap': 32, 'padding': 56, 'radius': 0, 'button_radius': 999,
        'hero_desktop': 24, 'hero_mobile': 24, 'body': 19,
    },
    'payments': {
        'name': '連續標題與解決方案格線', 'sections': ['導覽與操作', '連續大標及補充文字', '解決方案拼貼格線', '企業及新創案例', '開發者範例', '最新消息與頁尾'],
        'hero': '標題與接續說明維持同一閱讀尺度；右上斜向波形只作裝飾，缺素材可用指定 CSS 漸層。不要在主視覺另加支付儀表板。',
        'media_ratio': '16 / 10', 'image_count': 3, 'max': 1232, 'gap': 32, 'padding': 32, 'radius': 12, 'button_radius': 4,
        'hero_desktop': 48, 'hero_mobile': 36, 'body': 18,
    },
    'catalog': {
        'name': '分類與圖片目錄', 'sections': ['導覽與搜尋', '精簡主題介紹', '分類篩選列', '圖片內容格線', '選取內容的詳細資訊', '補充資訊與頁尾'],
        'hero': '主題與搜尋優先，將主要空間留給內容卡片；卡片包含標題、補充資訊及一項可理解操作。',
        'media_ratio': '4 / 3', 'image_count': 6, 'max': 1280, 'gap': 24, 'padding': 24, 'radius': 16, 'button_radius': 999,
        'hero_desktop': 40, 'hero_mobile': 30, 'body': 16,
    },
    'developer': {
        'name': '技術產品與示範面板', 'sections': ['導覽', '主標題、說明與主要操作', '產品或程式碼示範', '三組能力說明', '實際使用情境', '開始使用與頁尾'],
        'hero': '主標、說明與操作形成一組；產品示範另放在有邊界的面板。內容含程式碼時以文字及複製操作實作，不把整個面板做成圖片。',
        'media_ratio': '16 / 10', 'image_count': 2, 'max': 1200, 'gap': 32, 'padding': 24, 'radius': 12, 'button_radius': 8,
        'hero_desktop': 56, 'hero_mobile': 36, 'body': 17,
    },
    'editorial': {
        'name': '編輯式故事章節', 'sections': ['精簡導覽', '主要標題與引言', '重點故事或產品圖', '交錯的說明章節', '相關內容', '主要後續操作與頁尾'],
        'hero': '先讓標題建立方向，再放入引言與主要圖像；內文維持可閱讀欄寬，章節使用尺寸及留白區分。',
        'media_ratio': '3 / 2', 'image_count': 3, 'max': 1240, 'gap': 32, 'padding': 32, 'radius': 8, 'button_radius': 8,
        'hero_desktop': 56, 'hero_mobile': 36, 'body': 18,
    },
    'showcase': {
        'name': '影像主導的產品展示', 'sections': ['導覽與品牌識別', '大型產品影像與精簡標題', '產品優點章節', '規格或方案比較', '主要操作', '頁尾'],
        'hero': '大幅圖片或靜態海報為主，標題及操作放在可確保對比的背景上；不要依靠自動播放才能理解內容。',
        'media_ratio': '16 / 9', 'image_count': 3, 'max': 1440, 'gap': 32, 'padding': 32, 'radius': 4, 'button_radius': 4,
        'hero_desktop': 52, 'hero_mobile': 32, 'body': 17,
    },
    'data': {
        'name': '總覽與資料資訊', 'sections': ['導覽', '總覽標題與摘要', '重點資訊卡', '具單位的資料表', '情境說明', '資料日期與頁尾'],
        'hero': '摘要、主要指標及詳細資料依序排列；數字採等寬數字、單位相鄰，正負變化同時使用文字或符號。',
        'media_ratio': '16 / 10', 'image_count': 1, 'max': 1200, 'gap': 24, 'padding': 24, 'radius': 12, 'button_radius': 8,
        'hero_desktop': 44, 'hero_mobile': 30, 'body': 16,
    },
    'grid': {
        'name': '結構化資訊格線', 'sections': ['導覽', '主標題與操作', '特色資訊格線', '詳細產品或案例', '比較或支援資訊', '頁尾'],
        'hero': '主要內容遵循同一容器及格線，卡片以分隔線區隔；避免同時使用大量陰影、圓角與裝飾背景。',
        'media_ratio': '4 / 3', 'image_count': 3, 'max': 1280, 'gap': 24, 'padding': 24, 'radius': 0, 'button_radius': 0,
        'hero_desktop': 48, 'hero_mobile': 32, 'body': 16,
    },
    'retro': {
        'name': '可用的復古型錄', 'sections': ['框架與品牌標題', '精簡文字導覽', '彩色主題區', '分組產品或遊戲清單', '詳細內容', '頁尾'],
        'hero': '使用平面色、清楚邊框及字體比例建立年代感，保留現代語意、流動欄寬與可見焦點。',
        'media_ratio': '4 / 3', 'image_count': 4, 'max': 1100, 'gap': 16, 'padding': 20, 'radius': 0, 'button_radius': 0,
        'hero_desktop': 44, 'hero_mobile': 30, 'body': 17,
    },
    'minimal': {
        'name': '精簡工具介紹', 'sections': ['品牌及精簡導覽', '主標、說明與一項主要操作', '能力或模型清單', '使用方式', '頁尾'],
        'hero': '用文字、比例與留白建立層級。先呈現可理解的主題與主要操作，不增加無關的儀表板或大型裝飾。',
        'media_ratio': '16 / 10', 'image_count': 0, 'max': 1040, 'gap': 24, 'padding': 24, 'radius': 8, 'button_radius': 8,
        'hero_desktop': 44, 'hero_mobile': 30, 'body': 18,
    },
    'product': {
        'name': '產品介紹與操作範例', 'sections': ['導覽', '主標與主要操作', '核心產品示範', '三組重點功能', '使用情境與支援', '開始使用與頁尾'],
        'hero': '主題、說明與主要操作形成明確閱讀順序；產品畫面以可讀的示範內容支撐，功能卡不要只放圖示及口號。',
        'media_ratio': '16 / 10', 'image_count': 3, 'max': 1240, 'gap': 24, 'padding': 24, 'radius': 12, 'button_radius': 8,
        'hero_desktop': 48, 'hero_mobile': 32, 'body': 17,
    },
}


def sha(value):
    return hashlib.sha256(value if isinstance(value, bytes) else value.encode()).hexdigest()


def rgb(value):
    return [int(value[i:i+2], 16) for i in (1, 3, 5)]


def mix(a, b, amount):
    return '#' + ''.join(f'{round(x*(1-amount)+y*amount):02x}' for x, y in zip(rgb(a), rgb(b)))


def luminance(value):
    v = [x / 255 for x in rgb(value)]
    return sum(w * (x / 12.92 if x <= .04045 else ((x+.055)/1.055)**2.4) for w, x in zip((.2126, .7152, .0722), v))


def contrast(a, b):
    x, y = sorted([luminance(a), luminance(b)])
    return (y+.05)/(x+.05)


def contrasting(value):
    return '#ffffff' if contrast(value, '#ffffff') >= contrast(value, '#000000') else '#000000'


class CSSSources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_style = False
        self.styles = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.in_style = self.in_style or tag == 'style'
        if attrs.get('style'):
            self.styles.append(attrs['style'])
        if tag == 'link' and attrs.get('rel') == 'stylesheet':
            self.links.append(attrs.get('href', ''))

    def handle_endtag(self, tag):
        if tag == 'style':
            self.in_style = False

    def handle_data(self, data):
        if self.in_style:
            self.styles.append(data)


def css_sources(work, brand):
    file = work / (brand + '.html')
    parser = CSSSources()
    parser.feed(file.read_text())
    sources = [(file.name, '\n'.join(parser.styles), sha(file.read_bytes()))]
    queue = [(Path('.'), relative) for relative in parser.links]
    seen = set()
    while queue:
        parent, relative = queue.pop(0)
        if re.match(r'^(?:[a-z]+:|/|#)', relative, re.I):
            continue
        path = (work / parent / relative.split('?', 1)[0]).resolve()
        try:
            route = path.relative_to(work.resolve()).as_posix()
        except ValueError:
            raise ValueError('CSS dependency leaves source directory')
        if route in seen or not path.is_file() or path.suffix.lower() != '.css':
            continue
        seen.add(route)
        text = path.read_text()
        sources.append((route, text, sha(path.read_bytes())))
        queue += [(path.parent.relative_to(work.resolve()), match) for match in re.findall(r'@import\s+(?:url\()?\s*["\']([^"\']+)', text)]
    return sources


def color_evidence(value, sources):
    target = value.lower()
    for filename, text, digest in sources:
        text = re.sub(r'/\*[\s\S]*?\*/', '', text)
        for match in re.finditer(r'#[\da-fA-F]{3,8}(?![\da-fA-F])', text):
            found = match[0].lower()
            if len(found) == 4:
                found = '#' + ''.join(c*2 for c in found[1:])
            if found != target:
                continue
            return dict(kind='source_declaration', label='來源樣式出現此數值；角色由本規格指定，非瀏覽器實測保證',
                        path=filename, sha256=digest, excerpt=text[max(0, match.start()-65):match.end()+35].replace('\n', ' '))
    return dict(kind='implementation_recommendation', label='本版本實作建議值，非官網量測值')


def build_profile(root, entry, lock, direction):
    accent, canvas, ink, surface, composition, visual = direction
    layout = dict(COMPOSITIONS[composition])
    if contrast(canvas, ink) < 4.5:
        ink = contrasting(canvas)
    muted = mix(ink, canvas, .24)
    if contrast(canvas, muted) < 4.5:
        muted = ink
    border = mix(ink, canvas, .82)
    colors = dict(accent=accent, **{'on-accent': contrasting(accent)}, canvas=canvas,
                  ink=ink, muted=muted, surface=surface, border=border, focus=ink)
    # On light surfaces such as newsletter or product cards, pair text with that surface.
    colors['on-surface'] = ink if contrast(surface, ink) >= 4.5 else contrasting(surface)
    sources = css_sources(root / '.stitch-work/current-official', lock['file'])
    fields, behavior = json.loads((root / 'data/implementation/component-contracts.json').read_text())[entry['slug']]
    profile = dict(schema_version=1, locale='zh-TW', version=VERSION, slug=entry['slug'], name=entry['name'],
                   reference_date=lock['date'], reference_url=lock['reference_url'], reference_preview_sha256=lock['preview_sha256'],
                   usage='品牌設計語言的獨立實作規格；採明示建議值，不承諾與來源預覽像素一致',
                   visual=visual, composition=composition, layout=layout, colors=colors,
                   color_provenance={key: color_evidence(value, sources) for key, value in colors.items()},
                   typography=dict(family=FONT, heading_desktop_px=layout['hero_desktop'], heading_mobile_px=layout['hero_mobile'],
                                   section_px=24, body_px=layout['body'], small_px=14, body_line_height=1.65,
                                   heading_line_height=1.25, display_weight=300 if composition=='payments' else 600),
                   spacing_px=[4, 8, 12, 16, 24, 32, 48, 64, 96],
                   responsive=dict(narrow_max_px=767, tablet_max_px=1023, side_mobile_px=20, side_desktop_px=32,
                                   image_first_on_narrow=True, menu_width_percent=80, test_widths_px=[390,768,1440]),
                   components=dict(button_min_height_px=44, button_padding='10px 20px', button_radius_px=layout['button_radius'],
                                   input_min_height_px=44, input_padding='10px 12px', card_radius_px=layout['radius'],
                                   card_padding_px=layout['padding'], focus_ring='3px solid var(--focus)', focus_offset_px=3,
                                   transition_ms=160),
                   recommendation_scope='字型替代、字級、間距、斷點、元件尺寸與狀態為本版本統一實作建議；只有附來源宣告的色彩可溯源至指定檔案。',
                   required_user_inputs=['產品名稱與文案', '實際功能與資料來源', '有權使用的自有圖片，或選擇不用圖片', '真實聯絡與門市資料（適用時）'],
                   recipe=entry['brief'], component_task=entry['component'],
                   component_contract=dict(fields=fields.split('、'), behavior=behavior))
    if entry['slug'] == 'linear.app':
        profile['component_contract']['layout'] = dict(sidebar_px=220,detail_px=320,row_min_height_px=56,narrow='側欄改為橫向篩選，詳細資訊改用 dialog，清單保留標題及狀態。')
    elif entry['slug'] == 'stripe':
        profile['component_contract']['layout'] = dict(row_min_height_px=56,columns=['交易代號','金額／幣別','狀態','時間'],narrow='將交易列堆疊成卡片，明細可在原處展開。')
    elif entry['slug'] == 'starbucks':
        profile['component_contract']['layout'] = dict(dialog_max_width_px=560,card_min_height_px=240,narrow='飲品卡片單欄，容量切換與價格放在同一對話框內。')
    return profile


def asset_manifest(profile):
    count = profile['layout']['image_count']
    images = [dict(id=f'photo-{i+1:02d}', role='主要圖像' if i==0 else f'內容圖像 {i+1}',
                   suggested_local_path=f'assets/photo-{i+1:02d}.webp', aspect_ratio=profile['layout']['media_ratio'],
                   fit='cover', minimum_width_px=1440 if i==0 else 800,
                   supplied=False, required_to_run=False, source='使用者自有且有權使用的檔案；此包未提供品牌原圖',
                   fallback='未提供檔案時不要建立 img；使用文字特色卡與 solid 色塊保留資訊，使用者介面可提供另行加入圖片的入口。',
                   alt_requirement='依自有圖片內容填寫，純裝飾可使用空字串。') for i in range(count)]
    return dict(schema_version=1, locale='zh-TW', version=VERSION, brand=profile['slug'],
                can_run_without_external_assets=True, images=images,
                logo=dict(supplied=False,required_to_run=False,fallback='使用自己的產品名稱作文字識別，不擷取參考品牌商標。'),
                fonts=dict(files_supplied=False,required_to_run=False,stack=profile['typography']['family'],
                           fallback='直接使用系統字型；不自動下載專有字型，不以字寬完全相同為前提。'),
                motion=dict(required_to_run=False,fallback='省略影片與 WebGL，以可閱讀的靜態內容取代；不自動呼叫外部媒體。'),
                services=dict(included=False,fallback='前端範例只能使用明確的示範資料；真實登入、訂單與付款由使用者另行接上。'))


def starter_css(profile):
    colors = '\n'.join(f'  --{k}: {v};' for k, v in profile['colors'].items())
    l, t, c, r = (profile[k] for k in ['layout','typography','components','responsive'])
    extra = ''
    if profile['composition'] == 'payments':
        extra = '.payment-hero{position:relative;isolation:isolate;overflow:hidden;padding-block:96px}.payment-hero::before{content:"";position:absolute;z-index:-1;right:-10%;top:0;width:65%;height:100%;background:linear-gradient(135deg,var(--surface),var(--accent));opacity:.18;clip-path:polygon(28% 0,100% 0,100% 100%,0 70%)}.payment-hero .hero-title{max-width:24ch}.payment-hero p{max-width:58ch}.transaction-row{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:16px;min-height:56px;align-items:center;padding:16px;border-bottom:1px solid var(--border)}@media(max-width:767px){.payment-hero{padding-block:48px}.transaction-row{grid-template-columns:1fr 1fr}}\n'
    elif profile['slug'] == 'linear.app':
        extra = '.issue-workspace{display:grid;grid-template-columns:220px minmax(0,1fr) 320px;border:1px solid var(--border)}.issue-sidebar,.issue-detail{padding:24px;background:var(--surface);color:var(--on-surface)}.issue-row{display:grid;grid-template-columns:90px minmax(0,1fr) 100px;gap:12px;min-height:56px;padding:16px;border:0;border-bottom:1px solid var(--border);background:var(--canvas);color:var(--ink);text-align:left;width:100%}.issue-row[aria-pressed=true]{background:var(--surface)}@media(max-width:1023px){.issue-workspace{grid-template-columns:180px minmax(0,1fr)}.issue-detail{grid-column:1/-1}}@media(max-width:767px){.issue-workspace{grid-template-columns:minmax(0,1fr)}.issue-row{grid-template-columns:64px minmax(0,1fr)}.issue-row>span:last-child{grid-column:2}.issue-sidebar{padding:16px}}\n'
    elif profile['slug'] == 'canva':
        extra = '.feature-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:16px}.feature-grid>.feature:nth-child(1),.feature-grid>.feature:nth-child(4){grid-column:span 2}.feature{min-height:406px;border-radius:24px;overflow:hidden}.tool-tabs{display:flex;overflow-x:auto;gap:4px;border-radius:999px}.template-track{display:grid;grid-auto-flow:column;grid-template-rows:repeat(2,304px);grid-auto-columns:242px;gap:24px;overflow-x:auto}@media(max-width:767px){.feature-grid{grid-template-columns:minmax(0,1fr)}.feature-grid>.feature:nth-child(n){grid-column:auto}.feature{min-height:360px}.template-track{grid-template-rows:repeat(2,240px);grid-auto-columns:190px;gap:12px}}\n'
    elif profile['slug'] == 'etsy':
        extra = '.market-hero{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,1fr);gap:24px}.market-hero-main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))}@media(max-width:767px){.market-hero{grid-template-columns:minmax(0,1fr)}}\n'
    return f'''/* {profile['name']}｜{VERSION} 實作建議；與 TOKENS.json 相同版本。 */
:root {{
{colors}
  --font-body: {t['family']};
  --content-max: {l['max']}px;
  --section-gap: {l['gap']}px;
  --card-padding: {c['card_padding_px']}px;
  --card-radius: {c['card_radius_px']}px;
  --button-radius: {c['button_radius_px']}px;
  --heading-size: {t['heading_desktop_px']}px;
  --heading-size-narrow: {t['heading_mobile_px']}px;
}}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--canvas); color: var(--ink); font: {t['body_px']}px/{t['body_line_height']} var(--font-body); }}
button,input,select,textarea {{ font: inherit; }}
a {{ color: inherit; text-underline-offset: 3px; }}
[hidden] {{ display: none !important; }}
.container {{ width: min(var(--content-max),calc(100% - {r['side_desktop_px']*2}px)); margin-inline: auto; }}
.section {{ margin-block: var(--section-gap); }}
.hero-title {{ font-size: var(--heading-size); line-height: {t['heading_line_height']}; font-weight: {t['display_weight']}; margin: 0 0 24px; overflow-wrap: anywhere; }}
.section-title {{ font-size: {t['section_px']}px; line-height: 1.4; margin: 0 0 20px; }}
.muted {{ color: var(--muted); }}
.split {{ display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); }}
.split.reverse .media {{ order: 2; }}
.split-copy {{ padding: var(--card-padding); min-width: 0; }}
.media {{ width: 100%; min-width: 0; aspect-ratio: {l['media_ratio']}; object-fit: cover; }}
.text-feature {{ padding: var(--card-padding); background: var(--surface); color: var(--on-surface); }}
.card-grid {{ display: grid; grid-template-columns: repeat(3,minmax(0,1fr)); gap: {l['gap']}px; }}
.card {{ min-width: 0; padding: var(--card-padding); border: 1px solid var(--border); border-radius: var(--card-radius); background: var(--surface); color: var(--on-surface); }}
.button {{ display: inline-flex; align-items:center; justify-content:center; min-height:{c['button_min_height_px']}px; padding:{c['button_padding']}; border:1px solid currentColor; border-radius:var(--button-radius); background:transparent; color:inherit; font-weight:600; text-decoration:none; cursor:pointer; }}
.button-primary {{ background:var(--accent); color:var(--on-accent); border-color:var(--accent); }}
.button[aria-pressed=true] {{ background:var(--ink); color:var(--canvas); }}
.button:disabled {{ cursor:not-allowed; opacity:.55; }}
input,select,textarea {{ max-width:100%; min-height:{c['input_min_height_px']}px; padding:{c['input_padding']}; border:1px solid var(--border); background:var(--canvas); color:var(--ink); }}
:where(button,a,input,select,textarea,summary):focus-visible {{ outline:{c['focus_ring']}; outline-offset:{c['focus_offset_px']}px; }}
pre,.table-scroll {{ max-width:100%; overflow:auto; }}
.numeric {{ font-variant-numeric:tabular-nums; }}
dialog {{ max-width:min(560px,calc(100% - 32px)); border:1px solid var(--border); border-radius:var(--card-radius); padding:24px; background:var(--canvas); color:var(--ink); }}
dialog::backdrop {{ background:rgb(0 0 0 / .55); }}
@media(min-width:{r['narrow_max_px']+1}px) and (max-width:{r['tablet_max_px']}px) {{ .card-grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
@media(max-width:{r['narrow_max_px']}px) {{
  .container {{ width:calc(100% - {r['side_mobile_px']*2}px); }}
  .hero-title {{ font-size:var(--heading-size-narrow); }}
  .split,.card-grid {{ grid-template-columns:minmax(0,1fr); }}
  .split.reverse .media {{ order:0; }}
  .split-copy,.card,.text-feature {{ padding:24px; }}
}}
@media(prefers-reduced-motion:reduce) {{ html {{ scroll-behavior:auto; }} *,*::before,*::after {{ animation:none!important; transition:none!important; }} }}
{extra}
'''


def tables(profile):
    colors = '\n'.join(f'| `{key}` | `{value}` | {PROPERTIES.get(key,"卡片內文字")} | {profile["color_provenance"][key]["label"]} |' for key,value in profile['colors'].items())
    return '| 角色 | 色碼 | 用途 | 值的依據 |\n| --- | --- | --- | --- |\n' + colors


def assets_text(profile, manifest):
    rows = '\n'.join(f'| `{a["id"]}` | `{a["suggested_local_path"]}` | {a["aspect_ratio"]} | 寬至少 {a["minimum_width_px"]}px | 未附，非執行必要 |' for a in manifest['images'])
    return f'''# {profile['name']} 素材需求與替代方式

繁體中文（台灣用語，zh-TW）。版本：{VERSION}。

此包沒有附品牌照片、商標或專有字型，但可在完全不連外的狀態下完成文字版前端原型。選擇有圖片的版本時，請另提供自己的合法素材；不要把下表建議路徑誤認為已存在的檔案。

| 素材 | 建議本機路徑 | 比例 | 建議尺寸 | 提供狀態 |
| --- | --- | --- | --- | --- |
{rows or '| 無必要圖片 | — | — | — | 此方向可完全使用文字及結構 |'}

照片不存在時，不建立會破圖的 img，也不自行抓取官網素材。改用 `.text-feature` 的純色色塊、文字特色卡、條列內容或可閱讀的產品示範；這是無圖版設計，不宣稱與照片版完全一致。若需要保留未來照片位置，在開發模式顯示待提供即可，成品使用有意義的文字內容。

使用自己的產品名稱作文字識別；不要求參考品牌商標。字型直接採 `{profile['typography']['family']}`。所有系統字型皆不可用時以瀏覽器 sans-serif 呈現；保留相同字級與行高，允許換行差異。

影片、3D、WebGL 及即時資料不是執行必要。無影片時以靜態文字與卡片說明，無後端時明確標示示範資料。不要生成假登入、假付款或假訂單成功。

機器可讀版本為同資料夾 ASSETS.json；全部素材的 supplied=false，required_to_run=false。DESIGN.md 已含本節必要規則，因此單獨使用主要規格也不會依賴這份補充檔。
'''


def documents(profile, entry, lock, review):
    t,c,l,r = (profile[k] for k in ['typography','components','layout','responsive'])
    manifest = asset_manifest(profile)
    sections = '\n'.join(f'{i+1}. {v}。' for i,v in enumerate(l['sections']))
    css = starter_css(profile)
    color_table = tables(profile)
    columns = ('首頁主題磚使用 `grid-template-columns: minmax(0,2fr) minmax(0,1fr)`，左側主題磚內的文案與圖片可各占一半；窄版將兩個主題磚堆疊。' if profile['slug'] == 'etsy' else '工具卡片使用三欄等寬格線，第一與第四張跨兩欄，第二與第三張各占一欄；產品介紹採兩欄，窄版堆疊。' if profile['slug'] == 'canva' else '一般雙欄可使用 `repeat(2,minmax(0,1fr))`，不要讓長內容的最小寬度撐開格線。')
    contract = {
        'schema_version':1, 'brand':profile['slug'], 'version':VERSION, 'locale':'zh-TW',
        'colors':profile['colors'], 'typography':t, 'layout':{k:l[k] for k in ['max','gap','padding','radius','media_ratio']},
        'components':c, 'responsive':r, 'spacing_px':profile['spacing_px'],
        'color_provenance':profile['color_provenance'], 'recommendation_scope':profile['recommendation_scope'],
        'component_contract':profile['component_contract'],
    }
    analysis = f'''# {profile['name']} 風格實作規格

繁體中文（台灣用語，zh-TW）。實作版本：{VERSION}。參考畫面日期：{lock['date']}。

## 使用範圍

這是一份可獨立使用的前端實作規格，用來把 {profile['name']} 的設計方向套用到自己的產品。所有必要規則與可直接採用的 CSS 都在本檔，不需要另找舊版延伸規格。它不是原官網完整原始碼，也不保證與預覽像素相同。圖片、文案、資料與後端由使用者決定；未提供圖片時有明確無圖做法。

參考來源：{lock['reference_url']}。參考預覽摘要：`{lock['preview_sha256']}`。版本中的來源宣告只能證明指定樣式資料含此數值，不表示已驗證全部可見元素或瀏覽器尺寸。

## 設計方向與版面藍圖

{profile['visual']}

採用「{l['name']}」作為本版本的新專案實作方向。{l['hero']}

{sections}

以上是可執行的版面藍圖，不把每個區段當成目前官網的精確量測。功能依自己的需求調整；可從下列任務開始：{entry['brief']}優先元件為{entry['component']}。

## 色彩角色

{color_table}

主要背景與正文對比為 {contrast(profile['colors']['canvas'],profile['colors']['ink']):.2f}:1；主要按鈕與文字為 {contrast(profile['colors']['accent'],profile['colors']['on-accent']):.2f}:1。這是兩組純色的數值計算，不代表整頁無障礙驗收。次要連結保留底線；不要因品牌色偏亮而用低對比文字。

## 字型與文字層級

字型：`{t['family']}`。不要求下載專有字型。下列字級與行高為本版本實作建議，不冒充官網實測。

| 用途 | 桌面 | 窄版 | 字重 | 行高 |
| --- | --- | --- | --- | --- |
| 主標題 | {t['heading_desktop_px']}px | {t['heading_mobile_px']}px | {t['display_weight']} | {t['heading_line_height']} |
| 區段標題 | {t['section_px']}px | {t['section_px']}px | 600 | 1.4 |
| 內文 | {t['body_px']}px | {t['body_px']}px | 400 | {t['body_line_height']} |
| 補充資訊 | {t['small_px']}px | {t['small_px']}px | 400 | 1.6 |
| 按鈕文字 | 16px | 16px | 600 | 1.4 |

中文不套英文全大寫字距；長標題可換行，型號、網址、程式碼可在自己的容器折行或捲動。金額及規格採等寬數字，幣別及時區明確標示，不擅自換算。

## 容器、間距與響應式

- 內容最大寬度 {l['max']}px；桌面兩側至少 {r['side_desktop_px']}px，窄版兩側 {r['side_mobile_px']}px。
- 以 {', '.join(str(v) for v in profile['spacing_px'])}px 作間距級距，區段預設間隔 {l['gap']}px。
- {columns} 交錯區段用明確的 `.reverse` 類別，不用可能受到其他兄弟區段影響的序號選取器。
- {r['narrow_max_px']}px 以下採單欄、圖片或文字特色先、說明後；768–1023px 可採兩欄卡片；1024px 起卡片最多三欄。這些是本規格明確的建議斷點，不是官網斷點保證。
- 手機導覽收成 {r['menu_width_percent']}% 寬的選單，按鈕以 aria-expanded 表示；支援鍵盤、Escape 與連結選取後關閉。桌面恢復時清除窄版展開狀態。
- 圖片比例 `{l['media_ratio']}`，使用 object-fit: cover；無圖片時採下節的文字版，不建立失敗的圖片請求。
- 在 390、768、1440px 檢查文件水平溢位、長中文、內容增減與焦點遮擋。

## 元件與互動合約

### {entry['component']}

必要欄位：{'、'.join(profile['component_contract']['fields'])}。欄位值來自使用者提供資料；未提供時清楚標示，不捏造真實服務內容。

{profile['component_contract']['behavior']}

{('元件專屬配置建議：' + json.dumps(profile['component_contract']['layout'],ensure_ascii=False) + '。對應類別與數值已包含於下方 CSS；這是實作建議，不是來源量測。') if profile['component_contract'].get('layout') else ''}

若需要保存選取，可在單一瀏覽器使用 localStorage，並明確說明不代表帳戶同步；使用者不允許儲存時，本次狀態仍應可操作。

| 元件 | 外觀尺寸與內容 | 必要行為 |
| --- | --- | --- |
| 主要按鈕 | 至少 {c['button_min_height_px']}px 高；內距 {c['button_padding']}；圓角 {c['button_radius_px']}px；accent / on-accent | 有明確結果；載入時停用並顯示文字；失敗可重試。 |
| 次要按鈕 | 同尺寸；透明底、1px 當前文字色外框 | 不只靠色彩區分，保留可讀名稱。 |
| 內容卡片 | 內距 {c['card_padding_px']}px；圓角 {c['card_radius_px']}px；surface / on-surface | 標題、補充資訊、主要操作分層；長文字不溢出。 |
| 輸入與選擇 | 至少 {c['input_min_height_px']}px 高；內距 {c['input_padding']}；具獨立標示 | 必填、格式錯誤、停用與載入皆有文字說明。 |
| 篩選或分頁 | 沿用按鈕尺寸；已選使用 ink / canvas | 同時更新 aria-pressed 或 aria-selected、可見內容及結果數。 |
| 詳細資訊 | 使用 dialog 或語意面板；寬不超過 560px，窄版留 16px 外距 | 開啟移入焦點、Escape 關閉、關閉後回到觸發控制。 |
| 複製操作 | 一般文字按鈕 | 實際複製後才顯示成功；失敗顯示可手動複製的內容。 |

焦點外框為 `{c['focus_ring']}`，間隔 {c['focus_offset_px']}px。hover 可稍降低亮度；focus 必須可見。過場可用 {c['transition_ms']}ms，減少動態設定下停用。停用狀態不假裝完成；空內容提供下一步，錯誤提供原因與重試。

## 素材需求與零外部依賴做法

此方向建議使用 {len(manifest['images'])} 張自有圖片，比例 `{l['media_ratio']}`；第一張建議寬 1440px，其他至少 800px。圖片不在本檔或 ZIP 中；`assets/photo-01.webp` 等名稱只是建議目的地，不是已存在檔案。

如果沒有圖片，直接採 `.text-feature` 的純色色塊、清楚的特色標題、條列資訊或可閱讀的產品示範，不建立 img、不抓官網照片、不把生成圖片宣稱成原始素材。無圖版可完整執行，視覺效果會不同於攝影版。若圖片對產品理解不可或缺，交付時明列待補素材，不隱藏缺口。

品牌識別使用自己的文字名稱。字型用上述系統替代，影片、WebGL 及即時資料皆非執行必要。這份規格不依賴外部素材網址或額外檔案；ZIP 另附 ASSETS.md 與 ASSETS.json 供管理，但必要做法已完整收錄於此。

## 可直接採用的樣式起點

下方 CSS 與本版數值一致。可貼入既有樣式檔；同包 starter.css 內容相同。它提供基礎類別，仍須依自己的內容建立語意 HTML 與互動，不是完整網站。

```css
{css.rstrip()}
```

## 交付前驗收

1. 沒有附照片、字型、後端時，仍能開啟頁面，沒有失敗圖片、未知字型下載或假成功操作。
2. 390、768、1440px 的主要內容與標題可讀，文件不因格線或長網址產生水平溢位。
3. 篩選、分頁、對話框、選項、複製等實際需求逐項操作，記錄預設、已選、載入、空白與錯誤狀態。
4. 可用鍵盤到達控制項，焦點可見、選單可關閉、對話框關閉後焦點返回。
5. 說明自行新增或修改的值、替代素材及未完成服務，不把基礎前端原型說成已驗收的正式產品。

歷史畫面比對與生成細節保留於網站的開發紀錄，不是本檔實作步驟的依賴。參考來源日期沿用 {lock['date']}，本次補齊規格不代表重新驗證今日官網。
'''
    prompt = f'''# {profile['name']} AI 實作指令

繁體中文（台灣用語，zh-TW）。版本：{VERSION}。參考日期：{lock['date']}。

將此指令與同版本 DESIGN.md 一起交給 AI。DESIGN.md 已含全部必要數值、CSS 與缺素材做法；其餘 ZIP 檔為方便使用的補充，不是執行前提。

```text
請讀取隨附的 {profile['name']} 風格實作規格，沿用專案現有技術及元件，完成我的頁面。

我的產品名稱：[請填寫]
主要使用者與用途：[請填寫]
頁面功能與資料：[請填寫；只有示範資料時明確標示]
文案、圖片及後端：[請列出已提供內容；沒有圖片就採規格的無圖版]

設計方向：{profile['visual']}
功能起點：{entry['brief']}
優先元件：{entry['component']}。

依 DESIGN.md 的角色色碼、字級、容器、間距、元件及斷點實作，不以泛用卡片換色代替版面結構。不需要讀取其他延伸規格或自行瀏覽官網補齊依賴。來源宣告與實作建議要分清楚；若需求需要新值，列出理由，不稱為官網實測。

未提供照片時使用規格的文字特色卡或產品示範，不建立破圖、不自動抓取品牌素材。使用自己的產品名稱與已提供內容，字型採系統替代；不要求未附上的專有字型。影片與動態有可閱讀的靜態替代。

介面、提示、錯誤、圖片替代文字與交付說明使用繁體中文（台灣用語）。保留必要品牌名稱、檔名、網址、API 識別字與程式碼，HTML 語言使用 zh-Hant-TW。價格、數量與時間標示原本單位、幣別及時區，不擅自捏造來源資料。

所有可見操作都要有可理解結果。依功能支援預設、已選、停用、載入、空白與錯誤，提供可見鍵盤焦點及至少 44px 的主要觸控區域。選單支援關閉及 Escape；對話框管理焦點；複製成功需實際寫入剪貼簿。未接後端不顯示真實訂單、付款或登入成功。

在 390、768、1440px 實際檢查長中文、格線、換行與水平溢位；操作主要功能、鍵盤及失敗狀態。先交付可操作的最小完整頁面，再根據發現的問題調整。

交付實作檔案、操作方式、已執行的檢查及未完成項目，列出自行新增的值與缺少的內容。不要在未實際檢查時宣稱驗收通過。
```
'''
    return dict(analysis=analysis, prompts=prompt, review=review), dict(profile=profile, assets=manifest,
                files={'TOKENS.json':json.dumps(contract,ensure_ascii=False,indent=2)+'\n',
                       'ASSETS.json':json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',
                       'ASSETS.md':assets_text(profile,manifest), 'starter.css':css})
