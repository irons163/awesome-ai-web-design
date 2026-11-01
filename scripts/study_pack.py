"""Download the same dated analysis and prompt shown in the public tabs."""
import json
import re
import hashlib
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

USAGE = json.loads((Path(__file__).resolve().parents[1] / 'data/usage.json').read_text())

COMMON_USAGE = '## 把這段貼給 AI\n\n請先完成上面的檔案放置，再將下方指令貼到能讀取專案檔案的 AI 開發工具，並填入自己的需求。\n\n```text\n' + USAGE['start_prompt'] + '\n```\n\n## 檔案怎麼分工\n\n- `DESIGN.md`：畫面與互動規格，包含色彩、字級、間距、元件、響應式規則與必要 CSS；不依賴未附上的延伸規格。\n- `PROMPTS.md`：與這份設計搭配的 AI 實作指令。上方的開工指令會請 AI 一起讀取這兩份文件。\n- `starter.css`、`TOKENS.json`：同版本的樣式與設計數值，依專案需要使用。\n- `ASSETS.md`、`ASSETS.json`：素材需求與缺少圖片時的無圖版做法。建議路徑不代表檔案已存在。\n- `README.md`、`SOURCES.json`：使用說明與來源紀錄。\n- `LICENSE`、`ATTRIBUTION.md`：授權與來源聲明，請一併保留。\n\n請使用自己的產品名稱、內容與素材。這份資料用於建立前端介面，實際功能仍需依需求完成並測試；品牌圖片、商標、專有字型與後端服務未附。\n\n規格版本：2026-11-01。使用說明更新：' + USAGE['updated'] + '。參考日期與來源以 SOURCES.json 為準；線上路徑以 https://webdesign.zero2codex.dev/ 為基準。\n'
BRAND_STEPS = '這個 ZIP 已包含設計規格、AI 指令與補充檔案，不需要再分別下載。\n\n## 照這三步開始\n\n1. 解壓縮這個 ZIP；你會在同一層看到 `DESIGN.md` 與 `PROMPTS.md`。\n2. 在你的專案建立 `design-reference/` 資料夾，把解壓後的全部檔案放進去。\n3. 在 Codex、Claude Code、Cursor 等能讀取專案檔案的工具中貼上下方指令，填入產品與功能需求。\n\n'
COLLECTION_STEPS = '這是批次收藏用的合集。先選一個品牌資料夾，使用一套設計開始製作。\n\n## 照這三步開始\n\n1. 解壓縮合集，選一個你喜歡的品牌資料夾；每個資料夾都有 `DESIGN.md` 與 `PROMPTS.md`。\n2. 在你的專案建立 `design-reference/`，把選定品牌資料夾內的檔案放進去，並保留合集根目錄的 `LICENSE` 與 `ATTRIBUTION.md`。\n3. 在能讀取專案檔案的 AI 開發工具中貼上下方指令，填入自己的產品與功能需求。\n\n如果只需要一套設計，也可以回到網站下載該品牌的設計包，使用相同的三個步驟。\n\n'

def brand_readme(study):
    return '# ' + study.get('name', study['slug']) + ' 設計包\n\n繁體中文（台灣用語，zh-TW）。\n\n' + BRAND_STEPS + COMMON_USAGE


def collection_readme(count):
    return f'# {count} 套設計合集\n\n繁體中文（台灣用語，zh-TW）。\n\n' + COLLECTION_STEPS + COMMON_USAGE


def write_study_pack(output, studies):
    entries, sources = [], []
    root = Path(__file__).resolve().parents[1]
    notices = [(name, (root / name).read_bytes()) for name in ('LICENSE', 'ATTRIBUTION.md')]
    for study in sorted(studies, key=lambda row: row['slug']):
        slug = study['slug']
        if not re.fullmatch(r'[a-z0-9.-]+', slug):
            raise ValueError('Unsafe study pack name')
        brand_entries = []
        for kind, name in [('analysis', 'DESIGN.md'), ('prompts', 'PROMPTS.md')]:
            source = study['study'].get(kind, '')
            if not re.fullmatch(r'official-drafts/[a-z0-9.-]+\.md', source):
                raise ValueError('Study pack requires a current ' + kind + ': ' + slug)
            data = (output / source).read_bytes()
            entries.append((slug + '/' + name, data))
            brand_entries.append((name, data))
        simple_pack = output / 'assets/design-packs' / (slug + '-simple.zip')
        simple_pack.parent.mkdir(parents=True, exist_ok=True)
        # Keep the two core documents unchanged; retain the notices in ZIP metadata.
        notice = b'LICENSE\n' + dict(notices)['LICENSE'] + b'\n\n' + USAGE['simple_pack_attribution'].encode()
        write_zip(simple_pack, list(brand_entries), comment=notice)
        study['simple_pack'] = 'assets/design-packs/' + slug + '-simple.zip'
        for name, file in sorted(study.get('implementation_files', {}).items()):
            if name not in ('ASSETS.json', 'ASSETS.md', 'TOKENS.json', 'starter.css') or file['path'] != f'implementation/{slug}/{name}':
                raise ValueError('Unsafe study pack companion')
            data = (output / file['path']).read_bytes()
            if hashlib.sha256(data).hexdigest() != file['sha256']:
                raise ValueError('Study pack companion hash mismatch')
            entries.append((slug + '/' + name, data))
            brand_entries.append((name, data))
        source_row = dict(slug=slug, date=study['date'], preview=study['preview'],
                            preview_sha256=study['preview_sha256'], analysis=study['study']['analysis'],
                            prompts=study['study']['prompts'], review=study['study'].get('review'))
        if study.get('implementation_files'):
            source_row.update(implementation_version=study['implementation_version'], reference_url=study['reference_url'],
                              implementation_files=study['implementation_files'])
            pack = output / 'assets/design-packs' / (slug + '.zip')
            pack.parent.mkdir(parents=True, exist_ok=True)
            write_zip(pack, brand_entries + [('README.md', brand_readme(study).encode()), ('SOURCES.json', (json.dumps([source_row], ensure_ascii=False, separators=(',', ':')) + '\n').encode())] + notices)
            study['implementation_pack'] = 'assets/design-packs/' + slug + '.zip'
        sources.append(source_row)
    entries += [('README.md', collection_readme(len(studies)).encode()), ('SOURCES.json', (json.dumps(sources, ensure_ascii=False, separators=(',', ':')) + '\n').encode())] + notices
    write_zip(output / 'assets/design-references.zip', entries)


def write_zip(path, entries, comment=b''):
    with ZipFile(path, 'w', compression=ZIP_DEFLATED, compresslevel=6) as archive:
        if len(comment) > 65535:
            raise ValueError('ZIP notice is too long')
        archive.comment = comment
        for name, data in entries:
            info = ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info._compresslevel = 6
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
