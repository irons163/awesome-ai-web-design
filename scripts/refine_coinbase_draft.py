#!/usr/bin/env python3
"""Build an unofficial, dated Coinbase Canada study from observed public content."""

from __future__ import annotations

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
ASSETS = 'coinbase-assets/'

USDC = (
    ('Earn Rewards Automatically', 'No need to opt-in. When you hold USDC on Coinbase, you earn 3.60% rewards instantly, with weekly payouts.'),
    ('Boosted rates with Coinbase One', 'Join Coinbase One and earn up to 4.00%.'),
    ('Access your USDC anytime', 'Sell, send, or convert your USDC whenever you want — no lock-ups.'),
)
CANADA = (
    ('Top up without fees with Interac e-Transfer and Electronic Funds Transfer (EFT)', 'Quick and easy cash top-ups, even for larger amounts.'),
    ('Instant sell & withdraw', 'Sell your crypto and cash out instantly to most banks.'),
    ('Buy directly with PayPal or card', 'Get crypto instantly using PayPal or a supported debit or credit card.'),
    ('Simple & secure onboarding flow', 'Create your account without hassle.'),
    ('Trade 200+ assets securely', 'From Bitcoin to Ethereum to your favorite tokens.'),
)
ADVANCED = (
    ('More order types', 'Market, Limit, Stop Limit, and Auction Mode orders.'),
    ('Powerful trading tools', 'Charts powered by TradingView with EMA, MA, MACD, RSI, and Bollinger Bands.'),
    ('One unified balance', 'Seamlessly switch between Simple and Advanced Trade.'),
)
TRUST = (
    ('worldwide.svg', 'The largest public crypto company', 'In April 2021, Coinbase became the largest publicly traded crypto company in the world. That means we operate with more financial transparency, and make our financial statements available each quarter.', 'https://investor.coinbase.com/home/default.aspx'),
    ('safe.svg', 'Your assets are secure', "Your crypto is your crypto. It’s that simple. Coinbase doesn't use, or lend, your assets without your permission. Also, we offer risk management programs designed to protect customers' assets.", 'https://help.coinbase.com/coinbase/other-topics/legal-policies/what-does-coinbase-do-with-my-digital-assets'),
    ('support.svg', 'The help you need, when you need it', 'You can contact support through the virtual assistant or, depending on the hours, a live support agent. The Help Center also provides solutions to common problems.', 'https://help.coinbase.com/en'),
    ('canada.svg', 'Built for Canadians', 'Coinbase is committed to Canada and continues working with regulators on a framework that supports innovation and prioritizes consumer protection.', 'https://www.coinbase.com/en-ca/blog/building-for-canada-and-the-world-from-canada'),
)
FOOTER = (
    ('Company', (
        ('About', 'https://www.coinbase.com/en-ca/about'),
        ('Careers', 'https://www.coinbase.com/en-ca/careers'),
        ('Affiliates', 'https://www.coinbase.com/en-ca/affiliates'),
        ('Blog', 'https://www.coinbase.com/en-ca/blog'),
        ('Press', 'https://www.coinbase.com/en-ca/press'),
        ('Security', 'https://www.coinbase.com/en-ca/security'),
        ('Investors', 'https://investor.coinbase.com/'),
        ('Vendors', 'https://www.coinbase.com/en-ca/vendors/vendors-at-coinbase'),
        ('Legal & privacy', 'https://www.coinbase.com/en-ca/legal'),
        ('Cookie policy', 'https://www.coinbase.com/en-ca/legal/cookie'),
        ('Digital Asset Disclosures', 'https://www.coinbase.com/en-ca/legal/digital-asset-disclosures'),
    )),
    ('Learn', (
        ('Explore crypto', 'https://www.coinbase.com/en-ca/explore'),
        ('Explore stocks', 'https://www.coinbase.com/en-ca/stock/explore'),
        ('Market statistics', 'https://www.coinbase.com/en-ca/market-stats'),
        ('Coinbase Bytes newsletter', 'https://www.coinbase.com/en-ca/bytes'),
        ('Crypto basics', 'https://www.coinbase.com/en-ca/learn/crypto-basics'),
        ('Tips & tutorials', 'https://www.coinbase.com/en-ca/learn/tips-and-tutorials'),
        ('Crypto glossary', 'https://www.coinbase.com/en-ca/learn/crypto-glossary'),
        ('Market updates', 'https://www.coinbase.com/en-ca/learn/market-updates'),
        ('What is Bitcoin?', 'https://www.coinbase.com/en-ca/learn/crypto-basics/what-is-bitcoin'),
        ('What is crypto?', 'https://www.coinbase.com/en-ca/learn/crypto-basics/what-is-cryptocurrency'),
        ('What is a blockchain?', 'https://www.coinbase.com/en-ca/learn/crypto-basics/what-is-a-blockchain'),
        ('How to set up a crypto wallet?', 'https://www.coinbase.com/en-ca/learn/tips-and-tutorials/how-to-set-up-a-crypto-wallet'),
        ('How to send crypto?', 'https://www.coinbase.com/en-ca/learn/tips-and-tutorials/how-to-send-crypto'),
        ('Taxes', 'https://www.coinbase.com/en-ca/learn/crypto-basics/understanding-crypto-taxes'),
    )),
    ('Individuals', (
        ('Buy & sell', 'https://www.coinbase.com/en-ca/explore'),
        ('Coinbase Wallet', 'https://base.app/'),
        ('Coinbase One', 'https://www.coinbase.com/en-ca/one'),
        ('Debit Card', 'https://www.coinbase.com/en-ca/card'),
    )),
    ('Businesses', (
        ('Asset Listings', 'https://www.coinbase.com/en-ca/listings'),
        ('Payments', 'https://www.coinbase.com/en-ca/payments'),
        ('Token Manager', 'https://www.coinbase.com/en-ca/tokenmanager'),
    )),
    ('Institutions', (
        ('Prime', 'https://www.coinbase.com/en-ca/prime'),
        ('Staking', 'https://www.coinbase.com/en-ca/staking'),
        ('Exchange', 'https://www.coinbase.com/en-ca/exchange'),
        ('International Exchange', 'https://www.coinbase.com/en-ca/international-exchange'),
        ('Derivatives Exchange', 'https://www.coinbase.com/derivatives'),
        ('Verified Pools', 'https://www.coinbase.com/en-ca/verified-pools'),
    )),
    ('Developers', (
        ('Developer Platform', 'https://www.coinbase.com/en-ca/developer-platform'),
        ('Base', 'https://base.org/'),
        ('Server Wallets', 'https://www.coinbase.com/en-ca/developer-platform/products/wallets'),
        ('Embedded Wallets', 'https://www.coinbase.com/en-ca/developer-platform/products/embeddedwallets'),
        ('Base Accounts (Smart Wallets)', 'https://www.base.org/build/base-account'),
        ('Onramp & Offramp', 'https://www.coinbase.com/en-ca/developer-platform/products/onramp'),
        ('x402', 'https://www.x402.org/'),
        ('Trade API', 'https://www.coinbase.com/en-ca/developer-platform/products/trade-api'),
        ('Paymaster', 'https://www.coinbase.com/en-ca/developer-platform/products/paymaster'),
        ('OnchainKit', 'https://www.base.org/build/onchainkit'),
        ('Data API', 'https://www.coinbase.com/en-ca/developer-platform/products/data-api'),
        ('Verifications', 'https://www.coinbase.com/en-ca/developer-platform/products/verifications'),
        ('Node', 'https://www.coinbase.com/en-ca/developer-platform/products/node'),
        ('AgentKit', 'https://www.coinbase.com/en-ca/developer-platform/products/agentkit'),
        ('Staking', 'https://www.coinbase.com/en-ca/developer-platform/products/staking'),
        ('Faucet', 'https://www.coinbase.com/en-ca/developer-platform/products/faucet'),
        ('Exchange API', 'https://www.coinbase.com/en-ca/developer-platform/products/exchange-api'),
        ('International Exchange API', 'https://docs.cdp.coinbase.com/international-exchange/introduction/welcome'),
        ('Prime API', 'https://docs.cdp.coinbase.com/prime/introduction/welcome'),
        ('Derivatives API', 'https://docs.cdp.coinbase.com/derivatives/introduction/welcome'),
    )),
    ('Support', (
        ('Help center', 'https://help.coinbase.com/'),
        ('Contact us', 'https://help.coinbase.com/contact-us/'),
        ('Create account', 'https://help.coinbase.com/coinbase/getting-started/getting-started-with-coinbase/create-a-coinbase-account/'),
        ('ID verification', 'https://help.coinbase.com/coinbase/managing-my-account#identity-verification/'),
        ('Account information', 'https://help.coinbase.com/coinbase/managing-my-account/'),
        ('Payment methods', 'https://help.coinbase.com/coinbase/getting-started#add-a-payment-method/'),
        ('Account access', 'https://help.coinbase.com/coinbase/managing-my-account/'),
        ('Supported crypto', 'https://help.coinbase.com/supported-crypto.html'),
        ('Status', 'https://status.coinbase.com/'),
    )),
    ('Asset prices', (
        ('Bitcoin price', 'https://www.coinbase.com/en-ca/price/bitcoin'),
        ('Ethereum price', 'https://www.coinbase.com/en-ca/price/ethereum'),
        ('Solana price', 'https://www.coinbase.com/en-ca/price/solana'),
        ('XRP price', 'https://www.coinbase.com/en-ca/price/xrp'),
        ('NVIDIA price', 'https://www.coinbase.com/en-ca/stock/nvda'),
        ('Apple price', 'https://www.coinbase.com/en-ca/stock/aapl'),
        ('Microsoft price', 'https://www.coinbase.com/en-ca/stock/msft'),
        ('Amazon price', 'https://www.coinbase.com/en-ca/stock/amzn'),
    )),
)


