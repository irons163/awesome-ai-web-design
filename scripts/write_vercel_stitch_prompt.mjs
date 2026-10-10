import fs from 'node:fs';
import path from 'node:path';
import {JSDOM,VirtualConsole} from 'jsdom';
const work=path.resolve('.stitch-work/current-official');
const read=name=>JSON.parse(fs.readFileSync(path.join(work,name),'utf8'));
const desktop=read('vercel-desktop-browser-reference.json'),mobile=read('vercel-mobile-browser-reference.json');
const document=new JSDOM(desktop.htmlParts.join(''),{virtualConsole:new VirtualConsole()}).window.document;
document.querySelectorAll('style').forEach(e=>e.remove());
const prompt=`Create a complete desktop screen and HTML for a free, attributed study of the actual Vercel homepage observed on October 10, 2026. These instructions are independently written from current public browser evidence, not copied from any upstream AI prompt. This current source takes precedence over older Vercel project screens.

The actual current headline is “Agentic Infrastructure”. Keep the black canvas, original white Vercel triangle, GeistSans original font files, fine gray interface type and 64px desktop navigation. At1280×720 the hero heading is left-aligned x24/y302, width444, height128, font64px/64px, weight400, tracking-3.84px, with Deploy now and Talk to sales below. The middle uses the actual luminous black Vercel triangle from the original public dark-glow image. The right column contains For coding agents / To ship apps and agents / Automated by agents. The current Ship26 SF announcement sits above it. Do not use the older centered “Your complete platform for the web” layout, generic colorful dashboards, or invented artwork.

Keep Products and Resources with their real Agent Stack/Core Platform/Tools and Learn/Build/Explore menu contents, Enterprise, Pricing, Get a Demo, Log In, Sign Up and their genuine destinations. Keep the actual Meta, BLACKBOX.AI, DoorDash, OpenAI, SpaceXAI, The Weather Company and Polymarket logo strip. Continue in this exact current order: “Build agents on infrastructure that thinks like them” with the original Notion product image and four features; “Ship apps that scale from zero to millions instantly” with the actual Zapier image and features; “Host platforms that serve every customer” with original Mintlify image and features; “Recently shipped” with current eve/Passport/Dockerfile links; “Built by you, or your agents” with the two actual calls to action; then the complete Vercel Directory/footer, current source links and theme controls. Preserve the source alternating wide section geometry, original image proportions and the black background through the entire page.

At390×844, preserve the actual compact header, top announcement, original mobile dark-glow triangle, centered two-line heading at x24/y444, width342, height112,48px/56px weight400 with-2.88px tracking. The mobile hero’s supporting line and vertically stacked actions follow it. The original mobile menu uses Products/Resources accordion summaries and the actual links. Do not compress the desktop three-column hero into a tiny row. This narrow reference uses a desktop user agent and is not proof of true phone fidelity.

Use all original public fonts, logos and image bytes, exact visible copy and destination links below. Account, sales and deployment actions open the real official site; this free study never collects credentials, takes payment or deploys a visitor’s account. Do not invent content, statistics, controls or illustrations. Preserve the existing imported design analysis separately from these new implementation instructions. Generation success is not visual acceptance.

Reference: ${desktop.reference_url}
Observed: ${desktop.observed_at}
Desktop measured headings: ${JSON.stringify(desktop.headings.filter(h=>h.text&&h.box.height>0),null,2)}
Narrow measured headings: ${JSON.stringify(mobile.headings.filter(h=>h.text&&h.box.height>0),null,2)}
Original public file resources: ${JSON.stringify(read('vercel-browser-asset-provenance.json').assets.map(a=>({kind:a.kind,url:a.source_url})),null,2)}
Original current images: ${JSON.stringify(desktop.images.filter(i=>!i.src.startsWith('data:')),null,2)}
Complete ordered current page copy (alternate hidden navigation states may also be present):
${document.body.textContent.replace(/\s+/g,' ').trim()}
`;
fs.writeFileSync(path.join(work,'vercel-stitch-oct10-desktop-prompt.md'),prompt);
console.log(JSON.stringify({brand:'vercel',chars:prompt.length}));
