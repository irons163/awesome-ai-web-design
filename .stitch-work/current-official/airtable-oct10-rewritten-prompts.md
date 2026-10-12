# airtable｜重寫 AI 指令與實際生成紀錄

以下原始輸入曾實際送交 Google Stitch MCP，逐字保留；後續校正與原生輸出分開記錄。

```text
Reconstruct the CURRENT publicly visible Airtable homepage https://www.airtable.com/ as observed 2026-10-10. This is a free unofficial design study, no invented content. Desktop viewport 1280x720. Use the exact full page section order and visual measurements below. Do not create a dashboard specimen or redesign.
Header: pale #f0f3ff promo strip height42 says “Bring your Airtable data into Claude. Try it now →”, X close at far right. White 80px navigation with actual Airtable black logo left, Platform, Solutions, Resources, Enterprise, Pricing, outline Book Demo, black Sign up for free, Log in. Thin neutral borders.
Hero white centered: h1 at x240 y161 width800 height96 in Haas sans regular 40px /48px, dark #333840, EXACT “All your teams, all their workflows—connected in one workspace”. Body centered 18px, width800, line-height22: “Build AI-powered workflows that unify data, maximize collaboration, and set your teams up for long-term success. No code required.” Two 56px tall buttons, black rounded12 Get started for free and outline Book demo. Hero media starts x83 y444 width1114 with rounded16 pale pink background and real app table/video; use only actual official assets. Then 500,000 logos, pale workflow sections, light blue/dark blue/green feature panels, AI plays cards, resources, quote and footer. Keep genuine current official text, no fabricated names, metrics or testimonials.
Full page heading/typography records:
[
  {
    "box": {
      "height": 96,
      "width": 800,
      "x": 240,
      "y": 160.9921875
    },
    "color": "rgb(51, 56, 64)",
    "font": "Haas, -apple-system, \"system-ui\", \"Segoe UI\", Roboto, Oxygen, Ubuntu, Cantarell, \"Fira Sans\", \"Droid Sans\", \"Helvetica Neue\", sans-serif",
    "lineHeight": "48px",
    "size": "40px",
    "tag": "H1",
    "text": "All your teams, all their workflows—connected in one workspace",
    "weight": "400"
  },
  {
    "box": {
      "height": 18.8984375,
      "width": 1216,
      "x": 32,
      "y": 1150.3984375
    },
    "color": "rgb(51, 56, 64)",
    "font": "Haas, -apple-system, \"system-ui\", \"Segoe UI\", Roboto, Oxygen, Ubuntu, Cantarell, \"Fira Sans\", \"Droid Sans\", \"Helvetica Neue\", sans-serif",
    "lineHeight": "18.9px",
    "size": "14px",
    "tag": "H2",
    "text": "Trusted by 500,000 leading teams",
    "weight": "400"
  },
  {
    "box": {
      "height": 84.796875,
      "width": 1216,
      "x": 32,
      "y": 1301.296875
    },
    "color": "rgb(24, 29, 38)",
    "font": "\"Haas Groot Disp\", Haas, -apple-system, \"system-ui\", \"Segoe UI\", Roboto, Oxygen, Ubuntu, Cantarell, \"Fira Sans\", \"Droid Sans\", \"Helvetica Neue\", sans-serif",
    "lineHeight": "36.8px",
    "size": "32px",
    "tag": "H2",
    "text": "Sophisticated workflows in minutes, not months",
    "weight": "400"
  },
  {
    "box": {
      "height": 39,
      "width": 563.296875,
      "x": 355.5234375,
      "y": 1491.09375
    },
    "color": "rgb(255, 255, 255)",
    "font": "Haas, -apple-system, \"system-ui\", \"Segoe UI\", Roboto, Oxygen, Ubuntu, Cantarell, \"Fira Sans\", \"Droid Sans\", \"Helvetica Neue\", sans-serif",
    "lineHeight": "32.4px",
    "size": "24px",
    "tag": "H3",
    "text": "Production apps at prototype speed",
    "weight": "400"
  },
  {
    "box": {
      "height": 39,
      "width": 563.296875,
      "x": 355.5234375,
      "y": 2396.09375
    },
    "color": "rgb(24, 29, 38)",
    "font": "Haas, -apple-system, \"system-ui\", \"Segoe UI\", Roboto, Oxygen, Ubuntu, Cantarell, \"Fira Sans\", \"Droid Sans\", \"Helvetica Neue\", sans-serif",
    "lineHeight": "30px",
    "size": "24px",
    "tag": "H2",
    "text": "Don’t just ask AI. Deploy it.",
    "weight": "400"
  },
  {
    "box": {
      "height": 39,
      "width": 339.4453125,
      "x": 347.5234375,
      "y": 2925.09375
    },
    "color": "rgb(37, 79, 173)",
    "font": "Haas, -apple-system, \"system-ui\", \"Segoe UI\", Roboto, Oxygen, Ubuntu, Cantarell, \"Fira Sans\", \"Droid Sans\", \"Helvetica Neue\", sans-serif",
    "lineHeight": "30px",
    "size": "24px",
    "tag": "H2",
    "text": "Say hello to Omni",
    "weight": "400"
  },
  {
    "box": {
      "height": 157,
      "width": 339.4453125,
      "x": 347.5234375,
      "y": 3295.09375
    },
    "color": "rgb(33, 66, 36)",
    "font": "Haas, -apple-system, \"system-ui\", \"Segoe UI\", Roboto, Oxygen, Ubuntu, Cantarell, \"Fira Sans\", \"Droid Sans\", \"Helvetica Neue\", sans-serif",
    "lineHeight": "30px",
    "size": "24px",
    "tag": "H2",
    "text": "The power of AI with the industrial-grade platform your business demands",
    "weight": "400"
  },
  {
    "box": {
      "height": 40,
      "width": 1046.5703125,
      "x": 32,
      "y": 4101.34375
    },
    "color": "rgb(24, 29, 38)",
    "font": "\"Haas Groot Disp\", Haas, -apple-system, \"system-ui\", \"Segoe UI\", Roboto, Oxygen, Ubuntu, Cantarell, \"Fira Sans\", \"Droid Sans\", \"Helvetica Neue\", sans-serif",
    "lineHeight": "40px",
    "size": "32px",
    "tag": "H2",
    "text": "The path to 10x every person in your organization",
    "weight": "400"
  },
  {
    "box": {
      "height": 76,
      "width": 1134,
      "x": 73,
      "y": 6533
    },
    "color": "rgb(51, 56, 64)",
    "font": "Haas, -apple-system, \"system-ui\", \"Segoe UI\", Roboto, Oxygen, Ubuntu, Cantarell, \"Fira Sans\", \"Droid Sans\", \"Helvetica Neue\", sans-serif",
    "lineHeight": "40px",
    "size": "32px",
    "tag": "H2",
    "text": "Start building with AirtableTeams at over 500,000 forward-thinking organizations use Airtable every day. Join them.",
    "weight": "400"
  }
]
Use actual original public assets if available. Do not substitute stock photos or generated fake logos. External account/product links must go to official destinations; no payment, login form or signup backend. Preserve responsive behavior, desktop menus and narrow layout. Produce the full real homepage, not just the hero. Raw generated result will be separately retained, compared with actual source screenshots and corrected by hand. Do not label it verified or official.
```

後續校正應依相鄰的當前設計分析與實際畫面紀錄，保留公開原始圖片、SVG、字型與完整段落；動畫定格、未測互動及其他尺寸需如實列出，不能由供應商完成訊息推定與官方一致。
