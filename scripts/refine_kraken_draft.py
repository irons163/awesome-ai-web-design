#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build a dated, source-backed Kraken Canada homepage study."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1] / '.stitch-work' / 'current-official'
ASSETS = 'kraken-assets/'

PRODUCTS = (
    {
        'class': 'pro', 'logo': 'pro-logo.svg',
        'title': 'The command center for active traders',
        'description': 'Trade with leverage, deep liquidity, and fast execution across 600+ crypto pairs and 11,000+ stocks and ETFs. Web, mobile app, and API.',
        'cta': 'Sign up now', 'href': 'https://pro.kraken.com/app/home',
        'media': 'pro-terminal.webp', 'alt': 'Kraken Pro trading terminal',
    },
    {
        'class': 'consumer', 'logo': 'consumer-logo.svg',
        'title': 'Crypto and stocks made easy',
        'description': 'Buy and sell BTC, ETH, XRP, TSLA, AAPL and more. Automate recurring buys. Earn APY on assets.',
        'cta': 'Get Kraken', 'href': 'https://www.kraken.com/kraken-app',
        'media': 'consumer-image.webp', 'alt': 'Kraken app interface',
    },
    {
        'class': 'wallet', 'logo': 'wallet-logo.svg',
        'title': 'Secure your crypto with self custody',
        'description': 'Deposit, earn, and trade across the full breadth of DeFi on web and mobile',
        'cta': 'Try Wallet', 'href': 'https://www.kraken.com/wallet',
        'media': 'wallet-image.webp', 'alt': 'Kraken Wallet app screens',
    },
    {
        'class': 'krak', 'logo': 'krak-logo.svg',
        'title': 'The global money app',
        'description': 'Spend your crypto or cash at 80M+ merchants worldwide. Earn APY on your balance. Send anywhere in the world instantly, with no fees.',
        'cta': 'Open your free account', 'href': 'https://www.kraken.com/krak',
        'media': 'krak-card-wide.webp', 'alt': 'Krak payment cards',
    },
)

MARKETS = {
    'crypto': [
        ('btc', 'Bitcoin', 'BTC', '$84,410.00', '+0.10%', '$1.70T', 'https://www.kraken.com/prices/bitcoin'),
        ('eth', 'Ethereum', 'ETH', '$2,683.03', '-0.45%', '$327.61B', 'https://www.kraken.com/prices/ethereum'),
        ('usdt', 'Tether', 'USDT', '$1.00', '0.00%', '$183.78B', 'https://www.kraken.com/prices/tether'),
        ('bnb', 'BNB', 'BNB', '$780.82', '+1.03%', '$103.98B', 'https://www.kraken.com/prices/bnb'),
        ('xrp', 'XRP', 'XRP', '$1.52', '+0.22%', '$95.67B', 'https://www.kraken.com/prices/xrp'),
        ('usdc', 'USDC', 'USDC', '$1.00', '-0.01%', '$75.14B', 'https://www.kraken.com/prices/usdc'),
    ],
    'spot': [
        ('btc', 'BTC/USD', 'Bitcoin', '$84,457.00', '+0.18%', '$1.70T', 'https://pro.kraken.com/app/trade/btc-usd'),
        ('eth', 'ETH/USD', 'Ethereum', '$2,683.72', '-0.36%', '$327.64B', 'https://pro.kraken.com/app/trade/eth-usd'),
        ('sol', 'SOL/USD', 'Solana', '$122.35', '+1.31%', '$71.91B', 'https://pro.kraken.com/app/trade/sol-usd'),
        ('ltc', 'LTC/USD', 'Litecoin', '$70.46', '-1.89%', '$5.47B', 'https://pro.kraken.com/app/trade/ltc-usd'),
        ('usdt', 'USDT/USD', 'Tether', '$1.00', '-0.0066%', '$183.78B', 'https://pro.kraken.com/app/trade/usdt-usd'),
        ('xrp', 'XRP/USD', 'XRP', '$1.52', '+0.40%', '$95.73B', 'https://pro.kraken.com/app/trade/xrp-usd'),
    ],
    'futures': [
        ('btc', 'BTC Perp 100x', 'Bitcoin', '$84,221.00', '-0.080%', '$270.32M', 'https://pro.kraken.com/app/trade/pfxbtusd-usd'),
        ('eth', 'ETH Perp 100x', 'Ethereum', '$2,675.70', '-0.64%', '$82.48M', 'https://pro.kraken.com/app/trade/pfethusd-usd'),
        ('xrp', 'XRP Perp 50x', 'XRP', '$1.52', '-0.11%', '$81.30M', 'https://pro.kraken.com/app/trade/pfxrpusd-usd'),
        ('sol', 'SOL Perp 100x', 'Solana', '$121.76', '+0.79%', '$63.70M', 'https://pro.kraken.com/app/trade/pfsolusd-usd'),
        ('zec', 'ZEC Perp 25x', 'Zcash', '$1,572.60', '-4.40%', '$33.95M', 'https://pro.kraken.com/app/trade/pfzecusd-usd'),
        ('near', 'NEAR Perp 50x', 'NEAR Protocol', '$5.34', '+5.44%', '$20.61M', 'https://pro.kraken.com/app/trade/pfnearusd-usd'),
    ],
}

