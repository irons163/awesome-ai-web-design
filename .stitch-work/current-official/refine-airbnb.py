# coding: utf-8
"""Rebuild the native Stitch Airbnb screen with observed public-page content.

The unmodified Stitch export remains beside this file. The official-page JSON
is a dated Canadian-region snapshot, not a live Airbnb data feed.
"""

import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
raw_path = ROOT / "airbnb-stitch.html"
if not raw_path.is_file():
    # The current-site Stitch generation is asynchronous. Until it yields a
    # screen, use the already preserved native Stitch export for this brand.
    raw_path = ROOT.parents[1] / "design-md/airbnb/preview.html"
assert raw_path.is_file(), "No native Airbnb Stitch export is available"
raw = raw_path.read_text()
assert "Airbnb" in raw or "HavenStay" in raw, "Unexpected native Stitch export"
ref = json.loads((ROOT / "airbnb-browser-reference.json").read_text())
assert ref["sourceUrl"].startswith("https://www.airbnb.ca/")
assert len(ref["cards"]) == 96
assert len(ref["navIcons"]) == 4
assert (ROOT / "airbnb-assets/airbnb-wordmark.svg").is_file()


def e(value):
    return html.escape(str(value or ""), quote=True)


nav = "".join(
    f'<button type="button" class="nav-tab{" selected" if i == 0 else ""}" role="tab" '
    f'aria-selected="{"true" if i == 0 else "false"}"><img src="{e(item["src"])}" alt="">'
    f'<span>{e(item["label"])}</span></button>'
    for i, item in enumerate(ref["navIcons"])
)


def category_card(item, kind):
    title = e(item["label"])
    media = f'<img src="{e(item["src"])}" alt="" loading="{"eager" if item["index"] < 7 else "lazy"}">'
    href = item["href"] or ref["sourceUrl"]
    return (f'<a class="category-card {kind}" href="{e(href)}">'
            f'<span class="category-media">{media}</span><span class="category-label">{title}</span></a>')


experience_cards = "".join(category_card(item, "experience-card") for item in ref["categories"][:7])
service_cards = "".join(category_card(item, "service-card") for item in ref["categories"][7:])


def listing_card(item):
    badge = f'<span class="card-badge">{e(item["badge"])}</span>' if item["badge"] else ""
    date = f'<span class="card-date">{e(item["date"])}</span>' if item["date"] else ""
    price = e(item["price"])
    rating = f'<span class="card-rating">★ {e(item["rating"])}</span>' if item["rating"] else ""
    stats = f'<span class="card-stats">{price}{" · " if price and rating else ""}{rating}</span>' if price or rating else ""
    return (
        '<article class="listing-card">'
        f'<a class="listing-link" href="{e(item["href"])}" target="_blank" rel="noopener noreferrer">'
        f'<span class="listing-media"><img src="{e(item["image"])}" alt="{e(item["title"])}" loading="lazy">{badge}</span>'
        f'<strong>{e(item["title"])}</strong>{date}{stats}</a>'
        f'<button type="button" class="heart" aria-label="Add to wishlist: {e(item["title"])}" aria-pressed="false">♡</button>'
        '</article>'
    )


headings = [section["title"] for section in ref["headings"][2:-2]]
assert len(headings) == 12
listing_sections = []
for index, heading in enumerate(headings):
    cards = [card for card in ref["cards"] if card["section"] == heading]
    assert len(cards) == 8, heading
    listing_sections.append(
        f'<section class="listing-section" aria-labelledby="listing-heading-{index}">'
        f'<div class="section-heading"><h2 id="listing-heading-{index}"><a href="{e(cards[0]["href"])}">'
        f'{e(heading)} <span class="heading-arrow">→</span></a></h2>'
        f'<div class="carousel-controls"><button type="button" class="carousel-previous" aria-label="Previous">‹</button>'
        f'<button type="button" class="carousel-next" aria-label="Next">›</button></div></div>'
        f'<div class="listing-track carousel-track">{"".join(listing_card(card) for card in cards)}</div></section>'
    )

footer_groups = (
    ("Support", ref["footer"][0:7]),
    ("Hosting", ref["footer"][7:17]),
    ("Airbnb", ref["footer"][17:23]),
)
footer = "".join(
    f'<div class="footer-column"><h3>{e(title)}</h3>'
    + "".join(f'<a href="{e(item["href"])}">{e(item["text"])}</a>' for item in links)
    + '</div>'
    for title, links in footer_groups
)