def bullets(items: tuple[tuple[str, str], ...]) -> str:
    return '<ul class="benefits">' + ''.join(
        '<li><span class="check" aria-hidden="true">✓</span><span>'
        f'<strong>{escape(title)}</strong><small>{escape(detail)}</small></span></li>'
        for title, detail in items
    ) + '</ul>'


def feature(name: str, title: str, media: str, alt: str, items: tuple[tuple[str, str], ...],
            href: str, cta: str, reverse: bool = False, shaded: bool = False,
            intro: str = '', note: str = '') -> str:
    classes = 'feature ' + ('reverse ' if reverse else '') + ('shaded' if shaded else '')
    copy = (f'<div class="feature-copy"><h2>{escape(title)}</h2>'
            + (f'<p class="feature-intro">{escape(intro)}</p>' if intro else '')
            + (bullets(items) if items else '')
            + f'<a class="blue-button" href="{escape(href, quote=True)}">{escape(cta)}</a>'
            + (f'<p class="rate-note">{escape(note)}</p>' if note else '') + '</div>')
    image = (f'<div class="feature-media"><img src="{ASSETS}{media}" alt="{escape(alt, quote=True)}" '
             'loading="lazy"></div>')
    return (f'<section class="{classes}" id="{name}"><div class="feature-inner">'
            + (copy + image if reverse else image + copy) + '</div></section>')