FOOTER = (
    ('Features', ('Buy Crypto', 'https://www.kraken.com/buy'), ('Sell Crypto', 'https://www.kraken.com/sell'),
     ('Margin Trading', 'https://www.kraken.com/features/margin-trading'), ('Staking Rewards', 'https://www.kraken.com/features/staking')),
    ('About Kraken', ('Kraken Security', 'https://www.kraken.com/features/security'),
     ('Kraken Careers', 'https://www.kraken.com/careers'), ('Kraken Blog', 'https://blog.kraken.com/'),
     ('Support Center', 'https://support.kraken.com/hc/en-us')),
    ('Crypto Prices', ('Bitcoin Price', 'https://www.kraken.com/prices/bitcoin'),
     ('Ethereum Price', 'https://www.kraken.com/prices/ethereum'),
     ('Solana Price', 'https://www.kraken.com/prices/solana'),
     ('All Prices', 'https://www.kraken.com/prices')),
    ('Convert Crypto', ('BTC to USD', 'https://www.kraken.com/convert/btc/usd'),
     ('ETH to USD', 'https://www.kraken.com/convert/eth/usd'),
     ('XRP to USD', 'https://www.kraken.com/convert/xrp/usd')),
)


def card(item: dict[str, str]) -> str:
    css = item['class']
    return (
        f'<section class="product-card {css}" id="{css}">'
        '<div class="product-copy">'
        f'<img class="product-logo" src="{ASSETS}{item["logo"]}" alt="">'
        f'<h2>{escape(item["title"])}</h2><p>{escape(item["description"])}</p>'
        f'<a class="card-action" href="{escape(item["href"])}">{escape(item["cta"])}</a>'
        '</div>'
        f'<img class="product-media" src="{ASSETS}{item["media"]}" '
        f'alt="{escape(item["alt"])}" loading="lazy">'
        '</section>'
    )


def footer_group(group: tuple) -> str:
    heading, *links = group
    return '<div class="footer-column"><h3>' + escape(heading) + '</h3>' + ''.join(
        f'<a href="{escape(url)}">{escape(text)}</a>' for text, url in links
    ) + '</div>'


def main() -> None:
    page = r'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Kraken homepage study · Awesome AI Web Design</title>
