#!/usr/bin/env python3
"""Rebuild locally authored AI instructions; never downloads upstream content."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKER = '\n<!-- Original AI instructions: awesome-ai-web-design -->'


def make_prompts(entry):
    name = entry['name']
    start = f'Read the attached DESIGN.md as the visual reference for a {name}-inspired interface. '
    guard = ('Use my product name and content. Prefer existing project components and the current stack. '
             'Map the documented colors, typography, spacing, and radii to reusable tokens before styling. '
             'Use available system or open fonts when a listed font is unavailable; explain the substitution. ')
    quality = ('Make interactive elements work and expose their state to assistive technology. '
               'Provide visible keyboard focus, labeled controls, reduced-motion support, and at least 44px touch targets. '
               'If an imported visual rule conflicts with usability, make the smallest accessible adjustment and record it. '
               'Check the result at 390px, 768px, and 1440px, including long text and empty content. '
               'Finish with the implemented files, verification results, and any remaining assumptions.')
    return [
        {'id':'build','title':'建立新頁面','text':start + 'Implement this working page: ' + entry['brief'] + '\n\n' + guard + '\n\n' + quality},
        {'id':'component','title':'製作元件','text':start + 'Build ' + entry['component'] + '. '
         + 'Show it inside a small, realistic example using the existing component conventions. '
         + 'Derive its proportions and visual hierarchy from the reference; do not simply recolor a generic card. '
         + 'Support default, focused, disabled, loading, and error states wherever they apply. '
         + 'Use meaningful sample content and make every visible action functional.\n\n' + guard + '\n\n' + quality},
        {'id':'restyle','title':'改造既有介面','text':start + 'Restyle the selected page while preserving its routes, data, behavior, and user-facing meaning. '
         + 'First identify the existing page hierarchy and the smallest reusable token and component changes. '
         + 'Use this composition as a visual direction, adapting it to the page rather than adding unrelated features: '
         + entry['brief'] + '\n\n' + guard
         + 'Apply the visual changes in coherent component groups and check for unintended changes elsewhere. '
         + 'Report the main before-and-after differences.\n\n' + quality}
    ]


def remove_upstream_instructions(text):
    text = text.split(MARKER)[0]
    # Remove whole prompt and iteration sections at their own heading depth.
    lines = text.splitlines(keepends=True)
    kept, skip_level = [], None
    for line in lines:
        heading = re.match(r'^(#{1,6})\s+(.+)', line)
        if heading:
            level, title = len(heading[1]), heading[2]
            if skip_level is not None and level <= skip_level:
                skip_level = None
            if skip_level is None and re.search(r'Agent Prompt Guide|Example (?:Component )?Prompts|Iteration Guide', title, re.I):
                skip_level = level
        if skip_level is None:
            kept.append(line)
    return ''.join(kept).rstrip()


def main():
    for entry in json.loads((ROOT/'data/recipes.json').read_text()):
        folder = ROOT/'design-md'/entry['slug']
        prompts = make_prompts(entry)
        prompt_doc = f"# {entry['name']} — original AI prompts\n\n"
        prompt_doc += 'Place DESIGN.md beside your project, then choose a task below. These instructions were written for this free collection. Replace sample content with your own requirements.\n\n'
        for prompt in prompts:
            prompt_doc += f"## {prompt['title']}\n\n```text\n{prompt['text']}\n```\n\n"
        prompt_doc += ('## Iteration workflow\n\n'
                       '1. Name one observable problem in the current result, such as weak hierarchy or clipped content.\n'
                       '2. Locate the matching token or component rule in DESIGN.md and propose a bounded change.\n'
                       '3. Apply that change without modifying unrelated routes or data behavior.\n'
                       '4. Inspect keyboard focus, narrow-screen layout, and representative content states.\n'
                       '5. Report the result and any deliberate departure from the visual reference.\n')
        (folder/'PROMPTS.md').write_text(prompt_doc)
        base = remove_upstream_instructions((folder/'DESIGN.md').read_text())
        notice = '\n\n## Provenance and scope\n\nVisual analysis adapted from VoltAgent/awesome-design-md under the MIT license; see the repository LICENSE and ATTRIBUTION.md. Brand names identify the reference only. The AI instructions below are independently authored for this collection. The accessibility checks in these instructions take precedence over conflicting legacy interaction notes.\n'
        # Idempotent regeneration: the provenance notice belongs to the generated section.
        (folder/'DESIGN.md').write_text(base + MARKER + notice + '\n' + prompt_doc.replace('# '+entry['name']+' — original AI prompts', '## Original AI task prompts', 1))
        (folder/'README.md').write_text(f"# {entry['name']}\n\n{entry['description']}\n\n這套設計規格與所有指令均可免費使用，無須登入。\n\n- [完整設計規格](DESIGN.md)\n- [重新撰寫的 AI 指令](PROMPTS.md)\n- [淺色元件預覽](preview.html)\n- [深色元件預覽](preview-dark.html)\n- [回到總目錄](../../README.md)\n\n設計分析源自 VoltAgent 的 MIT 開源資料；AI 指令與預覽由本專案重新製作。預覽是 token 元件示意，不是品牌官方網站截圖。\n")
    count = len(json.loads((ROOT/'data/recipes.json').read_text()))
    print(f'Wrote {count * 3} original task prompts across {count} design systems.')

if __name__ == '__main__':
    main()