def trust_cards() -> str:
    return ''.join(
        f'<article class="trust-card"><img src="{ASSETS}{icon}" alt="" loading="lazy">'
        f'<h3>{escape(title)}</h3><p>{escape(detail)}</p>'
        f'<a href="{escape(href, quote=True)}">Learn more <span aria-hidden="true">↗</span></a></article>'
        for icon, title, detail, href in TRUST
    )


def footer_columns() -> str:
    return ''.join(
        f'<div class="footer-col"><h3>{escape(group)}</h3>'
        + ''.join(f'<a href="{escape(url, quote=True)}">{escape(label)}</a>' for label, url in links)
        + '</div>' for group, links in FOOTER
    )


def main() -> None:
    html = '''<!doctype html><html lang="en-CA"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Coinbase Canada homepage study · Awesome AI Web Design</title>
<meta name="description" content="Unofficial dated visual study of the Coinbase Canada homepage observed September 28, 2026.">
<style>
@font-face{font-family:CoinbaseDisplay;src:url(coinbase-assets/CoinbaseDisplay-Regular.woff2) format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:CoinbaseDisplay;src:url(coinbase-assets/CoinbaseDisplay-Medium.woff2) format('woff2');font-weight:500 800;font-display:swap}
@font-face{font-family:CoinbaseSans;src:url(coinbase-assets/CoinbaseSans-Regular.woff2) format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:CoinbaseSans;src:url(coinbase-assets/CoinbaseSans-Medium.woff2) format('woff2');font-weight:500 800;font-display:swap}
@font-face{font-family:CoinbaseText;src:url(coinbase-assets/CoinbaseText-Regular.woff2) format('woff2');font-weight:400;font-display:swap}
:root{--blue:#0052ff;--ink:#0a0b0d;--muted:#5b616e;--pale:#eef0f3;--line:#d9dcdf;--width:1216px}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:var(--ink);background:#fff;font:16px/1.5 CoinbaseSans,Arial,sans-serif}button,input{font:inherit}button{cursor:pointer}a{text-decoration:none;color:inherit}img{display:block;max-width:100%}a:focus-visible,button:focus-visible{outline:3px solid var(--blue);outline-offset:3px}
.campaign{height:48px;background:#f6f7f8;display:flex;align-items:center;justify-content:center;font-size:14px;font-weight:500}.campaign a{display:flex;align-items:center;gap:8px}.campaign a:hover{text-decoration:underline}.campaign span{font-size:19px;line-height:1}
.header{height:68px;background:#fff;position:sticky;top:0;z-index:80;border-bottom:1px solid #eee}.header-inner{height:100%;max-width:1280px;margin:auto;padding:0 32px;display:flex;align-items:center;gap:30px}.brand{width:40px;flex:none}.brand img{width:40px;height:40px}.nav{display:flex;align-items:center;gap:20px;white-space:nowrap}.nav a,.nav button{font-size:14px;font-weight:500;border:0;background:none;padding:10px 0;color:#111}.nav a:hover,.nav button:hover{color:var(--blue)}.header-actions{margin-left:auto;display:flex;align-items:center;gap:15px}.icon-btn{width:32px;height:32px;display:grid;place-items:center;border:0;background:transparent;padding:0}.icon-btn svg{width:22px;height:22px;stroke:#111;stroke-width:2;fill:none}.header-signin{font-size:14px;font-weight:600;white-space:nowrap}.pill{height:40px;padding:0 19px;display:inline-flex;align-items:center;justify-content:center;background:var(--blue);color:#fff;border-radius:999px;font-size:14px;font-weight:600;white-space:nowrap}.pill:hover,.blue-button:hover{background:#003fc5}.menu-button,.mobile-panel{display:none}.desktop-menu{display:none;position:absolute;top:68px;left:0;right:0;background:#fff;border-top:1px solid #eee;border-bottom:1px solid #eee;box-shadow:0 12px 24px #0001}.desktop-menu.open{display:block}.desktop-menu-inner{max-width:1216px;margin:auto;padding:34px 0;display:flex;gap:60px}.desktop-menu a{display:block;padding:8px 0;font-size:15px}.desktop-menu a:hover{color:var(--blue)}.desktop-menu strong{display:block;margin-bottom:8px;font-size:13px;color:var(--muted)}
.hero{height:668px;background:var(--pale)}.hero-inner{max-width:var(--width);height:100%;margin:auto;display:grid;grid-template-columns:1fr 1fr;column-gap:26px}.hero-copy{padding-top:146px}.hero h1{font:500 80px/1 CoinbaseDisplay,Arial,sans-serif;letter-spacing:-3.8px;margin:0}.hero p{font:400 18px/1.5 CoinbaseSans,Arial,sans-serif;max-width:540px;margin:28px 0 22px}.blue-button{height:56px;min-width:129px;padding:0 25px;display:inline-flex;align-items:center;justify-content:center;background:var(--blue);border-radius:999px;color:#fff;font:600 16px/1 CoinbaseSans,Arial,sans-serif;white-space:nowrap}.hero-media{display:flex;align-items:center;justify-content:center}.hero-media img{width:540px;height:540px;object-fit:contain}
.feature{background:#fff}.feature.shaded{background:var(--pale)}.feature-inner{max-width:1136px;margin:auto;display:grid;grid-template-columns:542px 542px;gap:50px;align-items:center}.feature-media img{width:542px;height:434px;object-fit:contain}.feature-copy h2{font:500 44px/1.1 CoinbaseDisplay,Arial,sans-serif;letter-spacing:-1.5px;margin:0 0 32px}.feature-copy .feature-intro{font:18px/1.45 CoinbaseSans,Arial,sans-serif;margin:0 0 26px}.benefits{list-style:none;margin:0 0 28px;padding:0;display:grid;gap:21px}.benefits li{display:flex;align-items:flex-start;gap:16px}.check{width:22px;height:22px;flex:none;border-radius:50%;background:var(--blue);color:white;text-align:center;font:600 14px/22px CoinbaseSans,Arial,sans-serif;margin-top:3px}.benefits strong{display:block;font:600 18px/1.35 CoinbaseSans,Arial,sans-serif}.benefits small{display:block;font:400 16px/1.45 CoinbaseText,Arial,sans-serif;color:var(--muted);margin-top:4px}.rate-note{font-size:12px;color:#666;margin:10px 0 0}.feature.reverse .feature-copy{grid-column:1;grid-row:1}.feature.reverse .feature-media{grid-column:2;grid-row:1}
#usdc{height:596px}#canada{height:704px}#apy{height:644px}#advanced{height:624px}#membership{height:596px}#apy .feature-copy h2,#membership .feature-copy h2{max-width:510px}
.video{height:844px;padding:80px 32px}.video a{position:relative;display:block;max-width:1216px;height:684px;margin:auto;overflow:hidden;border-radius:8px;background:#071734}.video img{width:100%;height:100%;object-fit:cover}.video-play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:74px;height:74px;border-radius:50%;background:#fff;color:#111;display:grid;place-items:center;font-size:27px;padding-left:4px;box-shadow:0 6px 30px #0005}
.trust{min-height:1212px;padding:80px 0 72px}.trust-header{text-align:center;max-width:830px;margin:0 auto 64px}.trust-header h2{font:500 64px/1.05 CoinbaseDisplay,Arial,sans-serif;letter-spacing:-2.6px;margin:0 auto 23px}.trust-header p{font:18px/1.5 CoinbaseSans,Arial,sans-serif;margin:0;color:#2c3138}.trust-grid{max-width:1136px;margin:auto;display:grid;grid-template-columns:1fr 1fr;gap:16px}.trust-card{min-height:366px;padding:32px;border:1px solid #e2e4e6;border-radius:18px;display:flex;flex-direction:column}.trust-card img{width:52px;height:52px;margin-bottom:26px}.trust-card h3{font:500 20px/1.25 CoinbaseDisplay,Arial,sans-serif;margin:0 0 12px}.trust-card p{font:16px/1.45 CoinbaseText,Arial,sans-serif;color:#454b55;margin:0 0 20px;max-width:485px}.trust-card a{color:var(--blue);font-weight:600;margin-top:auto}.trust-card a span{margin-left:5px}
.disclosure{background:#f8f9fa;min-height:517px;padding:56px max(32px,calc((100vw - 1136px)/2));color:#4b515b}.disclosure h2{font-size:13px;letter-spacing:.06em;margin:0 0 22px}.disclosure p{font:13px/1.55 CoinbaseText,Arial,sans-serif;margin:0 0 13px}.disclosure a{text-decoration:underline}.footer{max-width:1216px;margin:auto;padding:88px 0 30px}.footer-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:22px}.footer-col{display:flex;flex-direction:column;gap:11px}.footer-col h3{font-size:16px;margin:0 0 8px}.footer-col a{font-size:14px;color:#626975}.footer-col a:hover{color:var(--blue)}.footer-bottom{border-top:1px solid #e5e6e8;margin-top:70px;padding-top:25px;display:flex;justify-content:space-between;color:#626975;font-size:13px}.footer-bottom a:hover{text-decoration:underline}
@media(max-width:1200px){.header-inner,.hero-inner{padding-left:24px;padding-right:24px}.nav{gap:12px}.header-inner{gap:18px}.feature-inner,.trust-grid{width:calc(100% - 64px);grid-template-columns:repeat(2,minmax(0,1fr));gap:32px}.feature-media img{width:100%}.footer{padding-left:32px;padding-right:32px}}
@media(max-width:860px){.nav,.header-signin,.language{display:none}.menu-button{display:grid}.header-inner{padding:0 20px}.desktop-menu{display:none!important}.mobile-panel{display:none;position:fixed;z-index:79;top:116px;bottom:0;left:0;right:0;background:#fff;overflow:auto;padding:24px 20px}.mobile-panel.open{display:flex;flex-direction:column}.mobile-panel a{padding:16px 0;border-bottom:1px solid #eceff1;font-weight:600}.mobile-panel .spacer{flex:1}.mobile-panel .bottom-link{border:0}.hero{height:auto}.hero-inner{display:block;padding:36px 24px 60px}.hero-copy{padding:0}.hero h1{font-size:64px}.hero-media img{margin:36px auto 0;width:min(540px,100%);height:auto}.feature{height:auto!important}.feature-inner{display:flex;flex-direction:column;width:auto;margin:auto;padding:64px 24px;gap:30px}.feature.reverse .feature-media{order:0}.feature.reverse .feature-copy{order:1}.feature-media,.feature-copy{width:min(100%,640px)}.feature-media img{height:auto}.video{height:auto;padding:40px 24px}.video a{height:auto;aspect-ratio:16/9}.trust{padding:70px 24px}.trust-header h2{font-size:52px}.trust-grid{width:100%}.disclosure{padding:48px 24px}.footer-grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:600px){.campaign{font-size:12px;padding:0 12px;text-align:center}.header{height:72px}.header-inner{padding:0 16px;gap:8px}.brand,.brand img{width:40px;height:40px}.header-actions{gap:8px}.header-actions .pill{height:36px;padding:0 14px;font-size:13px}.header-actions .icon-btn{width:30px}.mobile-panel{top:120px;padding:16px}.mobile-panel a{font-size:18px;padding:18px 2px}.hero-inner{padding:32px 16px 0}.hero h1{font-size:52px;line-height:1;letter-spacing:-2.4px}.hero p{font-size:18px;line-height:1.42;margin:24px 0 24px}.hero .blue-button{width:100%;height:56px}.hero-media img{width:100%;margin:36px 0 0}.feature-inner{padding:80px 16px 72px;gap:34px}.feature-media img{width:100%;height:auto}.feature-copy h2{font-size:36px;line-height:1.1;letter-spacing:-.9px;margin-bottom:26px}.benefits{gap:22px}.benefits strong{font-size:17px}.benefits small{font-size:15px}.feature .blue-button{width:100%}.video{padding:40px 16px}.video a{border-radius:6px}.video-play{width:54px;height:54px;font-size:20px}.trust{padding:48px 16px 64px}.trust-header{text-align:left;margin-bottom:36px}.trust-header h2{font-size:44px;line-height:1.02;letter-spacing:-1.7px}.trust-header p{font-size:17px}.trust-grid{grid-template-columns:1fr;gap:12px}.trust-card{min-height:340px;padding:28px}.disclosure{padding:40px 16px}.footer{padding:60px 16px 28px}.footer-grid{grid-template-columns:1fr 1fr;gap:36px 22px}.footer-bottom{display:block;line-height:2}}
.feature-inner{height:100%}
@media(min-width:1201px){.hero-inner{grid-template-columns:584px 540px;column-gap:70px}.hero-media{justify-content:flex-start}.hero p{max-width:584px;margin:24px 0;line-height:28px}.trust{height:1212px;padding-bottom:0}.trust-header{margin-bottom:94px}.trust-card{min-height:392px}.footer{min-height:1254px}}
@media(max-width:600px){.hero{height:806px}.hero-inner{height:100%;padding:32px 16px}.hero p{line-height:28px;margin:16px 0}.hero-media img{width:358px;height:358px;margin-top:24px;object-fit:contain}.feature-inner{height:100%;padding:49px 16px 0;gap:25px}.feature-media{flex:0 0 285px;width:100%}.feature-media img{width:356px;height:285px;object-fit:contain;margin:auto}.feature-copy{width:100%}#usdc{height:847px!important}#canada{height:1023px!important}#apy{height:647px!important}#advanced{height:903px!important}#membership{height:662px!important}#apy .feature-inner{gap:73px}.video{height:297px;padding:48px 16px}.video a{height:201px;aspect-ratio:auto}.trust{height:2076px;padding:48px 16px 0}.trust-header{margin-bottom:60px}.trust-card{min-height:0;height:428px}.trust-grid{gap:16px}}
@media(max-width:600px){.disclosure{height:685px}.footer{height:3154px;padding:132px 20px 0}.footer-grid{display:flex;flex-direction:column;gap:12px}.footer-col{gap:8px}.footer-col h3{font-size:18px;line-height:24px;margin:0}.footer-col a{font-size:16px;line-height:24px}.footer-col:nth-child(1){order:1;margin-bottom:32px}.footer-col:nth-child(2){order:2}.footer-col:nth-child(7){order:3}.footer-col:nth-child(3){order:4}.footer-col:nth-child(4){order:5}.footer-col:nth-child(5){order:6}.footer-col:nth-child(6){order:7}.footer-col:nth-child(8){order:8}.footer-bottom{margin-top:129px;padding-top:25px}}
</style></head><body>
<a class="campaign" href="https://www.coinbase.com/signup">Get up to CA$200 for getting started¹ <span aria-hidden="true">→</span></a>
<header class="header"><div class="header-inner"><a class="brand" href="https://www.coinbase.com/en-ca" aria-label="Coinbase"><img src="coinbase-assets/logo.svg" alt="Coinbase"></a>
<nav class="nav" aria-label="Primary"><a href="https://www.coinbase.com/en-ca/explore">Cryptocurrencies</a><button type="button" data-menu="individuals">Individuals</button><button type="button" data-menu="businesses">Businesses</button><button type="button" data-menu="institutions">Institutions</button><button type="button" data-menu="developers">Developers</button><button type="button" data-menu="company">Company</button></nav>
<div class="header-actions"><a class="icon-btn" href="https://www.coinbase.com/en-ca/explore" aria-label="Search"><svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="7"></circle><path d="m16 16 5 5"></path></svg></a><a class="icon-btn language" href="https://www.coinbase.com/en-ca" aria-label="Canada English"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"></circle><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"></path></svg></a><a class="header-signin" href="https://www.coinbase.com/signin?locale=en-ca">Sign in</a><a class="pill" href="https://www.coinbase.com/signup">Sign up</a><button class="icon-btn menu-button" type="button" id="menu-toggle" aria-label="Open menu" aria-expanded="false"><svg viewBox="0 0 24 24"><path d="M3 6h18M3 12h18M3 18h18"></path></svg></button></div></div>
<div class="desktop-menu" id="desktop-menu"><div class="desktop-menu-inner"><div><strong>Explore Coinbase</strong><a href="https://www.coinbase.com/en-ca/">Buy & sell crypto</a><a href="https://www.coinbase.com/en-ca/advanced-trade">Advanced Trade</a><a href="https://www.coinbase.com/en-ca/one">Coinbase One</a></div><div><strong>Resources</strong><a href="https://www.coinbase.com/en-ca/explore">Cryptocurrencies</a><a href="https://www.coinbase.com/developer-platform">Developer Platform</a><a href="https://help.coinbase.com/en">Help center</a></div></div></div></header>
<nav class="mobile-panel" id="mobile-panel" aria-label="Mobile"><a href="https://www.coinbase.com/en-ca/explore">Cryptocurrencies</a><a href="https://www.coinbase.com/en-ca/">Individuals</a><a href="https://www.coinbase.com/commerce">Businesses</a><a href="https://www.coinbase.com/institutional">Institutions</a><a href="https://www.coinbase.com/developer-platform">Developers</a><a href="https://www.coinbase.com/about">Company</a><span class="spacer"></span><a class="bottom-link" href="https://www.coinbase.com/en-ca">Canada · English</a><a class="bottom-link" href="https://www.coinbase.com/signin?locale=en-ca">Sign in</a></nav>
<main id="main"><section class="hero"><div class="hero-inner"><div class="hero-copy"><h1>Buy. Sell.<br>Trade. Trust.</h1><p>Coinbase is the most trusted¹ crypto exchange to buy, sell, and manage crypto. Canadian users can now add cash for free with Interac e-Transfer and Electronic Funds Transfer (EFT), or buy directly with PayPal.</p><a class="blue-button" href="https://www.coinbase.com/en-ca/signup">Sign up</a></div><div class="hero-media"><img src="coinbase-assets/hero.avif" alt="Coinbase app and Canadian crypto graphic"></div></div></section>
__USDC__
__CANADA__
<section class="video"><a href="https://www.youtube.com/watch?v=7ZSYMM20BZk" aria-label="Watch Welcome to Coinbase Canada"><img src="coinbase-assets/video-poster.webp" alt="Welcome to Coinbase Canada video poster" loading="lazy"><span class="video-play" aria-hidden="true">▶</span></a></section>
__APY__
__ADVANCED__
__MEMBERSHIP__
<section class="trust"><div class="trust-header"><h2>The most trusted cryptocurrency exchange</h2><p>Millions of users trust us, and so can you. The proof is in our platform:</p></div><div class="trust-grid">__TRUST__</div></section>
<section class="disclosure"><h2>DISCLOSURE STATEMENT</h2><p>Coinbase Canada, Inc. is a Restricted Dealer in all provinces and territories of Canada and is registered with FINTRAC as an MSB (# M22815925). Trading in crypto assets may result in the loss of invested capital. The term “stablecoin” does not guarantee stable value or adequate reserves.</p><p>¹ See <a href="https://www.coinbase.com/en-ca">Coinbase’s current disclosures</a> for details about the “most trusted” claim. ² When you purchase or hold USDC, rewards are subject to eligibility and opt-out rules. Rates may change at any time; there is no contractual right to rewards. The rewards percentages on this page were observed on 2026-09-28 and are not current quotes.</p><p>* Crypto staking rewards are estimates and subject to change. Eligibility and availability depend on location, asset and account status. This page is an unofficial dated visual study; review the official Coinbase website for current terms and risk information.</p></section></main>
<footer class="footer"><div class="footer-grid">__FOOTER__</div><div class="footer-bottom"><span>© 2026 Coinbase · <a href="https://www.coinbase.com/legal/privacy">Privacy</a> · <a href="https://www.coinbase.com/legal/user_agreement">Terms &amp; Conditions</a></span><span>Canada · English</span></div></footer>
<script>
const mobileToggle=document.getElementById('menu-toggle'),mobilePanel=document.getElementById('mobile-panel'),desktopMenu=document.getElementById('desktop-menu');
function closeMenus(){mobilePanel.classList.remove('open');desktopMenu.classList.remove('open');mobileToggle.setAttribute('aria-expanded','false');mobileToggle.setAttribute('aria-label','Open menu');document.body.style.overflow=''}
mobileToggle.addEventListener('click',()=>{const open=!mobilePanel.classList.contains('open');closeMenus();mobilePanel.classList.toggle('open',open);mobileToggle.setAttribute('aria-expanded',String(open));mobileToggle.setAttribute('aria-label',open?'Close menu':'Open menu');document.body.style.overflow=open?'hidden':''});
document.querySelectorAll('[data-menu]').forEach(button=>button.addEventListener('click',()=>{const open=!desktopMenu.classList.contains('open');closeMenus();desktopMenu.classList.toggle('open',open)}));
document.addEventListener('keydown',event=>{if(event.key==='Escape')closeMenus()});document.addEventListener('click',event=>{if(!event.target.closest('.header')&&!event.target.closest('.mobile-panel'))closeMenus()});
document.querySelectorAll('.mobile-panel a,.desktop-menu a').forEach(link=>link.addEventListener('click',closeMenus));
</script></body></html>'''
    html = (html.replace('__USDC__', feature('usdc', 'Earn more on USDC', 'usdc.avif',
                 'USDC rewards Coinbase app graphic', USDC, 'https://www.coinbase.com/en-ca/signup',
                 'Sign up', note='Rates shown were observed 2026-09-28 and may change.'))
            .replace('__CANADA__', feature('canada', 'Built for Canada 🇨🇦', 'canada-phone.svg',
                 'Coinbase Canada payment method phone screen', CANADA,
                 'https://www.coinbase.com/en-ca/signup', 'Sign up', reverse=True))
            .replace('__APY__', feature('apy', 'Earn up to 10% APY on your crypto', 'apy-coins.webp',
                 'Coinbase graphic of crypto assets', (), 'https://www.coinbase.com/en-ca/earn',
                 'Learn more', shaded=True, intro='Put your crypto to work and earn rewards*',
                 note='Up to 10% APY was observed 2026-09-28; the estimated rate is subject to change.'))
            .replace('__ADVANCED__', feature('advanced', 'Get lower, volume-based pricing with Advanced Trade',
                 'advanced-trade.webp', 'Coinbase Advanced Trade app screen', ADVANCED,
                 'https://www.coinbase.com/en-ca/advanced-trade', 'Learn more', reverse=True))
            .replace('__MEMBERSHIP__', feature('membership', 'Get more out of crypto with one membership',
                 'coinbase-one.webp', 'Coinbase One Canada membership graphic', (),
                 'https://www.coinbase.com/en-ca/one', 'Claim your free trial', shaded=True,
                 intro='Zero trading fees, boosted staking rewards, priority support, and more.'))
            .replace('__TRUST__', trust_cards())
            .replace('__FOOTER__', footer_columns()))
    target = ROOT / 'coinbase.html'
    target.write_text(html)
    print(f'Wrote {target.name} ({len(html):,} characters)')


if __name__ == '__main__':
    main()