<meta name="description" content="Unofficial dated study of Kraken's current public Canada homepage.">
<style>
@font-face{font-family:KrakenBrand;src:url(kraken-assets/Kraken-Brand-Regular.otf) format('opentype');font-weight:400;font-display:swap}
@font-face{font-family:KrakenBrand;src:url(kraken-assets/Kraken-Brand-Bold.otf) format('opentype');font-weight:700;font-display:swap}
@font-face{font-family:KrakenProduct;src:url(kraken-assets/Kraken-Product-Regular.woff2) format('woff2');font-weight:400;font-display:swap}
@font-face{font-family:KrakenProduct;src:url(kraken-assets/Kraken-Product-Medium.woff2) format('woff2');font-weight:500;font-display:swap}
@font-face{font-family:KrakenProduct;src:url(kraken-assets/Kraken-Product-SemiBold.woff2) format('woff2');font-weight:600;font-display:swap}
:root{--paper:#f6f5f9;--ink:#101114;--purple:#7132f5;--muted:#686b82;--border:#dedee5}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.45 KrakenProduct,'Helvetica Neue',Arial,sans-serif}button,input{font:inherit}button{cursor:pointer}a{color:inherit;text-decoration:none}img{display:block;max-width:100%}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid var(--purple);outline-offset:2px}
.site-header{height:64px;position:fixed;z-index:50;inset:0 0 auto;background:#fff;display:flex;align-items:center;padding:0 18px;gap:32px}.brand-link{display:block;flex:none}.brand-link img{width:143px;height:auto}.desktop-nav,.header-actions{display:flex;align-items:center;gap:28px}.desktop-nav a{font-size:14px;white-space:nowrap}.desktop-nav a:hover,.footer a:hover{color:var(--purple)}.header-actions{margin-left:auto;gap:10px}.country,.search-button,.login{border:0;background:#f5f4f8;border-radius:12px;min-height:36px;padding:0 13px;font-size:14px}.country{display:flex;align-items:center;gap:8px}.country span{font-size:18px}.search-button{display:flex;align-items:center;gap:12px;color:#686b82}.search-button kbd{background:#ecebf1;padding:3px 6px;border-radius:6px;font-size:12px}.login{background:#eee7ff;color:#6c36d9}.signup{border-radius:12px;background:var(--purple);color:#fff;padding:10px 16px;font-size:14px;font-weight:600;white-space:nowrap}.signup:hover,.purple:hover{background:#5b1ecf}.mobile-search,.menu-toggle{display:none}.mobile-menu{display:none}
main{padding-top:64px}.hero{height:456px;text-align:center;padding:39px 16px 0}.hero h1{font:400 48px/1.17 KrakenBrand,'IBM Plex Sans',Arial,sans-serif;letter-spacing:-1px;margin:0}.hero .subtitle{font:400 24px/1.3 KrakenBrand,'IBM Plex Sans',Arial,sans-serif;margin:18px 0 30px}.signup-row{display:flex;gap:8px;width:min(436px,100%);height:48px;margin:auto}.signup-row input{border:0;border-radius:12px;background:#ecebf1;padding:0 13px;flex:1;min-width:0;font-size:14px}.purple{display:inline-flex;align-items:center;justify-content:center;background:var(--purple);border:0;color:#fff;border-radius:12px;padding:0 18px;font-weight:600;white-space:nowrap}.separator{display:flex;align-items:center;gap:12px;color:#9497a9;font-size:12px;width:min(436px,100%);margin:18px auto 13px}.separator:before,.separator:after{content:'';height:1px;background:#e5e4e8;flex:1}.socials{display:flex;justify-content:center;gap:12px}.socials span{width:56px;height:56px;border:1px solid #929199;border-radius:50%;background:#fff;display:grid;place-items:center}.socials img{width:25px;height:25px}.hero-stats{display:flex;justify-content:center;gap:54px;margin:37px auto 0}.hero-stats>div{min-width:155px;display:grid;gap:0}.hero-stats strong{font:700 24px/1.2 KrakenBrand,Arial,sans-serif}.hero-stats img{height:22px;width:auto;object-fit:contain;margin:auto}.hero-stats small{color:#9497a9;font-size:12px}
.products{padding:0 16px}.product-card{height:694px;border-radius:20px;overflow:hidden;position:relative;margin-bottom:16px;text-align:center;color:#fff;background:#100b1c}.product-card.pro{background:radial-gradient(circle at 20% 0%,#2b1855 0,#130b27 45%,#08050f 100%)}.product-card.consumer{background:#111}.product-card.wallet{background:radial-gradient(circle at 50% 75%,#353535 0,#171717 45%,#111 80%)}.product-card.krak{height:637px;background:radial-gradient(circle at 9% 15%,#5c2928 0,#23151b 50%,#101015 100%)}.product-copy{position:relative;z-index:2;padding:55px 24px 0;display:flex;flex-direction:column;align-items:center}.product-logo{height:27px;width:auto;max-width:150px;object-fit:contain;margin-bottom:15px}.product-card h2{font:400 36px/1.22 KrakenBrand,Arial,sans-serif;letter-spacing:-.5px;margin:0}.product-card p{font:400 20px/1.4 KrakenProduct,Arial,sans-serif;margin:13px auto 22px;max-width:690px}.card-action{min-height:52px;padding:0 24px;display:inline-flex;align-items:center;justify-content:center;background:#fff;color:#101114;border-radius:12px;font-weight:600}.pro .card-action{background:var(--purple);color:#fff}.product-media{position:absolute;left:50%;transform:translateX(-50%);width:min(1100px,89%);height:auto;top:344px}.consumer .product-media{width:min(670px,80%);top:376px}.wallet .product-media{width:min(1117px,90%);top:376px}.krak .product-media{width:min(970px,86%);top:350px}
.promo-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;padding:56px 16px 0}.promo{height:570px;border-radius:20px;background:radial-gradient(circle at 15% 5%,#2b1d45,#100b19 60%);color:#fff;overflow:hidden;position:relative;padding:32px 40px}.promo.leverage{background:#0c0718}.promo h2{font:400 36px/1.22 KrakenBrand,Arial,sans-serif;margin:0 0 12px}.promo p{font-size:18px;max-width:460px;margin:0 0 18px}.promo a{display:inline-block;background:#fff;color:#101114;border-radius:10px;padding:14px 20px;font-weight:600}.terminal{margin-top:25px;padding:22px;color:#c9bddc;background:#151020;border-radius:12px;font:13px/1.55 ui-monospace,monospace;white-space:pre-wrap;box-shadow:0 20px 60px #0005}.leverage img{width:100%;height:310px;object-fit:contain;position:absolute;bottom:0;left:0}
.markets{padding:86px 16px 82px;text-align:center}.markets h2,.first-move h2{font:400 clamp(36px,5vw,56px)/1.12 KrakenBrand,Arial,sans-serif;letter-spacing:-1px;margin:0}.tabs{display:flex;justify-content:center;gap:6px;margin:34px auto 25px}.tabs button{border:0;background:transparent;padding:12px 20px;border-radius:24px;font-size:20px;font-weight:500}.tabs button[aria-selected=true]{background:#fff;box-shadow:0 1px 7px #0001}.snapshot-note{font-size:12px;color:#686b82;margin:0 0 15px}.market-panel{width:min(830px,100%);margin:auto;background:#fff;border:1px solid #d6d5dc;border-radius:20px;padding:20px 48px 22px;text-align:left}.table-header,.market-row{display:grid;grid-template-columns:2fr 1.05fr .8fr .8fr;align-items:center;gap:16px}.table-header{font-size:13px;color:#686b82;padding:3px 0 18px;border-bottom:1px solid #ddd}.market-row{min-height:75px;border-bottom:1px solid #eee;color:#101114}.market-row:last-of-type{border:0}.asset-name{display:flex;align-items:center;gap:12px;font-weight:600}.asset-name img{width:40px;height:40px;object-fit:contain}.asset-name small{display:block;color:#686b82;font-weight:400}.positive{color:#026b3f}.negative{color:#a73455}.table-more{display:block;text-align:center;padding:17px;color:#7132f5;font-weight:500}.first-move{text-align:center;padding:40px 16px 100px}.first-move img{width:145px;height:145px;object-fit:contain;margin:auto auto 12px}.first-move p{font:400 20px/1.4 KrakenProduct,Arial,sans-serif;margin:20px auto 36px}.first-move .purple{height:52px}
.disclaimers{padding:15px 16px 34px;color:#686b82;font-size:12px;line-height:1.4}.disclaimers p{margin:0 0 15px}.disclaimers a{color:#7132f5}.footer{background:#fff;padding:40px 16px 70px}.footer-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:32px}.footer-column{display:flex;flex-direction:column;gap:13px}.footer h3{font-size:14px;margin:0 0 4px}.footer a{font-size:14px;color:#686b82}.footer-bottom{border-top:1px solid #e5e4e8;margin-top:45px;padding-top:25px;font-size:12px;color:#686b82}.footer-bottom a{font-size:12px;color:#686b82}
@media(max-width:800px){.site-header{gap:12px;padding:0 16px}.brand-link img{width:143px}.desktop-nav,.country,.search-button,.login{display:none}.header-actions{gap:10px}.mobile-search,.menu-toggle{display:grid;place-items:center;width:30px;height:36px;border:0;background:transparent;font-size:24px}.menu-toggle{font-size:22px}.signup{padding:9px 14px}.mobile-menu{display:none;position:fixed;z-index:49;top:64px;bottom:0;left:0;right:0;background:#fff;padding:0 16px 80px;overflow:auto}.mobile-menu.open{display:block}.menu-row{display:flex;align-items:center;justify-content:space-between;min-height:57px;border-bottom:1px solid #ddd;font-size:16px}.menu-sub{display:none;padding:12px 0}.menu-sub.open{display:grid;gap:18px}.menu-sub a{padding:6px 12px}.menu-bottom{position:sticky;bottom:-80px;background:#fff;display:flex;gap:14px;padding:16px 0 32px;margin-top:40px}.menu-bottom a{flex:1;text-align:center;border-radius:12px;padding:11px}.menu-bottom a:first-child{background:#eee7ff;color:#7132f5}.menu-bottom a:last-child{background:#7132f5;color:#fff}
.hero{height:576px;padding:28px 25px 0}.hero h1{font-size:32px;line-height:40px;letter-spacing:-.3px;max-width:290px;margin:auto}.hero .subtitle{font-size:18px;line-height:26px;margin:19px auto 25px;max-width:330px}.signup-row{display:flex;flex-direction:column;width:300px;height:auto;gap:8px}.signup-row input{flex:none;height:48px}.signup-row .purple{height:48px}.separator{width:300px;margin:18px auto 12px}.socials span{width:56px;height:56px}.hero-stats{display:grid;grid-template-columns:1fr 1fr;gap:18px 8px;margin:30px auto 0;max-width:310px}.hero-stats>div{min-width:0}.hero-stats>div:last-child{grid-column:1/-1}.hero-stats strong{font-size:22px}.hero-stats small{font-size:12px}
.products{padding:0 8px}.product-card{height:554px;margin-bottom:8px;border-radius:20px}.product-card.pro{height:570px}.product-card.wallet{height:446px}.product-card.krak{height:500px}.product-copy{padding:52px 20px 0}.product-logo{height:21px;margin-bottom:14px}.product-card h2{font-size:24px;line-height:32px;max-width:330px}.product-card p{font-size:18px;line-height:26px;margin:13px auto 22px;max-width:330px}.card-action{height:52px;min-height:0;padding:0 20px}.product-media{top:auto;bottom:-35px;width:90%}.pro .product-media{width:90%;bottom:-25px}.consumer .product-media{width:90%;top:auto;bottom:-50px}.wallet .product-media{width:100%;top:auto;bottom:-5px}.krak .product-media{width:92%;top:auto;bottom:-15px}
.promo-grid{display:grid;grid-template-columns:1fr;padding:8px 8px 0;gap:8px}.promo{height:520px;padding:48px 20px;text-align:center}.promo h2{font-size:24px;line-height:32px}.promo p{font-size:18px}.terminal{text-align:left;font-size:11px}.promo.leverage{height:500px}.leverage img{height:250px}.markets{padding:70px 16px}.markets h2,.first-move h2{font-size:36px;line-height:1.15}.tabs{gap:0}.tabs button{padding:10px 12px;font-size:16px}.market-panel{padding:12px 20px}.table-header,.market-row{grid-template-columns:1fr auto;gap:10px}.table-header span:nth-child(2),.table-header span:nth-child(4),.market-row .price,.market-row .cap{display:none}.market-row{min-height:90px}.market-row .change{text-align:right}.asset-name img{width:34px;height:34px}.first-move{padding:30px 20px 90px}.first-move img{width:100px;height:100px}.first-move p{font-size:18px}.footer-grid{grid-template-columns:1fr 1fr;gap:30px 18px}.disclaimers{padding-top:24px}
}
@media(max-width:350px){.brand-link img{width:120px}.header-actions{gap:4px}.signup-row,.separator{width:100%}.hero{padding-inline:16px}.product-card p{font-size:16px}}
</style></head><body>
<header class="site-header"><a class="brand-link" href="https://www.kraken.com/"><img src="kraken-assets/wordmark.svg" alt="Kraken by Payward"></a><nav class="desktop-nav" aria-label="Main navigation"><a href="https://www.kraken.com/kraken-app">Individuals</a><a href="https://www.kraken.com/institutions">Businesses</a><a href="https://www.kraken.com/vip">VIP</a><a href="https://www.kraken.com/affiliate">Affiliates</a><a href="#markets">Markets</a><a href="https://www.kraken.com/why-kraken">About</a></nav><div class="header-actions"><span class="country"><span aria-hidden="true">🇨🇦</span>EN</span><a class="search-button" href="https://www.kraken.com/search">⌕ <span>Search</span> <kbd>/</kbd></a><a class="login" href="https://id.kraken.com/sign-in">Log in</a><a class="signup" href="https://www.kraken.com/sign-up">Sign up</a><a class="mobile-search" href="https://www.kraken.com/search" aria-label="Search">⌕</a><button class="menu-toggle" id="menu-toggle" aria-label="Open menu" aria-expanded="false">☰</button></div></header>
<div class="mobile-menu" id="mobile-menu"><button class="menu-row" data-sub="individuals" aria-expanded="false">Individuals <span>›</span></button><div class="menu-sub" id="individuals"><a href="https://www.kraken.com/pro">Kraken Pro</a><a href="https://www.kraken.com/kraken-app">Kraken</a><a href="https://www.kraken.com/wallet">Kraken Wallet</a><a href="https://www.kraken.com/kraken-cli">Kraken CLI</a></div><button class="menu-row" data-sub="businesses" aria-expanded="false">Businesses <span>›</span></button><div class="menu-sub" id="businesses"><a href="https://www.kraken.com/institutions">Kraken Institutional</a><a href="https://www.kraken.com/institutions/custody">Custody</a><a href="https://www.kraken.com/features/api-trading">API Trading</a></div><a class="menu-row" href="https://www.kraken.com/vip">VIP</a><a class="menu-row" href="https://www.kraken.com/affiliate">Affiliates</a><a class="menu-row" href="#markets">Markets <span>›</span></a><a class="menu-row" href="https://www.kraken.com/why-kraken">About <span>›</span></a><div class="menu-bottom"><a href="https://id.kraken.com/sign-in">Log in</a><a href="https://www.kraken.com/sign-up">Sign up</a></div></div>
<main><section class="hero"><h1>Own the power of your money</h1><p class="subtitle">Crypto, stocks, futures, and more — trusted by millions worldwide</p><div class="signup-row"><input type="email" placeholder="satoshi@email.com" aria-label="Email address for Kraken"><a class="purple" href="https://www.kraken.com/sign-up">Try Kraken</a></div><div class="separator">or sign up with</div><div class="socials" aria-label="Sign-in options"><span><img src="kraken-assets/apple-signin.svg" alt="Apple"></span><span><img src="kraken-assets/google-signin.svg" alt="Google"></span></div><div class="hero-stats"><div><strong>Since 2011</strong><small>Powering secure markets</small></div><div><strong>$2T+</strong><small>Total transaction volume</small></div><div><img src="kraken-assets/forbes.svg" alt="Forbes"><small>Most popular crypto exchange 2026</small></div></div></section>
<div class="products">__PRODUCTS__</div>
<div class="promo-grid"><section class="promo cli"><h2>Your agent can trade now</h2><p>Kraken CLI for AI agents and global markets.</p><a href="https://www.kraken.com/kraken-cli">Install Kraken CLI</a><pre class="terminal">$ kraken paper reset --balance 1200 --currency USD
Mode       [PAPER] Simulated Trading
Balance    1200.00 USD
$ kraken paper status
BTC        0.00142000
USD        1100.35</pre></section><section class="promo leverage"><h2>Up to 20x leverage</h2><p>No expiry. No forced rolls. Trade on your schedule.</p><a href="https://www.kraken.com/features/margin-trading">Learn more</a><img src="kraken-assets/leverage.webp" alt="Kraken 20x leverage visual" loading="lazy"></section></div>
<section class="markets" id="markets"><h2>Explore every market</h2><div class="tabs" role="tablist" aria-label="Market types"><button role="tab" data-market="crypto" aria-selected="true">Crypto</button><button role="tab" data-market="spot" aria-selected="false">Spot / Margin</button><button role="tab" data-market="futures" aria-selected="false">Futures</button></div><p class="snapshot-note">Market values captured 2026-09-28; illustrative snapshot, not live prices.</p><div class="market-panel" role="tabpanel"><div class="table-header"><span>ASSET</span><span>PRICE</span><span>24H%</span><span id="last-heading">M. CAP</span></div><div id="market-rows"></div><a class="table-more" id="market-more" href="https://www.kraken.com/prices">View all cryptocurrencies →</a></div></section>
<section class="first-move"><img src="kraken-assets/beast.webp" alt="" loading="lazy"><h2>Make your first move</h2><p>Create your free account and get started in minutes.</p><a class="purple" href="https://www.kraken.com/sign-up">Try Kraken</a></section>
<div class="disclaimers"><p>Availability of margin trading services is subject to <a href="https://support.kraken.com/hc/en-us/articles/4402532394260-Client-eligibility-for-margin-trading-services-">certain limitations and eligibility criteria</a>. Trading using margin involves an element of risk and may not be suitable for everyone. Read <a href="https://www.kraken.com/legal">Kraken's Margin Disclosure Statement</a> to learn more.</p><p>Trading derivatives and other financial instruments, including leveraged financial instruments, involves significant risks and is not appropriate for all investors. See our <a href="https://support.kraken.com/hc/en-us/articles/360022629052-Risk-Disclosure">Risk Disclosure</a> to learn more.</p><p>Geographic restrictions apply. Projected annual rate is an estimate based on the average staking rewards accrued over the past period, before commission, and is subject to change. Staking involves risks including no guarantee of rewards, potential loss from slashing or hacks, and depreciation in the value of assets while staked. Please refer to Kraken's <a href="https://www.kraken.com/legal">Terms of Service</a> for additional information.</p><p>Kraken Equities is currently available in the U.S. only; may not be available in all states. Brokerage services are provided by Kraken Securities LLC (“Kraken Securities”), member FINRA/SIPC, a wholly owned subsidiary of Payward, Inc. (“Kraken”).</p></div></main>
<footer class="footer"><div class="footer-grid">__FOOTER__</div><div class="footer-bottom"><p>© 2011–2026 Payward, Inc. · <a href="https://www.kraken.com/privacy-hub">Privacy Hub</a> · <a href="https://www.kraken.com/legal">Terms of Service</a> · <a href="https://www.kraken.com/compliance">Compliance Hub</a></p><p>These materials are for general information purposes only and are not investment or financial product advice. Unofficial dated visual study.</p></div></footer>
<script>
const markets=__MARKETS__;const base='kraken-assets/';
function renderMarket(kind){const rows=document.getElementById('market-rows');rows.replaceChildren();for(const [icon,name,ticker,price,change,cap,url] of markets[kind]){const row=document.createElement('a');row.className='market-row';row.href=url;const asset=document.createElement('span');asset.className='asset-name';const img=document.createElement('img');img.src=base+icon+'.webp';img.alt='';const title=document.createElement('span');title.textContent=name;const small=document.createElement('small');small.textContent=ticker;title.append(small);asset.append(img,title);const p=document.createElement('span');p.className='price';p.textContent=price;const c=document.createElement('span');c.className='change '+(change.startsWith('-')?'negative':'positive');c.textContent=change;const m=document.createElement('span');m.className='cap';m.textContent=cap;row.append(asset,p,c,m);rows.append(row)}document.querySelectorAll('[data-market]').forEach(t=>t.setAttribute('aria-selected',String(t.dataset.market===kind)));document.getElementById('last-heading').textContent=kind==='futures'?'VOLUME':'M. CAP';const more=document.getElementById('market-more');more.href=kind==='crypto'?'https://www.kraken.com/prices':kind==='spot'?'https://pro.kraken.com/app/markets/crypto':'https://pro.kraken.com/app/trade/futures-btc-usd-perp';more.textContent=kind==='crypto'?'View all cryptocurrencies →':'View all →'}
document.querySelectorAll('[data-market]').forEach(t=>t.addEventListener('click',()=>renderMarket(t.dataset.market)));renderMarket('crypto');
const toggle=document.getElementById('menu-toggle'),menu=document.getElementById('mobile-menu');toggle.addEventListener('click',()=>{const open=!menu.classList.contains('open');menu.classList.toggle('open',open);toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Close menu':'Open menu');toggle.textContent=open?'×':'☰';document.body.style.overflow=open?'hidden':''});document.querySelectorAll('[data-sub]').forEach(t=>t.addEventListener('click',()=>{const pane=document.getElementById(t.dataset.sub),open=!pane.classList.contains('open');pane.classList.toggle('open',open);t.setAttribute('aria-expanded',String(open))}));menu.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menu.classList.remove('open');document.body.style.overflow='';toggle.setAttribute('aria-expanded','false');toggle.textContent='☰'}));document.addEventListener('keydown',e=>{if(e.key==='Escape'){menu.classList.remove('open');document.body.style.overflow='';toggle.setAttribute('aria-expanded','false');toggle.textContent='☰'}});
</script></body></html>'''
    page = (page.replace('__PRODUCTS__', ''.join(card(item) for item in PRODUCTS))
            .replace('__FOOTER__', ''.join(footer_group(group) for group in FOOTER))
            .replace('__MARKETS__', json.dumps(MARKETS, ensure_ascii=False)))
    target = ROOT / 'kraken.html'
    target.write_text(page)
    print(f'Wrote {target.name} ({len(page):,} characters)')


if __name__ == '__main__':
    main()
