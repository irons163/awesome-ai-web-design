"""Download the same dated analysis and prompt shown in the public tabs."""
import json
import re
from zipfile import ZipFile, ZipInfo, ZIP_STORED

README = '# 設計參考資料包\n\n每個品牌資料夾的 DESIGN.md 與 PROMPTS.md，對應網站主要分頁的設計分析與 AI 指令。\n\n各份參考日期與線上預覽路徑列於 SOURCES.json；相對路徑以網站根目錄為準。這個資料包提供 Markdown 規格，不包含完整預覽的圖片、字型或外部服務。\n\n原始 74 份分析、222 則任務指令與 AI 初稿仍保留於網站製作紀錄。已知差異依各品牌紀錄判讀。\n'


def write_study_pack(output, studies):
    entries, sources = [], []
    for study in sorted(studies, key=lambda row: row['slug']):
        slug = study['slug']
        if not re.fullmatch(r'[a-z0-9.-]+', slug):
            raise ValueError('Unsafe study pack name')
        for kind, name in [('analysis', 'DESIGN.md'), ('prompts', 'PROMPTS.md')]:
            source = study['study'].get(kind, '')
            if not re.fullmatch(r'official-drafts/[a-z0-9.-]+\.md', source):
                raise ValueError('Study pack requires a current ' + kind + ': ' + slug)
            entries.append((slug + '/' + name, (output / source).read_bytes()))
        sources.append(dict(slug=slug, date=study['date'], preview=study['preview'],
                            preview_sha256=study['preview_sha256'], analysis=study['study']['analysis'],
                            prompts=study['study']['prompts'], review=study['study'].get('review')))
    entries += [('README.md', README.encode()), ('SOURCES.json', (json.dumps(sources, ensure_ascii=False, separators=(',', ':')) + '\n').encode())]
    with ZipFile(output / 'assets/design-references.zip', 'w', compression=ZIP_STORED) as archive:
        for name, data in entries:
            info = ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)