destinations = (
    ("Tokyo", "Vacation rentals", "https://www.airbnb.ca/tokyo-japan/stays"),
    ("Boston", "Condo rentals", "https://www.airbnb.ca/boston-ma/stays/condos"),
    ("Whistler", "Villa rentals", "https://www.airbnb.ca/whistler-canada/stays/villas"),
    ("Rome", "Condo rentals", "https://www.airbnb.ca/rome-italy/stays/condos"),
    ("Pickering", "Cottage rentals", "https://www.airbnb.ca/pickering-canada/stays/cottages"),
    ("Ucluelet", "Apartment rentals", "https://www.airbnb.ca/ucluelet-canada/stays/apartments"),
    ("Ajax", "Apartment rentals", "https://www.airbnb.ca/ajax-canada/stays/apartments"),
    ("Barcelona", "House rentals", "https://www.airbnb.ca/barcelona-spain/stays/houses"),
    ("Bowen Island", "Cabin rentals", "https://www.airbnb.ca/bowen-island-canada/stays/cabins"),
    ("New York City", "Apartment rentals", "https://www.airbnb.ca/new-york-ny/stays/apartments"),
    ("Bracebridge", "Monthly Rentals", "https://www.airbnb.ca/bracebridge-canada/stays/monthly"),
    ("Shinjuku", "Apartment rentals", "https://www.airbnb.ca/shinjuku-city-japan/stays/apartments"),
    ("London", "Pet-friendly rentals", "https://www.airbnb.ca/london-united-kingdom/stays/pet-friendly"),
    ("Oakville", "Apartment rentals", "https://www.airbnb.ca/oakville-canada/stays/apartments"),
    ("Los Angeles", "Pet-friendly rentals", "https://www.airbnb.ca/los-angeles-ca/stays/pet-friendly"),
    ("Vancouver Island", "Condo rentals", "https://www.airbnb.ca/vancouver-island-canada/stays/condos"),
    ("Montreal", "Vacation rentals", "https://www.airbnb.ca/montreal-canada/stays"),
)
inspiration = "".join(
    f'<a href="{e(url)}"><strong>{e(place)}</strong><span>{e(category)}</span></a>'
    for place, category, url in destinations
)

page = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Airbnb | Vacation rentals, cabins, beach houses, & more</title>
<meta name="description" content="Independent visual study of the public Airbnb Canada homepage at a specific date.">
<style>
@font-face{font-family:AirbnbCereal;src:url("__FONT_URL__") format("woff2");font-style:normal;font-weight:100 900;font-display:swap}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;color:#222;background:#fff;font-family:AirbnbCereal,Circular,-apple-system,system-ui,sans-serif;font-size:14px}button,input{font:inherit}button{cursor:pointer}a{color:inherit;text-decoration:none}img{display:block}h1,h2,h3,p{margin:0}
.site-header{position:sticky;top:0;z-index:20;height:200px;background:linear-gradient(#fff 38%,#f8f8f8 100%);border-bottom:1px solid #e9e9e9;transition:height .18s ease}.site-header.compact{height:80px;background:#fff}.brand{position:absolute;top:24px;left:32px}.brand img{width:102px;height:32px}.brand .small-logo{display:none}.main-nav{position:absolute;top:3px;left:50%;transform:translateX(-50%);display:flex;align-items:center;gap:20px;height:71px}.nav-tab{border:0;background:none;display:flex;align-items:center;gap:0;height:69px;padding:0 0 2px;color:#6a6a6a;position:relative;white-space:nowrap}.nav-tab img{width:72px;height:72px;object-fit:contain;margin-right:-10px}.nav-tab span{font-size:14px;font-weight:500}.nav-tab.selected{color:#222}.nav-tab.selected:after{content:"";height:3px;background:#222;position:absolute;bottom:3px;left:18px;right:0;border-radius:2px}.header-actions{position:absolute;right:32px;top:21px;display:flex;gap:12px;align-items:center}.header-actions .host{border:0;background:none;padding:10px 8px;font-weight:600;font-size:14px}.round-action{width:42px;height:42px;border:0;background:#f7f7f7;border-radius:50%;font-size:21px;display:grid;place-items:center}.round-action.menu{font-size:19px}
.search-form{position:absolute;top:95px;left:50%;transform:translateX(-50%);width:850px;height:65px;background:white;border:1px solid #ddd;border-radius:999px;box-shadow:0 4px 15px #00000010;display:flex;align-items:center}.search-field{height:39px;padding:0 32px;display:flex;flex-direction:column;justify-content:center;border-right:1px solid #ddd}.search-field.where{width:281px}.search-field.when{width:288px}.search-field.who{flex:1;border-right:0;padding-left:26px}.search-field label,.search-field b{font-size:12px;font-weight:600;line-height:17px}.search-field input{border:0;background:none;outline:0;font-size:14px;color:#222;min-width:0;padding:0;line-height:19px}.search-field input::placeholder{color:#6a6a6a}.search-field button{border:0;background:none;text-align:left;color:#6a6a6a;padding:0;font-size:14px;line-height:19px}.search-submit{width:48px;height:48px;flex:none;border:0;border-radius:50%;background:#db0d53;color:#fff;font-size:26px;margin-right:8px;line-height:1}.compact-search{display:none;position:absolute;top:17px;left:50%;transform:translateX(-50%);border:1px solid #ddd;border-radius:999px;height:47px;background:#fff;box-shadow:0 2px 8px #00000016;align-items:center;padding-left:20px;white-space:nowrap;font-size:14px;font-weight:600}.compact-search img{width:34px;height:34px;object-fit:contain;margin-right:2px}.compact-search span{padding:0 16px;border-right:1px solid #ddd}.compact-search span:last-of-type{border:0}.compact-search .small-search{border:0;border-radius:50%;height:32px;width:32px;background:#db0d53;color:#fff;font-size:18px;margin-right:4px}.compact .main-nav,.compact .search-form{display:none}.compact .compact-search{display:flex}
.feed{overflow:hidden}.category-section,.listing-section{padding:34px 32px 0;position:relative}.experience-section{height:267px}.service-section{height:280px}.listing-section{height:343px}.section-heading{display:flex;align-items:center;justify-content:space-between;height:24px}.section-heading h2{font-size:20px;line-height:24px;letter-spacing:-.015em;font-weight:600}.section-heading a{display:flex;align-items:center;gap:9px}.heading-arrow{background:#f7f7f7;width:30px;height:30px;border-radius:50%;display:inline-grid;place-items:center;font-size:21px;font-weight:400}.carousel-controls{display:flex;gap:8px;align-items:center}.carousel-controls button{border:0;background:#f7f7f7;border-radius:50%;width:27px;height:27px;font-size:21px;line-height:20px}.carousel-controls button:disabled{opacity:.3;cursor:default}.carousel-track{display:flex;gap:10px;overflow-x:auto;overflow-y:hidden;scrollbar-width:none;scroll-snap-type:x mandatory;scroll-behavior:smooth}.carousel-track::-webkit-scrollbar{display:none}.category-track{margin-top:20px}.category-card{width:165px;flex:none;scroll-snap-align:start}.category-media{display:grid;place-items:center;width:165px;height:157px;overflow:hidden;border-radius:16px;background:#f7f7f7}.category-media img{width:100%;height:100%;object-fit:cover}.category-label{display:block;margin-top:8px;font-size:14px;font-weight:500;white-space:nowrap}.service-track{margin-top:20px}.service-card .category-media{height:165px}.service-card .category-media img{height:117px;width:117px;object-fit:contain}
.listing-track{gap:12px;margin-top:18px}.listing-card{width:193px;flex:none;position:relative;scroll-snap-align:start}.listing-link{display:block}.listing-media{position:relative;display:block;width:193px;height:183px;border-radius:17px;overflow:hidden;background:#ddd}.listing-media img{width:100%;height:100%;object-fit:cover}.card-badge{position:absolute;left:12px;top:12px;background:#fff;padding:5px 10px;border-radius:999px;font-size:11px;line-height:14px;font-weight:600;box-shadow:0 1px 4px #0002}.heart{position:absolute;top:11px;right:10px;color:#fff;text-shadow:0 0 3px #555,0 1px 3px #555;background:none;border:0;font-size:29px;line-height:27px;padding:0 2px}.heart[aria-pressed="true"]{color:#ff385c;text-shadow:0 1px 2px #555}.listing-card strong{display:block;font-size:13px;line-height:16px;font-weight:500;margin:8px 4px 2px;min-height:16px;max-height:32px;overflow:hidden}.card-date,.card-stats{display:block;margin-left:4px;color:#6a6a6a;font-size:12px;line-height:17px;white-space:nowrap}.card-rating{font-size:12px}.inspiration{background:#f7f7f7;padding:48px 32px 70px}.inspiration h2{font-size:20px;font-weight:600;line-height:24px}.inspiration-tabs{display:flex;gap:34px;margin-top:20px;border-bottom:1px solid #ddd;overflow:auto}.inspiration-tabs a{display:block;padding:0 0 12px;color:#6a6a6a;white-space:nowrap}.inspiration-tabs a:first-child{border-bottom:2px solid #222;color:#222}.destination-grid{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:28px 20px;margin-top:32px}.destination-grid a{display:flex;flex-direction:column;font-size:14px}.destination-grid strong{font-weight:500}.destination-grid span{color:#6a6a6a}.site-footer{background:#f7f7f7;padding:64px 32px 40px;border-top:1px solid #ddd}.footer-columns{display:grid;grid-template-columns:repeat(3,1fr);gap:40px}.footer-column{display:flex;flex-direction:column;gap:18px}.footer-column h3{font-size:14px;font-weight:600;margin-bottom:2px}.footer-bottom{display:flex;justify-content:space-between;border-top:1px solid #ddd;margin-top:55px;padding-top:28px;gap:20px}.footer-bottom a{margin-left:12px}.footer-locales{font-weight:500}
@media(max-width:950px){.main-nav{gap:5px}.nav-tab img{width:55px;height:55px}.nav-tab span{font-size:12px}.header-actions .host{display:none}.search-form{width:min(850px,calc(100% - 40px))}.search-field{padding-left:20px!important}.destination-grid{grid-template-columns:repeat(3,1fr)}}
@media(max-width:650px){.site-header{height:156px}.site-header.compact{height:70px}.brand{top:19px;left:20px}.brand .wide-logo{display:none}.brand .small-logo{display:block;width:30px}.main-nav{left:50%;top:0;height:56px;gap:0}.nav-tab{height:56px}.nav-tab img{width:35px;height:35px;margin-right:0}.nav-tab span{display:none}.header-actions{top:13px;right:16px;gap:6px}.round-action{width:34px;height:34px;font-size:17px}.search-form{top:75px;width:calc(100% - 32px);height:62px}.search-field{padding:0 12px!important}.search-field.where{width:45%}.search-field.when{width:27%}.search-field.who{width:24%}.search-field label,.search-field b{font-size:11px}.search-field input,.search-field button{font-size:11px}.search-submit{width:36px;height:36px;font-size:20px;margin-right:4px}.compact-search{top:13px;height:44px;left:auto;right:56px;transform:none;font-size:11px;padding-left:5px}.compact-search span{padding:0 8px}.compact-search img{display:none}.category-section,.listing-section{padding-left:16px;padding-right:16px}.category-card,.category-media{width:140px}.category-media{height:134px}.service-card .category-media{height:140px}.service-card .category-media img{width:105px;height:105px}.section-heading h2{font-size:18px}.listing-card,.listing-media{width:165px}.listing-media{height:158px}.listing-section{height:328px}.inspiration{padding:40px 16px}.destination-grid{grid-template-columns:repeat(2,1fr)}.site-footer{padding:45px 16px}.footer-columns{grid-template-columns:1fr;gap:35px}.footer-bottom{flex-direction:column}}
</style></head><body>
<header class="site-header" id="site-header"><a class="brand" href="https://www.airbnb.ca/" aria-label="Airbnb homepage"><img class="wide-logo" src="airbnb-assets/airbnb-wordmark.svg" alt="Airbnb"><img class="small-logo" src="airbnb-assets/airbnb-icon.svg" alt=""></a><nav class="main-nav" role="tablist" aria-label="Choose Airbnb category">__NAV__</nav><div class="header-actions"><button type="button" class="host" onclick="location.href='https://www.airbnb.ca/host/homes'">Become a host</button><button type="button" class="round-action" aria-label="Choose a language and currency">◎</button><button type="button" class="round-action menu" aria-label="Main navigation menu">☰</button></div>
<form class="search-form" action="https://www.airbnb.ca/s/homes" method="get"><div class="search-field where"><label for="where">Where</label><input id="where" name="query" placeholder="Search destinations"></div><div class="search-field when"><b>When</b><button type="button">Add dates</button></div><div class="search-field who"><b>Who</b><button type="button">Add guests</button></div><button type="submit" class="search-submit" aria-label="Search">⌕</button></form><div class="compact-search"><img src="__COMPACT_ICON__" alt=""><span>Anywhere</span><span>Anytime</span><span>Add guests</span><button class="small-search" aria-label="Search" type="button" onclick="document.getElementById('where').focus()">⌕</button></div></header>
<main class="feed"><section class="category-section experience-section" aria-labelledby="experiences-heading"><div class="section-heading"><h2 id="experiences-heading"><a href="https://www.airbnb.ca/s/Montreal/experiences">Explore experiences nearby <span class="heading-arrow">→</span></a></h2></div><div class="carousel-track category-track">__EXPERIENCES__</div></section>
<section class="category-section service-section" aria-labelledby="services-heading"><div class="section-heading"><h2 id="services-heading">Find services near you</h2><div class="carousel-controls"><button type="button" class="carousel-previous" aria-label="Previous">‹</button><button type="button" class="carousel-next" aria-label="Next">›</button></div></div><div class="carousel-track service-track">__SERVICES__</div></section>
__LISTINGS__
<section class="inspiration"><h2>Inspiration for future getaways</h2><nav class="inspiration-tabs" aria-label="Getaway categories"><a href="https://www.airbnb.ca/">Popular</a><a href="https://www.airbnb.ca/">Coastal</a><a href="https://www.airbnb.ca/">Islands</a><a href="https://www.airbnb.ca/">Lakes</a><a href="https://www.airbnb.ca/">Mountains</a><a href="https://www.airbnb.ca/">Outdoors</a><a href="https://www.airbnb.ca/">Things to do</a></nav><div class="destination-grid">__INSPIRATION__</div></section></main>
<footer class="site-footer"><div class="footer-columns">__FOOTER__</div><div class="footer-bottom"><div>© 2026 Airbnb, Inc. · <a href="https://www.airbnb.ca/terms/privacy_policy">Privacy</a> · <a href="https://www.airbnb.ca/terms">Terms</a></div><div class="footer-locales">◎ &nbsp; English (CA) &nbsp;&nbsp; $ CAD &nbsp;&nbsp; <a href="https://www.facebook.com/airbnb">f</a><a href="https://twitter.com/airbnb">𝕏</a><a href="https://instagram.com/airbnb">◎</a></div></div></footer>
<script>
const header=document.getElementById('site-header');const syncHeader=()=>header.classList.toggle('compact',window.scrollY>80);window.addEventListener('scroll',syncHeader,{passive:true});syncHeader();
document.querySelectorAll('.nav-tab').forEach(tab=>tab.addEventListener('click',()=>{document.querySelectorAll('.nav-tab').forEach(x=>{x.classList.remove('selected');x.setAttribute('aria-selected','false')});tab.classList.add('selected');tab.setAttribute('aria-selected','true')}));
document.querySelectorAll('.carousel-controls').forEach(controls=>{const track=controls.parentElement.nextElementSibling;controls.querySelector('.carousel-previous').addEventListener('click',()=>track.scrollBy({left:-1230,behavior:'smooth'}));controls.querySelector('.carousel-next').addEventListener('click',()=>track.scrollBy({left:1230,behavior:'smooth'}))});
document.querySelectorAll('.heart').forEach(button=>button.addEventListener('click',()=>{const active=button.getAttribute('aria-pressed')==='true';button.setAttribute('aria-pressed',String(!active));button.textContent=active?'♡':'♥'}));
</script></body></html>'''

for marker, value in {
    "__FONT_URL__": e(ref["fontUrl"]),
    "__NAV__": nav,
    "__COMPACT_ICON__": e(ref["navIcons"][1]["src"]),
    "__EXPERIENCES__": experience_cards,
    "__SERVICES__": service_cards,
    "__LISTINGS__": "\n".join(listing_sections),
    "__INSPIRATION__": inspiration,
    "__FOOTER__": footer,
}.items():
    assert page.count(marker) == 1, marker
    page = page.replace(marker, value)

assert "HavenStay" not in page
(ROOT / "airbnb.html").write_text(page)
print("airbnb.html", len(page), "bytes", len(headings), "listing sections", "seed:", raw_path)
