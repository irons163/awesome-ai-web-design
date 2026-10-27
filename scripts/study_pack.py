"""Download the same dated analysis and prompt shown in the public tabs."""
import json
import re
import hashlib
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

README = '# 設計實作資料包\n\n繁體中文（台灣用語，zh-TW）。版本：2026-10-20。\n\n1. 選擇一個品牌資料夾，將 DESIGN.md 與 PROMPTS.md 交給 AI。\n2. 在指令中填入自己的產品、內容、功能及資料；沒有照片時選擇規格的無圖版。\n3. 檢查 390、768、1440px 與主要操作，依結果調整，不把單次生成視為完成驗收。\n\nDESIGN.md 已含完整角色色碼、字級、間距、元件狀態、響應式條件、素材替代方式與可直接採用的 CSS，不依賴未附上的延伸規格。starter.css 與 TOKENS.json 是同版本的樣式與機器可讀數值；ASSETS.md、ASSETS.json 列出自有素材需求與缺少時的作法。單一品牌 ZIP 的檔案直接放在根目錄。每個 ZIP 均附 LICENSE 與 ATTRIBUTION.md，保留授權與來源說明。\n\n規格明確區分來源宣告與實作建議值，不保證與原官網像素相同。品牌圖片、商標、專有字型與後端未附，但不使用外部素材也能依規格做出文字版原型。請勿將建議素材路徑當成已存在檔案。\n\nSOURCES.json 記錄原參考日期、預覽摘要與實作版本，線上路徑以 https://webdesign.zero2codex.dev/ 為基準。歷史生成及比對紀錄另保留於網站開發紀錄，AI 指令不依賴它們。\n'


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
            write_zip(pack, brand_entries + [('README.md', README.encode()), ('SOURCES.json', (json.dumps([source_row], ensure_ascii=False, separators=(',', ':')) + '\n').encode())] + notices)
            study['implementation_pack'] = 'assets/design-packs/' + slug + '.zip'
        sources.append(source_row)
    entries += [('README.md', README.encode()), ('SOURCES.json', (json.dumps(sources, ensure_ascii=False, separators=(',', ':')) + '\n').encode())] + notices
    write_zip(output / 'assets/design-references.zip', entries)


def write_zip(path, entries):
    with ZipFile(path, 'w', compression=ZIP_DEFLATED, compresslevel=6) as archive:
        for name, data in entries:
            info = ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info._compresslevel = 6
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
