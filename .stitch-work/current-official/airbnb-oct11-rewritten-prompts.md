# Airbnb｜實際送出指令與後續來源校正規格

以下完整保留10月10日實際送交Google Stitch MCP的原DESKTOP指令。project `13625555706512007030`；該請求逾時且十次查詢為空，仍未取得該次輸出。後續不同390px範圍的新工作另列，不能抹除這條失敗歷史。

```text
Reconstruct the observed Airbnb Canada public homepage as a faithful independent design study. This is not an invented travel brand. Keep Airbnb branding and actual reference content.
Source: https://www.airbnb.ca/?locale=en; observed 2026-10-10T11:09:10.905Z in a public Chrome session with Only necessary cookies. Region/personalization can vary. Target this particular captured variant, not a universal homepage.
Desktop viewport 1440 x 900, devicePixelRatio 1. Full reference page height 4613 px after all lazy-loaded rows were loaded. White page, Airbnb Cereal-like sans-serif, #222 primary text, #6a6a6a muted text. Use precise actual photo URLs below.
The header is 200 px high. Wordmark at x48 y32, width102 height32. Four illustrated tabs centered at top: All, Homes, Experiences, Services. All has black 3px underline. Right: Become a host, a round outlined profile icon, a round hamburger menu. Large search pill at x295 y102 width850 height65: Where / Search destinations (width281), When / Add dates (width288), Who / Add guests, red #e00b41 circular search button at x1087 y111 48x48. Background is a subtle white-to-#f8f8f8 gradient; thin gray bottom border. At scroll the header is compact at 96 px high, logo remains x48 y32, center small search Anywhere | Anytime | Add guests and small red search.
There is no marketing hero, headline, services carousel, or experience carousel in this observed version. Start with the real listing feed at y254, left/right margins48. Seven property cards visible across desktop, each181.71px wide, gap12px, images172.625px high, 20px corner radius. Titles13px medium, dates/prices/ratings12px regular. Photos show top-left white Guest favourite pill where present, and top-right dark translucent heart with white outline. Heading visual text20px semibold line24; subtitle14px line20. First heading text starts x50 y256, subtitle y288, photos x48 y318. Next row top606.625. Preserve observed row rhythm and subtitles. Right of each row: pale circular Previous (disabled at start) and Next arrow buttons. Carousel is horizontal; no visible scrollbars.
Use semantic accessible HTML, a visually hidden h1 Airbnb homepage, genuine navigation links, keyboard focus states, horizontal carousel buttons, and local-only favorite toggles (do not create an account or booking action). Search may open the official search destination with user-entered public city/date/guest fields. Do not fake completed bookings or official affiliation.
Full listing feed, exact order and content:

SECTION Stay in Lake Kawaguchi
Subtitle: Lake near Mount Fuji with hot springs
Desktop top: 254; section height: 312.625
- Guest favourite | Villa in Fujikawaguchiko | Jan 8–10 | $826 CAD total | 4.97 out of 5 average rating | 4.97
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1643751316846284459/original/95b180e5-610c-474e-ab46-dd3465024953.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/1643751316846284459?check_in=2027-01-08&check_out=2027-01-10&photo_id=2555091093
- Guest favourite | Villa in Fujikawaguchiko | Dec 18–20 | $501 CAD total | 5.0 out of 5 average rating | 5.0
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-1157544045597144904/original/9995ee75-5f85-43cf-bd49-726302c5e79f.jpeg?im_w=960
  Link: https://www.airbnb.ca/rooms/1157544045597144904?check_in=2026-12-18&check_out=2026-12-20&photo_id=1935433831
- Home in Fujikawaguchiko | Jan 8–10 | $900 CAD total | 5.0 out of 5 average rating | 5.0
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1765851217717766105/original/4fc7fb29-f279-49da-91a8-5f0768b7669a.png?im_w=720
  Link: https://www.airbnb.ca/rooms/1765851217717766105?check_in=2027-01-08&check_out=2027-01-10&photo_id=2810445666
- Guest favourite | Room in Fujikawaguchiko | Dec 25–27 | $126 CAD total | 4.91 out of 5 average rating | 4.91
  Photo: https://a0.muscache.com/im/pictures/56879337-8c77-48d1-85c2-f7adc365240d.jpg?im_w=720
  Link: https://www.airbnb.ca/rooms/37946844?check_in=2026-12-25&check_out=2026-12-27&photo_id=1690396856
- Villa in Fujikawaguchiko | Dec 4–6 | $829 CAD total | 4.97 out of 5 average rating | 4.97
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTI5ODAyODM0MjM3OTI3ODk0MQ%3D%3D/original/af35b904-5b43-4224-a8f9-45a546076cc3.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/1298028342379278941?check_in=2026-12-04&check_out=2026-12-06&photo_id=2053633251
- Guest favourite | Home in Fujikawaguchiko | Jan 15–17 | $826 CAD total | 4.99 out of 5 average rating | 4.99
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1541201076214760918/original/c5be7b50-9904-4471-a5a1-55454ec4e4f0.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/1541201076214760918?check_in=2027-01-15&check_out=2027-01-17&photo_id=2385711402
- Guest favourite | Home in Fujikawaguchiko | Jan 8–10 | $2,739 CAD total | 4.92 out of 5 average rating | 4.92
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTQ2ODA0NDc0MTQwNTE3NDcyMw==/original/df37cf2e-95a7-425b-bd47-2ba557b0e698.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/1468044741405174723?check_in=2027-01-08&check_out=2027-01-10&photo_id=2277845846
- Guest favourite | Townhouse in Fujikawaguchiko | Jan 15–17 | $627 CAD total | 4.85 out of 5 average rating | 4.85
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1662004249160940860/original/3fc8f1e5-7f75-4985-a644-af2bfc09f587.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/1662004249160940860?check_in=2027-01-15&check_out=2027-01-17&photo_id=2589221688

SECTION Places to stay in Taitung City
Subtitle: Taiwan city on the Pacific coast
Desktop top: 606.625; section height: 296.625
- Guest favourite | Condo in 鐵花里 | Oct 16–18 | $230 CAD total | 4.97 out of 5 average rating | 4.97
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTA0NzY2MjU0Nzk1MTQxMTgzNg%3D%3D/original/ceeff414-5926-485e-ae41-a7602906f22c.jpeg?im_w=480
  Link: https://www.airbnb.ca/rooms/1047662547951411836?check_in=2026-10-16&check_out=2026-10-18&photo_id=1822250993
- Guest favourite | Room in Taitung City | Nov 6–8 | $158 CAD total | 4.97 out of 5 average rating | 4.97
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1573156596883032250/original/89973b2d-ffeb-40eb-815c-f3bfd5194802.png?im_w=480
  Link: https://www.airbnb.ca/rooms/1573156596883032250?check_in=2026-11-06&check_out=2026-11-08&photo_id=2734486045
- Guest favourite | Apartment in Taitung City | Nov 13–15 | $162 CAD total | 4.81 out of 5 average rating | 4.81
  Photo: https://a0.muscache.com/im/pictures/3b22e9b2-e9b7-4fdb-a036-12a629b8cf81.jpg?im_w=720
  Link: https://www.airbnb.ca/rooms/946739388519494023?check_in=2026-11-13&check_out=2026-11-15&photo_id=1788319157
- Guest favourite | Apartment in Taitung City | Nov 13–15 | $637 CAD total | 4.97 out of 5 average rating | 4.97
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-993162296352157724/original/b916bd51-9230-4364-ab31-bb6bf4ebe25e.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/993162296352157724?check_in=2026-11-13&check_out=2026-11-15&photo_id=1803998346
- Guest favourite | Room in Taitung City | Nov 6–8 | $188 CAD total | 4.83 out of 5 average rating | 4.83
  Photo: https://a0.muscache.com/im/pictures/22375ac8-66a0-4a0b-8680-926689b9eee5.jpg?im_w=720
  Link: https://www.airbnb.ca/rooms/14888380?check_in=2026-11-06&check_out=2026-11-08&photo_id=208212461
- Guest favourite | Room in Taitung City | Nov 6–8 | $589 CAD total | 4.94 out of 5 average rating | 4.94
  Photo: https://a0.muscache.com/im/pictures/b38a2038-b3d8-4b7f-8360-e13ecfd134c1.jpg?im_w=720
  Link: https://www.airbnb.ca/rooms/51243169?check_in=2026-11-06&check_out=2026-11-08&photo_id=1225734378
- Guest favourite | Room in Taitung City | Nov 6–8 | $136 CAD total | 4.88 out of 5 average rating | 4.88
  Photo: https://a0.muscache.com/im/pictures/7c1ad469-1951-48f2-a3ca-5427605db5ad.jpg?im_w=960
  Link: https://www.airbnb.ca/rooms/23301740?check_in=2026-11-06&check_out=2026-11-08&photo_id=1030515126
- Guest favourite | Room in Taitung City | Oct 16–18 | $60 CAD total | 4.82 out of 5 average rating | 4.82
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-678760882010269235/original/edafbd08-6664-407a-b9f1-681ed8a1a482.jpeg?im_w=960
  Link: https://www.airbnb.ca/rooms/678760882010269235?check_in=2026-10-16&check_out=2026-10-18&photo_id=1455392868

SECTION Available in Taichung City this weekend
Subtitle: Taiwan city with night markets
Desktop top: 943.25; section height: 296.625
- Guest favourite | Apartment in 忠誠里 | Oct 10–11 | $224 CAD total | 4.92 out of 5 average rating | 4.92
  Photo: https://a0.muscache.com/im/pictures/airflow/Hosting-1570949563091479875/original/8ae7bbe2-3f63-4679-9deb-1c34b62345cb.jpg?im_w=720
  Link: https://www.airbnb.ca/rooms/1570949563091479875?check_in=2026-10-10&check_out=2026-10-11&photo_id=2442791259
- Room in Xitun District | Oct 10–11 | $94 CAD total | 4.88 out of 5 average rating | 4.88
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-651654978734621095/original/1ddb82c8-8914-4fa7-abad-092b0ea0f8f9.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/651654978734621095?check_in=2026-10-10&check_out=2026-10-11&photo_id=1430692126
- Apartment in Taichung | Oct 10–11 | $111 CAD total | 4.87 out of 5 average rating | 4.87
  Photo: https://a0.muscache.com/im/pictures/4836d8ea-0f4f-4387-af26-b0b520b083ec.jpg?im_w=720
  Link: https://www.airbnb.ca/rooms/27509822?check_in=2026-10-10&check_out=2026-10-11&photo_id=553749184
- Room in Xitun District | Oct 10–11 | $98 CAD total | 4.8 out of 5 average rating | 4.8
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-690115060110554587/original/33e9bfa2-fba0-40d7-820e-c1ae8617287c.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/690115060110554587?check_in=2026-10-10&check_out=2026-10-11&photo_id=1467146075
- Room in 平陽里 | Oct 10–11 | $107 CAD total | 5.0 out of 5 average rating | 5.0
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1549012632786958249/original/bc443033-6e70-4af1-8769-299824a11151.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/1549012632786958249?check_in=2026-10-10&check_out=2026-10-11&photo_id=2471362749
- Guest favourite | Room in Central District | Oct 10–11 | $98 CAD total | 4.77 out of 5 average rating | 4.77
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-730022067306698171/original/1b6b702a-b488-4ac2-9668-4517e911bb62.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/730022067306698171?check_in=2026-10-10&check_out=2026-10-11&photo_id=1502590515
- Room in Xitun District | Oct 10–11 | $101 CAD total | 4.79 out of 5 average rating | 4.79
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-651651195085468655/original/7eea19d0-d07d-471e-aa7d-dabb770f314d.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/651651195085468655?check_in=2026-10-10&check_out=2026-10-11&photo_id=1429636681
- Guest favourite | Apartment in 育德里 | Oct 10–11 | $174 CAD total | 4.98 out of 5 average rating | 4.98
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1560808041559653256/original/01617dc0-46bd-44b9-858e-a7eff3db1586.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/1560808041559653256?check_in=2026-10-10&check_out=2026-10-11&photo_id=2416717554

SECTION Homes in Kaohsiung City
Subtitle: Taiwan port city with night markets
Desktop top: 1279.875; section height: 312.625
- Guest favourite | Home in Qianjin District | Oct 16–18 | $682 CAD total | 4.79 out of 5 average rating | 4.79
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-897024973787698725/original/1014fd8b-bbf9-4864-8858-59bf8cb5acc1.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/897024973787698725?check_in=2026-10-16&check_out=2026-10-18&photo_id=1657375779
- Guest favourite | Condo in 灣中里 | Nov 6–8 | $259 CAD total | 5.0 out of 5 average rating | 5.0
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTMwMTkxMzA2MjEwNTUyNDgzNg==/original/549c0025-3675-4031-97fc-a5658116e60e.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/1301913062105524836?check_in=2026-11-06&check_out=2026-11-08&photo_id=2209795927
- Guest favourite | Room in Yancheng District | Jan 15–17 | $332 CAD total | 4.9 out of 5 average rating | 4.9
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-808287376143537238/original/a374d55d-ea33-4029-b875-4cacbf98932e.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/808287376143537238?check_in=2027-01-15&check_out=2027-01-17&photo_id=1569790899
- Guest favourite | Home in Qianzhen District | Jan 8–10 | $456 CAD total | 4.94 out of 5 average rating | 4.94
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-650921304601585994/original/3e3c4a9b-aee9-406d-8425-86bcb67a3697.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/650921304601585994?check_in=2027-01-08&check_out=2027-01-10&photo_id=2129205598
- Room in Xinxing District | Nov 6–8 | $89 CAD total | 4.77 out of 5 average rating | 4.77
  Photo: https://a0.muscache.com/im/pictures/ee9575a3-0a2f-4e52-bd55-3e4653ae3af4.jpg?im_w=720
  Link: https://www.airbnb.ca/rooms/44273213?check_in=2026-11-06&check_out=2026-11-08&photo_id=1038998433
- Guest favourite | Apartment in Xinfeng Village | Dec 18–20 | $501 CAD total | 5.0 out of 5 average rating | 5.0
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1730306784928542363/original/e22f555e-cf7b-41d7-894b-cfeede88979d.jpeg?im_w=720
  Link: https://www.airbnb.ca/rooms/1730306784928542363?check_in=2026-12-18&check_out=2026-12-20&photo_id=2726792391
- Apartment in Lingya District | Nov 13–15 | $468 CAD total | 4.77 out of 5 average rating | 4.77
  Photo: https://a0.muscache.com/im/pictures/271be2ec-5499-4f99-93a6-426d23e9345e.jpg?im_w=720
  Link: https://www.airbnb.ca/rooms/716167599882221090?check_in=2026-11-13&check_out=2026-11-15&photo_id=1563239990
- Guest favourite | Condo in Yancheng District | Oct 16–18 | $350 CAD total | 4.94 out of 5 average rating | 4.94
  Photo: https://a0.muscache.com/im/pictures/1a9a3d7b-d431-4877-a15a-bd20ad8cf4a5.jpg?im_w=720
  Link: https://www.airbnb.ca/rooms/13501457?check_in=2026-10-16&check_out=2026-10-18&photo_id=489417348

SECTION Popular homes in Tokyo
Subtitle: none
Desktop top: 1632.5; section height: 276.625
- Rental unit in Shinjuku | $362 CAD total | 4.77 out of 5 average rating | 4.77
  Photo: https://a0.muscache.com/im/pictures/BnbProperty/BnbProperty-1715245240960211552/original/432ddba4-3307-4c9c-bbf7-44f6034d636e.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1332384853772547571?check_in=2026-10-30&check_out=2026-11-01&photo_id=2695944752
- Guest favourite | Apartment in Taitō-ku | Dec 18–20 | $682 CAD total | 5.0 out of 5 average rating | 5.0
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1759965640601579918/original/27572d9a-cfb8-4870-9269-af3144a5f283.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1759965640601579918?check_in=2026-12-18&check_out=2026-12-20&photo_id=2789384777
- Guest favourite | Apartment in Shinjuku | Dec 4–6 | $1,547 CAD total | 5.0 out of 5 average rating | 5.0
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1730335197701117128/original/4b7dfde2-6f9c-409c-8c11-9c632380194e.png?im_w=320
  Link: https://www.airbnb.ca/rooms/1730335197701117128?check_in=2026-12-04&check_out=2026-12-06&photo_id=2818288551
- Guest favourite | Apartment in Shinagawa-ku | Jan 29–31 | $155 CAD total | 4.88 out of 5 average rating | 4.88
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1694737098121578462/original/0f6d8a5e-644f-4939-a834-a96d11640301.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1694737098121578462?check_in=2027-01-29&check_out=2027-01-31&photo_id=2765559397
- Guest favourite | Room in Taitō-ku | Dec 18–20 | $249 CAD total | 5.0 out of 5 average rating | 5.0
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1372736213120320541/original/50522660-4fe4-4668-8569-1a325674dd1e.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1372736213120320541?check_in=2026-12-18&check_out=2026-12-20&photo_id=2465437128
- Guest favourite | Room in Shinjuku | Apr 30–May 2 | $199 CAD total | 5.0 out of 5 average rating | 5.0
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1651502296251741047/original/976e4dec-680d-40a9-8fa0-c42aa240c7d9.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1651502296251741047?check_in=2027-04-30&check_out=2027-05-02&photo_id=2616233287
- Guest favourite | Room in Sumida-ku | Dec 4–6 | $149 CAD total | 4.98 out of 5 average rating | 4.98
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1460502131361073474/original/e6c650ad-b4fb-4af8-be37-bf24a904444d.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1460502131361073474?check_in=2026-12-04&check_out=2026-12-06&photo_id=2264272236
- Guest favourite | Rental unit in Shinjuku | $262 CAD total | 4.98 out of 5 average rating | 4.98
  Photo: https://a0.muscache.com/im/pictures/BnbProperty/BnbProperty-1715240659669561503/original/42a50085-2177-482d-ae21-a4c13b36a565.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/31191801?check_in=2026-12-04&check_out=2026-12-06&photo_id=2695573684

SECTION Stay in Osaka
Subtitle: Harbor city and street food capital
Desktop top: 1949.125; section height: 296.625
- Guest favourite | Apartment in Naniwa Ward | Dec 4–6 | $129 CAD total | 4.92 out of 5 average rating | 4.92
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-32073378/original/6a5b6c26-ea12-4dc5-a5a6-7075c52d1fd0.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/32073378?check_in=2026-12-04&check_out=2026-12-06&photo_id=1855883622
- Guest favourite | Apartment in Osaka | Dec 4–6 | $145 CAD total | 4.89 out of 5 average rating | 4.89
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-32075321/original/199932ce-b5de-446c-bb28-9191c225510f.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/32075321?check_in=2026-12-04&check_out=2026-12-06&photo_id=1855877915
- Guest favourite | Apartment in Osaka | Jan 29–31 | $167 CAD total | 4.92 out of 5 average rating | 4.92
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1151290073382598901/original/377c49d1-b564-4453-8997-fb0ef41cf6ca.jpeg?im_w=240
  Link: https://www.airbnb.ca/rooms/1151290073382598901?check_in=2027-01-29&check_out=2027-01-31&photo_id=1901311983
- Guest favourite | Apartment in Osaka | Nov 27–29 | $1,618 CAD total | 5.0 out of 5 average rating | 5.0
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1725743112384393116/original/6c5e411a-a5f9-451d-b063-c840496e89b0.png?im_w=320
  Link: https://www.airbnb.ca/rooms/1725743112384393116?check_in=2026-11-27&check_out=2026-11-29&photo_id=2733044160
- Guest favourite | Home in Osaka | Jan 29–31 | $977 CAD total | 4.98 out of 5 average rating | 4.98
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1381518135279946352/original/e859f468-6a30-4d4d-b2fb-5907bb85f5e4.jpeg?im_w=240
  Link: https://www.airbnb.ca/rooms/1381518135279946352?check_in=2027-01-29&check_out=2027-01-31&photo_id=2121747062
- Guest favourite | Condo in Naniwa Ward | Nov 20–22 | $153 CAD total | 4.91 out of 5 average rating | 4.91
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTMxNzcxOTAwMjU0MDM4Mzc3NA%3D%3D/original/72025365-77f5-4d7e-b7c8-6b2cbece54af.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1317719002540383774?check_in=2026-11-20&check_out=2026-11-22&photo_id=2054704994
- Guest favourite | Hotel room in Naniwa Ward | Dec 4–6 | $164 CAD total | 4.9 out of 5 average rating | 4.9
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-27375581/original/7a2e17ed-4197-400f-8dc8-77264eaef15d.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1370075364241583514?check_in=2026-12-04&check_out=2026-12-06&photo_id=2101427251
- Guest favourite | Apartment in Osaka | Nov 27–29 | $140 CAD total | 4.75 out of 5 average rating | 4.75
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1296258316953205424/original/3ccc8f75-1ade-417f-9a31-f3fab1a44c0e.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1533803333197517003?check_in=2026-11-27&check_out=2026-11-29&photo_id=2373516770

SECTION Check out homes in Bangkok
Subtitle: none
Desktop top: 2285.75; section height: 276.625
- Guest favourite | Apartment in Sathon | Oct 16–18 | $59 CAD total | 4.9 out of 5 average rating | 4.9
  Photo: https://a0.muscache.com/im/pictures/32fbdc07-9770-4ddb-8a47-133c25a64b2c.jpg?im_w=320
  Link: https://www.airbnb.ca/rooms/29222188?check_in=2026-10-16&check_out=2026-10-18&photo_id=596186277
- Guest favourite | Apartment in Bangkok | Oct 16–18 | $118 CAD total | 4.92 out of 5 average rating | 4.92
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-1114904195556862236/original/38e9ffc2-2548-4e99-bcdc-83f028aed510.jpeg?im_w=240
  Link: https://www.airbnb.ca/rooms/1114904195556862236?check_in=2026-10-16&check_out=2026-10-18&photo_id=1863508371
- Guest favourite | Apartment in Sathon | Oct 23–25 | $81 CAD total | 4.93 out of 5 average rating | 4.93
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-29222102/original/c28ecdf4-3146-4c4a-ae2c-cd704e10d9cb.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/29222102?check_in=2026-10-23&check_out=2026-10-25&photo_id=1644998935
- Guest favourite | Room in Bang Rak | Oct 30–Nov 1 | $132 CAD total | 4.96 out of 5 average rating | 4.96
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTI5MzIzNjU0MTQ4NTMxNjIwOA%3D%3D/original/d0808ef7-cd6a-4902-9f5d-bd9e6e16c629.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1293236541485316208?check_in=2026-10-30&check_out=2026-11-01&photo_id=2033108375
- Guest favourite | Apartment in Khet Sathon | Nov 13–15 | $59 CAD total | 4.89 out of 5 average rating | 4.89
  Photo: https://a0.muscache.com/im/pictures/385a26b4-6a66-4e56-a996-980b58e033b3.jpg?im_w=480
  Link: https://www.airbnb.ca/rooms/28443679?check_in=2026-11-13&check_out=2026-11-15&photo_id=576832672
- Guest favourite | Home in Khlong San | Oct 16–18 | $143 CAD total | 4.97 out of 5 average rating | 4.97
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1590681599191028215/original/c9d115fd-13ae-4d95-8264-6128f6de1588.jpeg?im_w=240
  Link: https://www.airbnb.ca/rooms/1590681599191028215?check_in=2026-10-16&check_out=2026-10-18&photo_id=2572095225
- Guest favourite | Room in Khet Bang Kapi | Oct 23–25 | $35 CAD total | 4.9 out of 5 average rating | 4.9
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1701561810733949709/original/be2629c0-ff97-4dc6-8794-05bdba7db4d1.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1701561810733949709?check_in=2026-10-23&check_out=2026-10-25&photo_id=2666878879
- Guest favourite | Room in Khet Phra Nakhon | Oct 16–18 | $199 CAD total | 4.98 out of 5 average rating | 4.98
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTI5NjM4NzUwMzYzODk5MDI1MA%3D%3D/original/f9e0098f-c4f8-4e41-ae87-a7dffff8f665.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1296387503638990250?check_in=2026-10-16&check_out=2026-10-18&photo_id=2035960614

SECTION Popular homes in Vancouver
Subtitle: Pacific city with mountain views
Desktop top: 2602.375; section height: 296.625
- Guest favourite | Guest suite in Vancouver | Dec 18–20 | $457 CAD total | 4.86 out of 5 average rating | 4.86
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-32646786/original/5fa48175-ec51-4c61-83b9-266ab837962a.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/32646786?check_in=2026-12-18&check_out=2026-12-20&photo_id=2660605823
- Executive Hotel Le Soleil | $828 CAD total | 4.88 out of 5 average rating | 4.88
  Photo: https://a0.muscache.com/im/pictures/BnbProperty/BnbProperty-1701478825418872058/original/5ca3c2ae-8969-457b-8e32-89563e7c262c.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1699582835980108221?check_in=2026-10-23&check_out=2026-10-25&photo_id=2666647896
- Guest favourite | Room in Vancouver | Nov 13–15 | $275 CAD total | 4.94 out of 5 average rating | 4.94
  Photo: https://a0.muscache.com/im/pictures/1a043826-9b73-457a-9c34-0c72a706a151.jpg?im_w=320
  Link: https://www.airbnb.ca/rooms/20799287?check_in=2026-11-13&check_out=2026-11-15&photo_id=370183044
- EXchange Hotel Vancouver | $785 CAD total | 4.85 out of 5 average rating | 4.85
  Photo: https://a0.muscache.com/im/pictures/BnbProperty/BnbProperty-1700025435063662140/original/d86132d1-cf21-4626-8069-7c7748420184.jpeg?im_w=240
  Link: https://www.airbnb.ca/rooms/1693772925819433419?check_in=2026-10-23&check_out=2026-10-25&photo_id=2663447173
- Guest favourite | Guest suite in Vancouver | Nov 6–8 | $347 CAD total | 4.98 out of 5 average rating | 4.98
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1130105894987703195/original/2f39fa07-2379-414c-b9fb-88e703ea2929.jpeg?im_w=240
  Link: https://www.airbnb.ca/rooms/1130105894987703195?check_in=2026-11-06&check_out=2026-11-08&photo_id=2772538965
- Guest favourite | Guest suite in Vancouver | Nov 13–15 | $301 CAD total | 4.83 out of 5 average rating | 4.83
  Photo: https://a0.muscache.com/im/pictures/46381238/f5a20440_original.jpg?im_w=320
  Link: https://www.airbnb.ca/rooms/3678989?check_in=2026-11-13&check_out=2026-11-15&photo_id=28979959
- Guest favourite | Home in West Vancouver | Nov 6–8 | $997 CAD total | 4.98 out of 5 average rating | 4.98
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1458180758155324907/original/54f0c639-c4e0-4e02-9a89-ce0cbb89a4fb.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1458180758155324907?check_in=2026-11-06&check_out=2026-11-08&photo_id=2469483744
- Guest favourite | Apartment in Vancouver | Oct 30–Nov 1 | $1,292 CAD total | 5.0 out of 5 average rating | 5.0
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1746649758225675833/original/efdbb142-19d2-4ff8-b5bb-94a143840b49.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1746649758225675833?check_in=2026-10-30&check_out=2026-11-01&photo_id=2762268810

SECTION Available next month in Busan
Subtitle: South Korean beach and port city
Desktop top: 2939; section height: 296.625
- Guest favourite | Apartment in Dong-gu | Nov 27–29 | $249 CAD total | 4.88 out of 5 average rating | 4.88
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTEyNTMyMDU2OTAwNzQyNjM5OQ%3D%3D/original/529ac8b8-f78f-4a71-8328-ef611b5516f9.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1125320569007426399?check_in=2026-11-27&check_out=2026-11-29&photo_id=2047307223
- Guest favourite | Room in Busanjin-gu | Nov 27–29 | $155 CAD total | 4.95 out of 5 average rating | 4.95
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1695960707785726999/original/a7edced5-380e-438e-9184-ba546fbd747b.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1695960707785726999?check_in=2026-11-27&check_out=2026-11-29&photo_id=2666086416
- Guest favourite | Home in Jung-gu | Nov 20–22 | $506 CAD total | 5.0 out of 5 average rating | 5.0
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1668153694750261205/original/4a766517-a372-4fed-bea2-a390cf52be4b.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1668153694750261205?check_in=2026-11-20&check_out=2026-11-22&photo_id=2664640939
- Guest favourite | Home in Suyeong-gu | Nov 27–29 | $312 CAD total | 4.97 out of 5 average rating | 4.97
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-968008962561816389/original/d8dda498-5526-435a-ad15-0e6122f50f34.jpeg?im_w=240
  Link: https://www.airbnb.ca/rooms/968008962561816389?check_in=2026-11-27&check_out=2026-11-29&photo_id=1728840413
- Guest favourite | Room in Suyeong-gu | Nov 27–29 | $883 CAD total | 4.92 out of 5 average rating | 4.92
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1754611007391472164/original/653e2e04-9c58-4754-bb31-2797a4bf8b16.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1754611007391472164?check_in=2026-11-27&check_out=2026-11-29&photo_id=2778953713
- Guest favourite | Apartment in Suyeong-gu | Nov 13–15 | $692 CAD total | 4.99 out of 5 average rating | 4.99
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1132242941765156298/original/bbde7293-52b8-479c-83cf-43a38be6fc6b.jpeg?im_w=480
  Link: https://www.airbnb.ca/rooms/1132242941765156298?check_in=2026-11-13&check_out=2026-11-15&photo_id=1908131484
- Guest favourite | Home in Suyeong-gu | Nov 13–15 | $506 CAD total | 5.0 out of 5 average rating | 5.0
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1447718714676835698/original/f3c36757-7255-4e46-9dc4-ebfb108a6305.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1447718714676835698?check_in=2026-11-13&check_out=2026-11-15&photo_id=2494489766
- Apartment in Haeundae-gu | Nov 27–29 | $259 CAD total | 4.93 out of 5 average rating | 4.93
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-854166305333708690/original/c1dcbe59-3812-48ac-a10d-7e625ee82ddf.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/854166305333708690?check_in=2026-11-27&check_out=2026-11-29&photo_id=2739292614

SECTION Available next month in Kyoto
Subtitle: Ancient temples and shrines
Desktop top: 3275.625; section height: 296.625
- Guest favourite | Rental unit in Shimogyo-ku | $442 CAD total | 4.92 out of 5 average rating | 4.92
  Photo: https://a0.muscache.com/im/pictures/BnbProperty/BnbProperty-1715238778064899971/original/56454a56-e694-4fcd-bb3c-e9512f22d212.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1364382005540231413?check_in=2026-11-06&check_out=2026-11-08&photo_id=2695266730
- Guest favourite | Home in Minami Ward | Nov 13–15 | $577 CAD total | 4.95 out of 5 average rating | 4.95
  Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1214243381661088835/original/3a766b70-f76c-4d57-8e59-81177618d7ef.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1214243381661088835?check_in=2026-11-13&check_out=2026-11-15&photo_id=2005822240
- Rental unit in Higashiyama-ku | $398 CAD total | 4.79 out of 5 average rating | 4.79
  Photo: https://a0.muscache.com/im/pictures/BnbProperty/BnbProperty-1715237538047706638/original/a1f99a37-72fd-4212-a3eb-00d717d22f8a.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1587443077550186515?check_in=2026-11-06&check_out=2026-11-08&photo_id=2695067161
- Guest favourite | Home in Kamigyo Ward | Nov 6–8 | $674 CAD total | 4.95 out of 5 average rating | 4.95
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-1041858369279250258/original/c4f44586-10e3-4424-804c-7d0b67805c1a.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1041858369279250258?check_in=2026-11-06&check_out=2026-11-08&photo_id=1840946465
- Guest favourite | Townhouse in Kyoto | Nov 13–15 | $479 CAD total | 4.94 out of 5 average rating | 4.94
  Photo: https://a0.muscache.com/im/pictures/667e530f-c13e-4a01-9d1f-f7eafe168969.jpg?im_w=320
  Link: https://www.airbnb.ca/rooms/2994040?check_in=2026-11-13&check_out=2026-11-15&photo_id=130247586
- Guest favourite | Home in Higashiyama-ku | Nov 6–8 | $537 CAD total | 4.95 out of 5 average rating | 4.95
  Photo: https://a0.muscache.com/im/pictures/905a9cd2-8bc1-427d-b4ff-8599daa1f748.jpg?im_w=320
  Link: https://www.airbnb.ca/rooms/41075404?check_in=2026-11-06&check_out=2026-11-08&photo_id=937030996
- Guest favourite | Home in Fushimi-ku | Nov 6–8 | $1,007 CAD total | 4.99 out of 5 average rating | 4.99
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-1338396533065289653/original/f160cc8c-e780-47f7-a5e7-8b4688883439.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/1338396533065289653?check_in=2026-11-06&check_out=2026-11-08&photo_id=2072500362
- Guest favourite | Townhouse in Kyoto | Nov 6–8 | $683 CAD total | 4.94 out of 5 average rating | 4.94
  Photo: https://a0.muscache.com/im/pictures/miso/Hosting-43987995/original/b82326c2-df75-482a-bb2e-ce857dbd8cd8.jpeg?im_w=320
  Link: https://www.airbnb.ca/rooms/43987995?check_in=2026-11-06&check_out=2026-11-08&photo_id=1366939238

After the ten listing rows, use a full-width #f7f7f7 Inspiration for future getaways area. Heading22px semibold. Tabs Popular (selected), Coastal, Islands, Lakes, Mountains, Outdoors, Things to do; thin underline/border. Six columns with these exact 17 visible links followed by Show more:
- Penticton  | House rentals — https://www.airbnb.ca/penticton-canada/stays/houses
- Las Vegas  | Apartment rentals — https://www.airbnb.ca/las-vegas-nv/stays/apartments
- Oakville  | Monthly Rentals — https://www.airbnb.ca/oakville-canada/stays/monthly
- Scarborough  | Vacation rentals — https://www.airbnb.ca/scarborough-toronto-canada/stays
- Vancouver Island  | Cabin rentals — https://www.airbnb.ca/vancouver-island-canada/stays/cabins
- Montreal  | Pet-friendly rentals — https://www.airbnb.ca/montreal-canada/stays/pet-friendly
- Fernie  | Apartment rentals — https://www.airbnb.ca/fernie-canada/stays/apartments
- Mexico City  | Cabin rentals — https://www.airbnb.ca/mexico-city/stays/cabins
- Red Deer  | Monthly Rentals — https://www.airbnb.ca/red-deer-canada/stays/monthly
- Richmond  | Pet-friendly rentals — https://www.airbnb.ca/richmond-canada/stays/pet-friendly
- North York  | Apartment rentals — https://www.airbnb.ca/north-york-toronto-canada/stays/apartments
- Los Angeles  | Villa rentals — https://www.airbnb.ca/los-angeles-ca/stays/villas
- Newfoundland  | Apartment rentals — https://www.airbnb.ca/newfoundland-canada/stays/apartments
- Winnipeg  | Vacation rentals — https://www.airbnb.ca/winnipeg-canada/stays
- Quebec City  | Condo rentals — https://www.airbnb.ca/quebec-city-canada/stays/condos
- Halifax  | Condo rentals — https://www.airbnb.ca/halifax-canada/stays/condos
- Collingwood  | Condo rentals — https://www.airbnb.ca/collingwood-canada/stays/condos
Footer pale gray with three columns: Support, Hosting, Airbnb. Column headings14px medium and link text14px. Use the observed links below. Bottom divided by thin border; copyright © 2026 Airbnb, Inc., Privacy, Terms left, globe English (CA), $ CAD, Facebook, X, Instagram right.
- Help Centre — https://www.airbnb.ca/help/home?from=footer
- Get help with a safety issue — https://www.airbnb.ca/help/contact-us?entry=DESKTOP_FOOTER_SAFETY
- AirCover — https://www.airbnb.ca/aircover
- Anti-discrimination — https://www.airbnb.ca/against-discrimination
- Disability support — https://www.airbnb.ca/accessibility
- Cancellation options — https://www.airbnb.ca/help/article/2701/extenuating-circumstances-policy-and-the-coronavirus-covid19
- Report neighbourhood concern — https://www.airbnb.ca/neighbors
- Airbnb your home — https://www.airbnb.ca/host/homes?from_footer=1
- Airbnb your experience — https://www.airbnb.ca/host/experiences
- Airbnb your service — https://www.airbnb.ca/host/services
- AirCover for Hosts — https://www.airbnb.ca/aircover-for-hosts
- Hosting resources — https://www.airbnb.ca/resources
- Community forum — https://community.withairbnb.com/t5/Community-Center/ct-p/community-center
- Hosting responsibly — https://www.airbnb.ca/help/responsible-hosting
- Join a free hosting class — https://www.airbnb.ca/e/intro-to-hosting
- Find a co-host — https://www.airbnb.ca/host/co-hosts
- Refer a host — https://www.airbnb.ca/refer
- 2026 Summer Release — https://www.airbnb.ca/release
- Newsroom — https://www.airbnb.ca/press/news
- Careers — https://www.airbnb.ca/careers
- Investors — https://investors.airbnb.com/
- Gift cards — https://www.airbnb.ca/giftcards
- Airbnb.org emergency stays — https://www.airbnb.org/?locale=en-CA
- Navigate to Facebook — https://www.facebook.com/airbnb
- Navigate to Twitter — https://twitter.com/airbnb
- Navigate to Instagram — https://instagram.com/airbnb
- Privacy — https://www.airbnb.ca/terms/privacy_policy
- Terms — https://www.airbnb.ca/terms
- Navigate to Facebook — https://www.facebook.com/airbnb
- Navigate to Twitter — https://twitter.com/airbnb
- Navigate to Instagram — https://instagram.com/airbnb
- Privacy — https://www.airbnb.ca/terms/privacy_policy
- Terms — https://www.airbnb.ca/terms
- Privacy — https://www.airbnb.ca/terms/privacy_policy
- Terms — https://www.airbnb.ca/terms
- Navigate to Facebook — https://www.facebook.com/airbnb
- Navigate to Twitter — https://twitter.com/airbnb
- Navigate to Instagram — https://instagram.com/airbnb

For narrow widths preserve horizontal property carousels, do not stack all cards into an unrelated vertical grid. Use the observed compact mobile header/search treatment once mobile reference details are supplied. Do not invent titles, rating values, regional availability, photography, campaigns or badges. Do not claim the result is verified or pixel-identical; actual rendered verification is performed separately. Produce responsive working HTML/CSS and a full desktop screen.
```

## 10月11日另送出的390px窄版新工作

此為不同範圍的新MOBILE請求，不是重送原DESKTOP逾時請求。session `2686441563832907567`，screen `73285e56f28a4277af38628dc351e433`。已取得完整原始HTML／PNG與回應；提供者實際回報DESKTOP2560×9340。主代理已查看原PNG，左側窄內容與右側大片白區、紫色placeholder均保留為限制，不宣稱MOBILE成功或與官方一致。原始輸出與來源校正HTML分開保存。

```text
Create a new MOBILE screen, target 390 CSS px wide, for the observed public Airbnb Canada homepage. This is a distinct narrow-width study based on the 2026-10-10 public reference at https://www.airbnb.ca/?locale=en, not a regeneration of the prior desktop request. Region/cookie/personalization varies; do not invent a marketing hero or universal official fidelity claim. Reproduce the observed listing feed, using genuine image URLs and content below. Produce a full mobile screen with responsive working semantic HTML/CSS. No subscription or paid service.
At 390x844: white background, Airbnb Cereal-like sans serif, primary #222 and muted #6a6a6a. Search pill x24 y12 width342 height56, radius28, thin #ddd border, soft shadow, search icon and text Start your search. No desktop wordmark/header. Horizontally scrollable illustrated category pills start x24 y86, height40: All (selected), Homes, Experiences, Services partly offscreen. Keep overflow inside the strip, not document width. Four official icon images are listed below. First heading x26 y148, actual visual weight600 size20 line24; subtitle x26 y177 size12 line16. Row arrow circle at338 y146 28x28. Property cards x24 and201, width165 gap12, image156.75px high radius20; third card clipped at x378. Below photos title13px medium, dates/total CAD price/rating12px. White Guest favourite pill at left top and white outlined heart at right top where observed. Do not create fake account or booking completion; favorites are local demonstration toggles only. Preserve horizontal carousels for all ten rows. No services/experience hero feed is present.
Source full page height4980. Row heading Y values:148,464.75,779.5,1102.25,1419,1719.75,2036.5,2337.25,2638,2954.75. Bottom fixed navigation at y779 height65: Explore selected pink #ff385c search icon, Wishlists heart gray, Log in profile gray. Use actual footer after all ten rows, pale gray Inspiration for future getaways area with horizontally scrollable category tabs; Popular selected, Coastal, Islands, Lakes, Mountains, Outdoors, Things to do. Narrow destination grid two columns and Show more. Footer columns stack vertically Support, Hosting, Airbnb, gray dividers, copyright ©2026 Airbnb Inc., English(CA), CAD, Privacy, Terms and social links. Leave enough bottom padding for fixed navigation.
Category icons:
All https://a0.muscache.com/im/pictures/AirbnbPlatformAssets/AirbnbPlatformAssets-search-bar-icons/original/ab2fd9ad-d830-4342-982b-47722f2d93bf.png?im_w=120
Homes https://a0.muscache.com/im/pictures/AirbnbPlatformAssets/AirbnbPlatformAssets-search-bar-icons/original/d4446c94-f881-4797-a0ed-ebc6631386de.png?im_w=120
Experiences https://a0.muscache.com/im/pictures/AirbnbPlatformAssets/AirbnbPlatformAssets-search-bar-icons/original/bd2cb05a-95c9-41bd-8b5f-3faa08e49ba2.png?im_w=120
Services https://a0.muscache.com/im/pictures/AirbnbPlatformAssets/AirbnbPlatformAssets-search-bar-icons/original/7e922391-eb34-4021-9bde-92ee4cd5676c.png?im_w=120

Ten listing rows. Preserve exact order and dates/prices, all assets are public official listing photography. Deduplicate repeated accessibility strings when displaying card labels:

ROW Stay in Lake Kawaguchi | Stay in Lake Kawaguchi
Lake near Mount Fuji with hot springs
Card Villa in Fujikawaguchiko
Observed labels: Guest favourite | Guest favourite | Villa in Fujikawaguchiko | Jan 8–10 | $826 CAD total |   | $826 CAD total | , |  ·  | 4.97 out of 5 average rating | 4.97
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1643751316846284459/original/95b180e5-610c-474e-ab46-dd3465024953.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1643751316846284459?check_in=2027-01-08&check_out=2027-01-10&photo_id=2555091093
Card Villa in Fujikawaguchiko
Observed labels: Guest favourite | Guest favourite | Villa in Fujikawaguchiko | Dec 18–20 | $501 CAD total |   | $501 CAD total | , |  ·  | 5.0 out of 5 average rating | 5.0
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-1157544045597144904/original/9995ee75-5f85-43cf-bd49-726302c5e79f.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1157544045597144904?check_in=2026-12-18&check_out=2026-12-20&photo_id=1935433831
Card Home in Fujikawaguchiko
Observed labels: Home in Fujikawaguchiko | Jan 8–10 | $900 CAD total |   | $900 CAD total | , |  ·  | 5.0 out of 5 average rating | 5.0
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1765851217717766105/original/4fc7fb29-f279-49da-91a8-5f0768b7669a.png?im_w=480
Link: https://www.airbnb.ca/rooms/1765851217717766105?check_in=2027-01-08&check_out=2027-01-10&photo_id=2810445666
Card Room in Fujikawaguchiko
Observed labels: Guest favourite | Guest favourite | Room in Fujikawaguchiko | Dec 25–27 | $126 CAD total |   | $126 CAD total | , |  ·  | 4.91 out of 5 average rating | 4.91
Photo: https://a0.muscache.com/im/pictures/56879337-8c77-48d1-85c2-f7adc365240d.jpg?im_w=480
Link: https://www.airbnb.ca/rooms/37946844?check_in=2026-12-25&check_out=2026-12-27&photo_id=1690396856
Card Villa in Fujikawaguchiko
Observed labels: Villa in Fujikawaguchiko | Dec 4–6 | $829 CAD total |   | $829 CAD total | , |  ·  | 4.97 out of 5 average rating | 4.97
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTI5ODAyODM0MjM3OTI3ODk0MQ%3D%3D/original/af35b904-5b43-4224-a8f9-45a546076cc3.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1298028342379278941?check_in=2026-12-04&check_out=2026-12-06&photo_id=2053633251
Card Home in Fujikawaguchiko
Observed labels: Guest favourite | Guest favourite | Home in Fujikawaguchiko | Jan 15–17 | $826 CAD total |   | $826 CAD total | , |  ·  | 4.99 out of 5 average rating | 4.99
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1541201076214760918/original/c5be7b50-9904-4471-a5a1-55454ec4e4f0.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/1541201076214760918?check_in=2027-01-15&check_out=2027-01-17&photo_id=2385711402
Card Home in Fujikawaguchiko
Observed labels: Guest favourite | Guest favourite | Home in Fujikawaguchiko | Jan 8–10 | $2,739 CAD total |   | $2,739 CAD total | , |  ·  | 4.92 out of 5 average rating | 4.92
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTQ2ODA0NDc0MTQwNTE3NDcyMw==/original/df37cf2e-95a7-425b-bd47-2ba557b0e698.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/1468044741405174723?check_in=2027-01-08&check_out=2027-01-10&photo_id=2277845846
Card Townhouse in Fujikawaguchiko
Observed labels: Guest favourite | Guest favourite | Townhouse in Fujikawaguchiko | Jan 15–17 | $627 CAD total |   | $627 CAD total | , |  ·  | 4.85 out of 5 average rating | 4.85
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1662004249160940860/original/3fc8f1e5-7f75-4985-a644-af2bfc09f587.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/1662004249160940860?check_in=2027-01-15&check_out=2027-01-17&photo_id=2589221688

ROW Places to stay in Taitung City | Places to stay in Taitung City
Taiwan city on the Pacific coast
Card Condo in 鐵花里
Observed labels: Guest favourite | Guest favourite | Condo in 鐵花里 | Oct 16–18 | $230 CAD total |   | $230 CAD total | , |  ·  | 4.97 out of 5 average rating | 4.97
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTA0NzY2MjU0Nzk1MTQxMTgzNg%3D%3D/original/ceeff414-5926-485e-ae41-a7602906f22c.jpeg?im_w=320
Link: https://www.airbnb.ca/rooms/1047662547951411836?check_in=2026-10-16&check_out=2026-10-18&photo_id=1822250993
Card Room in Taitung City
Observed labels: Guest favourite | Guest favourite | Room in Taitung City | Nov 6–8 | $158 CAD total |   | $158 CAD total | , |  ·  | 4.97 out of 5 average rating | 4.97
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1573156596883032250/original/89973b2d-ffeb-40eb-815c-f3bfd5194802.png?im_w=320
Link: https://www.airbnb.ca/rooms/1573156596883032250?check_in=2026-11-06&check_out=2026-11-08&photo_id=2734486045
Card Apartment in Taitung City
Observed labels: Guest favourite | Guest favourite | Apartment in Taitung City | Nov 13–15 | $162 CAD total |   | $162 CAD total | , |  ·  | 4.81 out of 5 average rating | 4.81
Photo: https://a0.muscache.com/im/pictures/3b22e9b2-e9b7-4fdb-a036-12a629b8cf81.jpg?im_w=480
Link: https://www.airbnb.ca/rooms/946739388519494023?check_in=2026-11-13&check_out=2026-11-15&photo_id=1788319157
Card Apartment in Taitung City
Observed labels: Guest favourite | Guest favourite | Apartment in Taitung City | Nov 13–15 | $637 CAD total |   | $637 CAD total | , |  ·  | 4.97 out of 5 average rating | 4.97
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-993162296352157724/original/b916bd51-9230-4364-ab31-bb6bf4ebe25e.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/993162296352157724?check_in=2026-11-13&check_out=2026-11-15&photo_id=1803998346
Card Room in Taitung City
Observed labels: Guest favourite | Guest favourite | Room in Taitung City | Nov 6–8 | $188 CAD total |   | $188 CAD total | , |  ·  | 4.83 out of 5 average rating | 4.83
Photo: https://a0.muscache.com/im/pictures/22375ac8-66a0-4a0b-8680-926689b9eee5.jpg?im_w=480
Link: https://www.airbnb.ca/rooms/14888380?check_in=2026-11-06&check_out=2026-11-08&photo_id=208212461
Card Room in Taitung City
Observed labels: Guest favourite | Guest favourite | Room in Taitung City | Nov 6–8 | $589 CAD total |   | $589 CAD total | , |  ·  | 4.94 out of 5 average rating | 4.94
Photo: https://a0.muscache.com/im/pictures/b38a2038-b3d8-4b7f-8360-e13ecfd134c1.jpg?im_w=720
Link: https://www.airbnb.ca/rooms/51243169?check_in=2026-11-06&check_out=2026-11-08&photo_id=1225734378
Card Room in Taitung City
Observed labels: Guest favourite | Guest favourite | Room in Taitung City | Nov 6–8 | $136 CAD total |   | $136 CAD total | , |  ·  | 4.88 out of 5 average rating | 4.88
Photo: https://a0.muscache.com/im/pictures/7c1ad469-1951-48f2-a3ca-5427605db5ad.jpg?im_w=720
Link: https://www.airbnb.ca/rooms/23301740?check_in=2026-11-06&check_out=2026-11-08&photo_id=1030515126
Card Room in Taitung City
Observed labels: Guest favourite | Guest favourite | Room in Taitung City | Oct 16–18 | $60 CAD total |   | $60 CAD total | , |  ·  | 4.82 out of 5 average rating | 4.82
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-678760882010269235/original/edafbd08-6664-407a-b9f1-681ed8a1a482.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/678760882010269235?check_in=2026-10-16&check_out=2026-10-18&photo_id=1455392868

ROW Available in Taichung City this weekend | Available in Taichung City this weekend
Taiwan city with night markets
Card Apartment in 忠誠里
Observed labels: Guest favourite | Guest favourite | Apartment in 忠誠里 | Oct 10–11 | $224 CAD total |   | $224 CAD total | , |  ·  | 4.92 out of 5 average rating | 4.92
Photo: https://a0.muscache.com/im/pictures/airflow/Hosting-1570949563091479875/original/8ae7bbe2-3f63-4679-9deb-1c34b62345cb.jpg?im_w=480
Link: https://www.airbnb.ca/rooms/1570949563091479875?check_in=2026-10-10&check_out=2026-10-11&photo_id=2442791259
Card Room in Xitun District
Observed labels: Room in Xitun District | Oct 10–11 | $94 CAD total |   | $94 CAD total | , |  ·  | 4.88 out of 5 average rating | 4.88
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-651654978734621095/original/1ddb82c8-8914-4fa7-abad-092b0ea0f8f9.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/651654978734621095?check_in=2026-10-10&check_out=2026-10-11&photo_id=1430692126
Card Apartment in Taichung
Observed labels: Apartment in Taichung | Oct 10–11 | $111 CAD total |   | $111 CAD total | , |  ·  | 4.87 out of 5 average rating | 4.87
Photo: https://a0.muscache.com/im/pictures/4836d8ea-0f4f-4387-af26-b0b520b083ec.jpg?im_w=480
Link: https://www.airbnb.ca/rooms/27509822?check_in=2026-10-10&check_out=2026-10-11&photo_id=553749184
Card Room in Xitun District
Observed labels: Room in Xitun District | Oct 10–11 | $98 CAD total |   | $98 CAD total | , |  ·  | 4.8 out of 5 average rating | 4.8
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-690115060110554587/original/33e9bfa2-fba0-40d7-820e-c1ae8617287c.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/690115060110554587?check_in=2026-10-10&check_out=2026-10-11&photo_id=1467146075
Card Room in 平陽里
Observed labels: Room in 平陽里 | Oct 10–11 | $107 CAD total |   | $107 CAD total | , |  ·  | 5.0 out of 5 average rating | 5.0
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1549012632786958249/original/bc443033-6e70-4af1-8769-299824a11151.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1549012632786958249?check_in=2026-10-10&check_out=2026-10-11&photo_id=2471362749
Card Room in Central District
Observed labels: Guest favourite | Guest favourite | Room in Central District | Oct 10–11 | $98 CAD total |   | $98 CAD total | , |  ·  | 4.77 out of 5 average rating | 4.77
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-730022067306698171/original/1b6b702a-b488-4ac2-9668-4517e911bb62.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/730022067306698171?check_in=2026-10-10&check_out=2026-10-11&photo_id=1502590515
Card Room in Xitun District
Observed labels: Room in Xitun District | Oct 10–11 | $101 CAD total |   | $101 CAD total | , |  ·  | 4.79 out of 5 average rating | 4.79
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-651651195085468655/original/7eea19d0-d07d-471e-aa7d-dabb770f314d.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/651651195085468655?check_in=2026-10-10&check_out=2026-10-11&photo_id=1429636681
Card Apartment in 育德里
Observed labels: Guest favourite | Guest favourite | Apartment in 育德里 | Oct 10–11 | $174 CAD total |   | $174 CAD total | , |  ·  | 4.98 out of 5 average rating | 4.98
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1560808041559653256/original/01617dc0-46bd-44b9-858e-a7eff3db1586.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/1560808041559653256?check_in=2026-10-10&check_out=2026-10-11&photo_id=2416717554

ROW Homes in Kaohsiung City | Homes in Kaohsiung City
Taiwan port city with night markets
Card Home in Qianjin District
Observed labels: Guest favourite | Guest favourite | Home in Qianjin District | Oct 16–18 | $682 CAD total |   | $682 CAD total | , |  ·  | 4.79 out of 5 average rating | 4.79
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-897024973787698725/original/1014fd8b-bbf9-4864-8858-59bf8cb5acc1.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/897024973787698725?check_in=2026-10-16&check_out=2026-10-18&photo_id=1657375779
Card Condo in 灣中里
Observed labels: Guest favourite | Guest favourite | Condo in 灣中里 | Nov 6–8 | $259 CAD total |   | $259 CAD total | , |  ·  | 5.0 out of 5 average rating | 5.0
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTMwMTkxMzA2MjEwNTUyNDgzNg==/original/549c0025-3675-4031-97fc-a5658116e60e.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1301913062105524836?check_in=2026-11-06&check_out=2026-11-08&photo_id=2209795927
Card Room in Yancheng District
Observed labels: Guest favourite | Guest favourite | Room in Yancheng District | Jan 15–17 | $332 CAD total |   | $332 CAD total | , |  ·  | 4.9 out of 5 average rating | 4.9
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-808287376143537238/original/a374d55d-ea33-4029-b875-4cacbf98932e.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/808287376143537238?check_in=2027-01-15&check_out=2027-01-17&photo_id=1569790899
Card Home in Qianzhen District
Observed labels: Guest favourite | Guest favourite | Home in Qianzhen District | Jan 8–10 | $456 CAD total |   | $456 CAD total | , |  ·  | 4.94 out of 5 average rating | 4.94
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-650921304601585994/original/3e3c4a9b-aee9-406d-8425-86bcb67a3697.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/650921304601585994?check_in=2027-01-08&check_out=2027-01-10&photo_id=2129205598
Card Room in Xinxing District
Observed labels: Room in Xinxing District | Nov 6–8 | $89 CAD total |   | $89 CAD total | , |  ·  | 4.77 out of 5 average rating | 4.77
Photo: https://a0.muscache.com/im/pictures/ee9575a3-0a2f-4e52-bd55-3e4653ae3af4.jpg?im_w=480
Link: https://www.airbnb.ca/rooms/44273213?check_in=2026-11-06&check_out=2026-11-08&photo_id=1038998433
Card Apartment in Xinfeng Village
Observed labels: Guest favourite | Guest favourite | Apartment in Xinfeng Village | Dec 18–20 | $501 CAD total |   | $501 CAD total | , |  ·  | 5.0 out of 5 average rating | 5.0
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1730306784928542363/original/e22f555e-cf7b-41d7-894b-cfeede88979d.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/1730306784928542363?check_in=2026-12-18&check_out=2026-12-20&photo_id=2726792391
Card Apartment in Lingya District
Observed labels: Apartment in Lingya District | Nov 13–15 | $468 CAD total |   | $468 CAD total | , |  ·  | 4.77 out of 5 average rating | 4.77
Photo: https://a0.muscache.com/im/pictures/271be2ec-5499-4f99-93a6-426d23e9345e.jpg?im_w=720
Link: https://www.airbnb.ca/rooms/716167599882221090?check_in=2026-11-13&check_out=2026-11-15&photo_id=1563239990
Card Condo in Yancheng District
Observed labels: Guest favourite | Guest favourite | Condo in Yancheng District | Oct 16–18 | $350 CAD total |   | $350 CAD total | , |  ·  | 4.94 out of 5 average rating | 4.94
Photo: https://a0.muscache.com/im/pictures/1a9a3d7b-d431-4877-a15a-bd20ad8cf4a5.jpg?im_w=720
Link: https://www.airbnb.ca/rooms/13501457?check_in=2026-10-16&check_out=2026-10-18&photo_id=489417348

ROW Popular homes in Tokyo | Popular homes in Tokyo
Card Rental unit in Shinjuku
Observed labels: Rental unit in Shinjuku | $362 CAD total |   | $362 CAD total | , |  ·  | 4.77 out of 5 average rating | 4.77
Photo: https://a0.muscache.com/im/pictures/BnbProperty/BnbProperty-1715245240960211552/original/432ddba4-3307-4c9c-bbf7-44f6034d636e.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1332384853772547571?check_in=2026-10-30&check_out=2026-11-01&photo_id=2695944752
Card Apartment in Taitō-ku
Observed labels: Guest favourite | Guest favourite | Apartment in Taitō-ku | Dec 18–20 | $682 CAD total |   | $682 CAD total | , |  ·  | 5.0 out of 5 average rating | 5.0
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1759965640601579918/original/27572d9a-cfb8-4870-9269-af3144a5f283.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1759965640601579918?check_in=2026-12-18&check_out=2026-12-20&photo_id=2789384777
Card Apartment in Shinjuku
Observed labels: Guest favourite | Guest favourite | Apartment in Shinjuku | Dec 4–6 | $1,547 CAD total |   | $1,547 CAD total | , |  ·  | 5.0 out of 5 average rating | 5.0
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1730335197701117128/original/4b7dfde2-6f9c-409c-8c11-9c632380194e.png?im_w=480
Link: https://www.airbnb.ca/rooms/1730335197701117128?check_in=2026-12-04&check_out=2026-12-06&photo_id=2818288551
Card Apartment in Shinagawa-ku
Observed labels: Guest favourite | Guest favourite | Apartment in Shinagawa-ku | Jan 29–31 | $155 CAD total |   | $155 CAD total | , |  ·  | 4.88 out of 5 average rating | 4.88
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1694737098121578462/original/0f6d8a5e-644f-4939-a834-a96d11640301.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1694737098121578462?check_in=2027-01-29&check_out=2027-01-31&photo_id=2765559397
Card Room in Taitō-ku
Observed labels: Guest favourite | Guest favourite | Room in Taitō-ku | Dec 18–20 | $249 CAD total |   | $249 CAD total | , |  ·  | 5.0 out of 5 average rating | 5.0
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1372736213120320541/original/50522660-4fe4-4668-8569-1a325674dd1e.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1372736213120320541?check_in=2026-12-18&check_out=2026-12-20&photo_id=2465437128
Card Room in Shinjuku
Observed labels: Guest favourite | Guest favourite | Room in Shinjuku | Apr 30–May 2 | $199 CAD total |   | $199 CAD total | , |  ·  | 5.0 out of 5 average rating | 5.0
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1651502296251741047/original/976e4dec-680d-40a9-8fa0-c42aa240c7d9.jpeg?im_w=240
Link: https://www.airbnb.ca/rooms/1651502296251741047?check_in=2027-04-30&check_out=2027-05-02&photo_id=2616233287
Card Room in Sumida-ku
Observed labels: Guest favourite | Guest favourite | Room in Sumida-ku | Dec 4–6 | $149 CAD total |   | $149 CAD total | , |  ·  | 4.98 out of 5 average rating | 4.98
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1460502131361073474/original/e6c650ad-b4fb-4af8-be37-bf24a904444d.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/1460502131361073474?check_in=2026-12-04&check_out=2026-12-06&photo_id=2264272236
Card Rental unit in Shinjuku
Observed labels: Guest favourite | Guest favourite | Rental unit in Shinjuku | $262 CAD total |   | $262 CAD total | , |  ·  | 4.98 out of 5 average rating | 4.98
Photo: https://a0.muscache.com/im/pictures/BnbProperty/BnbProperty-1715240659669561503/original/42a50085-2177-482d-ae21-a4c13b36a565.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/31191801?check_in=2026-12-04&check_out=2026-12-06&photo_id=2695573684

ROW Stay in Osaka | Stay in Osaka
Harbor city and street food capital
Card Apartment in Naniwa Ward
Observed labels: Guest favourite | Guest favourite | Apartment in Naniwa Ward | Dec 4–6 | $129 CAD total |   | $129 CAD total | , |  ·  | 4.92 out of 5 average rating | 4.92
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-32073378/original/6a5b6c26-ea12-4dc5-a5a6-7075c52d1fd0.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/32073378?check_in=2026-12-04&check_out=2026-12-06&photo_id=1855883622
Card Apartment in Osaka
Observed labels: Guest favourite | Guest favourite | Apartment in Osaka | Dec 4–6 | $145 CAD total |   | $145 CAD total | , |  ·  | 4.89 out of 5 average rating | 4.89
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-32075321/original/199932ce-b5de-446c-bb28-9191c225510f.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/32075321?check_in=2026-12-04&check_out=2026-12-06&photo_id=1855877915
Card Apartment in Osaka
Observed labels: Guest favourite | Guest favourite | Apartment in Osaka | Jan 29–31 | $167 CAD total |   | $167 CAD total | , |  ·  | 4.92 out of 5 average rating | 4.92
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1151290073382598901/original/377c49d1-b564-4453-8997-fb0ef41cf6ca.jpeg?im_w=320
Link: https://www.airbnb.ca/rooms/1151290073382598901?check_in=2027-01-29&check_out=2027-01-31&photo_id=1901311983
Card Apartment in Osaka
Observed labels: Guest favourite | Guest favourite | Apartment in Osaka | Nov 27–29 | $1,618 CAD total |   | $1,618 CAD total | , |  ·  | 5.0 out of 5 average rating | 5.0
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1725743112384393116/original/6c5e411a-a5f9-451d-b063-c840496e89b0.png?im_w=480
Link: https://www.airbnb.ca/rooms/1725743112384393116?check_in=2026-11-27&check_out=2026-11-29&photo_id=2733044160
Card Home in Osaka
Observed labels: Guest favourite | Guest favourite | Home in Osaka | Jan 29–31 | $977 CAD total |   | $977 CAD total | , |  ·  | 4.98 out of 5 average rating | 4.98
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1381518135279946352/original/e859f468-6a30-4d4d-b2fb-5907bb85f5e4.jpeg?im_w=320
Link: https://www.airbnb.ca/rooms/1381518135279946352?check_in=2027-01-29&check_out=2027-01-31&photo_id=2121747062
Card Condo in Naniwa Ward
Observed labels: Guest favourite | Guest favourite | Condo in Naniwa Ward | Nov 20–22 | $153 CAD total |   | $153 CAD total | , |  ·  | 4.91 out of 5 average rating | 4.91
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTMxNzcxOTAwMjU0MDM4Mzc3NA%3D%3D/original/72025365-77f5-4d7e-b7c8-6b2cbece54af.jpeg?im_w=240
Link: https://www.airbnb.ca/rooms/1317719002540383774?check_in=2026-11-20&check_out=2026-11-22&photo_id=2054704994
Card Hotel room in Naniwa Ward
Observed labels: Guest favourite | Guest favourite | Hotel room in Naniwa Ward | Dec 4–6 | $164 CAD total |   | $164 CAD total | , |  ·  | 4.9 out of 5 average rating | 4.9
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-27375581/original/7a2e17ed-4197-400f-8dc8-77264eaef15d.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/1370075364241583514?check_in=2026-12-04&check_out=2026-12-06&photo_id=2101427251
Card Apartment in Osaka
Observed labels: Guest favourite | Guest favourite | Apartment in Osaka | Nov 27–29 | $140 CAD total |   | $140 CAD total | , |  ·  | 4.75 out of 5 average rating | 4.75
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1296258316953205424/original/3ccc8f75-1ade-417f-9a31-f3fab1a44c0e.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/1533803333197517003?check_in=2026-11-27&check_out=2026-11-29&photo_id=2373516770

ROW Check out homes in Bangkok | Check out homes in Bangkok
Card Apartment in Sathon
Observed labels: Guest favourite | Guest favourite | Apartment in Sathon | Oct 16–18 | $59 CAD total |   | $59 CAD total | , |  ·  | 4.9 out of 5 average rating | 4.9
Photo: https://a0.muscache.com/im/pictures/32fbdc07-9770-4ddb-8a47-133c25a64b2c.jpg?im_w=480
Link: https://www.airbnb.ca/rooms/29222188?check_in=2026-10-16&check_out=2026-10-18&photo_id=596186277
Card Apartment in Bangkok
Observed labels: Guest favourite | Guest favourite | Apartment in Bangkok | Oct 16–18 | $118 CAD total |   | $118 CAD total | , |  ·  | 4.92 out of 5 average rating | 4.92
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-1114904195556862236/original/38e9ffc2-2548-4e99-bcdc-83f028aed510.jpeg?im_w=320
Link: https://www.airbnb.ca/rooms/1114904195556862236?check_in=2026-10-16&check_out=2026-10-18&photo_id=1863508371
Card Apartment in Sathon
Observed labels: Guest favourite | Guest favourite | Apartment in Sathon | Oct 23–25 | $81 CAD total |   | $81 CAD total | , |  ·  | 4.93 out of 5 average rating | 4.93
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-29222102/original/c28ecdf4-3146-4c4a-ae2c-cd704e10d9cb.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/29222102?check_in=2026-10-23&check_out=2026-10-25&photo_id=1644998935
Card Room in Bang Rak
Observed labels: Guest favourite | Guest favourite | Room in Bang Rak | Oct 30–Nov 1 | $132 CAD total |   | $132 CAD total | , |  ·  | 4.96 out of 5 average rating | 4.96
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTI5MzIzNjU0MTQ4NTMxNjIwOA%3D%3D/original/d0808ef7-cd6a-4902-9f5d-bd9e6e16c629.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1293236541485316208?check_in=2026-10-30&check_out=2026-11-01&photo_id=2033108375
Card Apartment in Khet Sathon
Observed labels: Guest favourite | Guest favourite | Apartment in Khet Sathon | Nov 13–15 | $59 CAD total |   | $59 CAD total | , |  ·  | 4.89 out of 5 average rating | 4.89
Photo: https://a0.muscache.com/im/pictures/385a26b4-6a66-4e56-a996-980b58e033b3.jpg?im_w=480
Link: https://www.airbnb.ca/rooms/28443679?check_in=2026-11-13&check_out=2026-11-15&photo_id=576832672
Card Home in Khlong San
Observed labels: Guest favourite | Guest favourite | Home in Khlong San | Oct 16–18 | $143 CAD total |   | $143 CAD total | , |  ·  | 4.97 out of 5 average rating | 4.97
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1590681599191028215/original/c9d115fd-13ae-4d95-8264-6128f6de1588.jpeg?im_w=240
Link: https://www.airbnb.ca/rooms/1590681599191028215?check_in=2026-10-16&check_out=2026-10-18&photo_id=2572095225
Card Room in Khet Bang Kapi
Observed labels: Guest favourite | Guest favourite | Room in Khet Bang Kapi | Oct 23–25 | $35 CAD total |   | $35 CAD total | , |  ·  | 4.9 out of 5 average rating | 4.9
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1701561810733949709/original/be2629c0-ff97-4dc6-8794-05bdba7db4d1.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/1701561810733949709?check_in=2026-10-23&check_out=2026-10-25&photo_id=2666878879
Card Room in Khet Phra Nakhon
Observed labels: Guest favourite | Guest favourite | Room in Khet Phra Nakhon | Oct 16–18 | $199 CAD total |   | $199 CAD total | , |  ·  | 4.98 out of 5 average rating | 4.98
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTI5NjM4NzUwMzYzODk5MDI1MA%3D%3D/original/f9e0098f-c4f8-4e41-ae87-a7dffff8f665.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/1296387503638990250?check_in=2026-10-16&check_out=2026-10-18&photo_id=2035960614

ROW Popular homes in Vancouver | Popular homes in Vancouver
Pacific city with mountain views
Card Guest suite in Vancouver
Observed labels: Guest favourite | Guest favourite | Guest suite in Vancouver | Dec 18–20 | $457 CAD total |   | $457 CAD total | , |  ·  | 4.86 out of 5 average rating | 4.86
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-32646786/original/5fa48175-ec51-4c61-83b9-266ab837962a.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/32646786?check_in=2026-12-18&check_out=2026-12-20&photo_id=2660605823
Card Executive Hotel Le Soleil
Observed labels: Executive Hotel Le Soleil | $828 CAD total |   | $828 CAD total | , |  ·  | 4.88 out of 5 average rating | 4.88
Photo: https://a0.muscache.com/im/pictures/BnbProperty/BnbProperty-1701478825418872058/original/5ca3c2ae-8969-457b-8e32-89563e7c262c.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1699582835980108221?check_in=2026-10-23&check_out=2026-10-25&photo_id=2666647896
Card Room in Vancouver
Observed labels: Guest favourite | Guest favourite | Room in Vancouver | Nov 13–15 | $275 CAD total |   | $275 CAD total | , |  ·  | 4.94 out of 5 average rating | 4.94
Photo: https://a0.muscache.com/im/pictures/1a043826-9b73-457a-9c34-0c72a706a151.jpg?im_w=480
Link: https://www.airbnb.ca/rooms/20799287?check_in=2026-11-13&check_out=2026-11-15&photo_id=370183044
Card EXchange Hotel Vancouver
Observed labels: EXchange Hotel Vancouver | $785 CAD total |   | $785 CAD total | , |  ·  | 4.85 out of 5 average rating | 4.85
Photo: https://a0.muscache.com/im/pictures/BnbProperty/BnbProperty-1700025435063662140/original/d86132d1-cf21-4626-8069-7c7748420184.jpeg?im_w=320
Link: https://www.airbnb.ca/rooms/1693772925819433419?check_in=2026-10-23&check_out=2026-10-25&photo_id=2663447173
Card Guest suite in Vancouver
Observed labels: Guest favourite | Guest favourite | Guest suite in Vancouver | Nov 6–8 | $347 CAD total |   | $347 CAD total | , |  ·  | 4.98 out of 5 average rating | 4.98
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1130105894987703195/original/2f39fa07-2379-414c-b9fb-88e703ea2929.jpeg?im_w=320
Link: https://www.airbnb.ca/rooms/1130105894987703195?check_in=2026-11-06&check_out=2026-11-08&photo_id=2772538965
Card Guest suite in Vancouver
Observed labels: Guest favourite | Guest favourite | Guest suite in Vancouver | Nov 13–15 | $301 CAD total |   | $301 CAD total | , |  ·  | 4.83 out of 5 average rating | 4.83
Photo: https://a0.muscache.com/im/pictures/46381238/f5a20440_original.jpg?im_w=240
Link: https://www.airbnb.ca/rooms/3678989?check_in=2026-11-13&check_out=2026-11-15&photo_id=28979959
Card Home in West Vancouver
Observed labels: Guest favourite | Guest favourite | Home in West Vancouver | Nov 6–8 | $997 CAD total |   | $997 CAD total | , |  ·  | 4.98 out of 5 average rating | 4.98
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1458180758155324907/original/54f0c639-c4e0-4e02-9a89-ce0cbb89a4fb.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/1458180758155324907?check_in=2026-11-06&check_out=2026-11-08&photo_id=2469483744
Card Apartment in Vancouver
Observed labels: Guest favourite | Guest favourite | Apartment in Vancouver | Oct 30–Nov 1 | $1,292 CAD total |   | $1,292 CAD total | , |  ·  | 5.0 out of 5 average rating | 5.0
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1746649758225675833/original/efdbb142-19d2-4ff8-b5bb-94a143840b49.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/1746649758225675833?check_in=2026-10-30&check_out=2026-11-01&photo_id=2762268810

ROW Available next month in Busan | Available next month in Busan
South Korean beach and port city
Card Apartment in Dong-gu
Observed labels: Guest favourite | Guest favourite | Apartment in Dong-gu | Nov 27–29 | $249 CAD total |   | $249 CAD total | , |  ·  | 4.88 out of 5 average rating | 4.88
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-U3RheVN1cHBseUxpc3Rpbmc6MTEyNTMyMDU2OTAwNzQyNjM5OQ%3D%3D/original/529ac8b8-f78f-4a71-8328-ef611b5516f9.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1125320569007426399?check_in=2026-11-27&check_out=2026-11-29&photo_id=2047307223
Card Room in Busanjin-gu
Observed labels: Guest favourite | Guest favourite | Room in Busanjin-gu | Nov 27–29 | $155 CAD total |   | $155 CAD total | , |  ·  | 4.95 out of 5 average rating | 4.95
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1695960707785726999/original/a7edced5-380e-438e-9184-ba546fbd747b.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1695960707785726999?check_in=2026-11-27&check_out=2026-11-29&photo_id=2666086416
Card Home in Jung-gu
Observed labels: Guest favourite | Guest favourite | Home in Jung-gu | Nov 20–22 | $506 CAD total |   | $506 CAD total | , |  ·  | 5.0 out of 5 average rating | 5.0
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1668153694750261205/original/4a766517-a372-4fed-bea2-a390cf52be4b.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1668153694750261205?check_in=2026-11-20&check_out=2026-11-22&photo_id=2664640939
Card Home in Suyeong-gu
Observed labels: Guest favourite | Guest favourite | Home in Suyeong-gu | Nov 27–29 | $312 CAD total |   | $312 CAD total | , |  ·  | 4.97 out of 5 average rating | 4.97
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-968008962561816389/original/d8dda498-5526-435a-ad15-0e6122f50f34.jpeg?im_w=320
Link: https://www.airbnb.ca/rooms/968008962561816389?check_in=2026-11-27&check_out=2026-11-29&photo_id=1728840413
Card Room in Suyeong-gu
Observed labels: Guest favourite | Guest favourite | Room in Suyeong-gu | Nov 27–29 | $883 CAD total |   | $883 CAD total | , |  ·  | 4.92 out of 5 average rating | 4.92
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1754611007391472164/original/653e2e04-9c58-4754-bb31-2797a4bf8b16.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1754611007391472164?check_in=2026-11-27&check_out=2026-11-29&photo_id=2778953713
Card Apartment in Suyeong-gu
Observed labels: Guest favourite | Guest favourite | Apartment in Suyeong-gu | Nov 13–15 | $692 CAD total |   | $692 CAD total | , |  ·  | 4.99 out of 5 average rating | 4.99
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1132242941765156298/original/bbde7293-52b8-479c-83cf-43a38be6fc6b.jpeg?im_w=320
Link: https://www.airbnb.ca/rooms/1132242941765156298?check_in=2026-11-13&check_out=2026-11-15&photo_id=1908131484
Card Home in Suyeong-gu
Observed labels: Guest favourite | Guest favourite | Home in Suyeong-gu | Nov 13–15 | $506 CAD total |   | $506 CAD total | , |  ·  | 5.0 out of 5 average rating | 5.0
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1447718714676835698/original/f3c36757-7255-4e46-9dc4-ebfb108a6305.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/1447718714676835698?check_in=2026-11-13&check_out=2026-11-15&photo_id=2494489766
Card Apartment in Haeundae-gu
Observed labels: Apartment in Haeundae-gu | Nov 27–29 | $259 CAD total |   | $259 CAD total | , |  ·  | 4.93 out of 5 average rating | 4.93
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-854166305333708690/original/c1dcbe59-3812-48ac-a10d-7e625ee82ddf.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/854166305333708690?check_in=2026-11-27&check_out=2026-11-29&photo_id=2739292614

ROW Available next month in Kyoto | Available next month in Kyoto
Ancient temples and shrines
Card Rental unit in Shimogyo-ku
Observed labels: Guest favourite | Guest favourite | Rental unit in Shimogyo-ku | $442 CAD total |   | $442 CAD total | , |  ·  | 4.92 out of 5 average rating | 4.92
Photo: https://a0.muscache.com/im/pictures/BnbProperty/BnbProperty-1715238778064899971/original/56454a56-e694-4fcd-bb3c-e9512f22d212.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1364382005540231413?check_in=2026-11-06&check_out=2026-11-08&photo_id=2695266730
Card Home in Minami Ward
Observed labels: Guest favourite | Guest favourite | Home in Minami Ward | Nov 13–15 | $577 CAD total |   | $577 CAD total | , |  ·  | 4.95 out of 5 average rating | 4.95
Photo: https://a0.muscache.com/im/pictures/hosting/Hosting-1214243381661088835/original/3a766b70-f76c-4d57-8e59-81177618d7ef.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1214243381661088835?check_in=2026-11-13&check_out=2026-11-15&photo_id=2005822240
Card Rental unit in Higashiyama-ku
Observed labels: Rental unit in Higashiyama-ku | $398 CAD total |   | $398 CAD total | , |  ·  | 4.79 out of 5 average rating | 4.79
Photo: https://a0.muscache.com/im/pictures/BnbProperty/BnbProperty-1715237538047706638/original/a1f99a37-72fd-4212-a3eb-00d717d22f8a.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1587443077550186515?check_in=2026-11-06&check_out=2026-11-08&photo_id=2695067161
Card Home in Kamigyo Ward
Observed labels: Guest favourite | Guest favourite | Home in Kamigyo Ward | Nov 6–8 | $674 CAD total |   | $674 CAD total | , |  ·  | 4.95 out of 5 average rating | 4.95
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-1041858369279250258/original/c4f44586-10e3-4424-804c-7d0b67805c1a.jpeg?im_w=480
Link: https://www.airbnb.ca/rooms/1041858369279250258?check_in=2026-11-06&check_out=2026-11-08&photo_id=1840946465
Card Townhouse in Kyoto
Observed labels: Guest favourite | Guest favourite | Townhouse in Kyoto | Nov 13–15 | $479 CAD total |   | $479 CAD total | , |  ·  | 4.94 out of 5 average rating | 4.94
Photo: https://a0.muscache.com/im/pictures/667e530f-c13e-4a01-9d1f-f7eafe168969.jpg?im_w=480
Link: https://www.airbnb.ca/rooms/2994040?check_in=2026-11-13&check_out=2026-11-15&photo_id=130247586
Card Home in Higashiyama-ku
Observed labels: Guest favourite | Guest favourite | Home in Higashiyama-ku | Nov 6–8 | $537 CAD total |   | $537 CAD total | , |  ·  | 4.95 out of 5 average rating | 4.95
Photo: https://a0.muscache.com/im/pictures/905a9cd2-8bc1-427d-b4ff-8599daa1f748.jpg?im_w=240
Link: https://www.airbnb.ca/rooms/41075404?check_in=2026-11-06&check_out=2026-11-08&photo_id=937030996
Card Home in Fushimi-ku
Observed labels: Guest favourite | Guest favourite | Home in Fushimi-ku | Nov 6–8 | $1,007 CAD total |   | $1,007 CAD total | , |  ·  | 4.99 out of 5 average rating | 4.99
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-1338396533065289653/original/f160cc8c-e780-47f7-a5e7-8b4688883439.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/1338396533065289653?check_in=2026-11-06&check_out=2026-11-08&photo_id=2072500362
Card Townhouse in Kyoto
Observed labels: Guest favourite | Guest favourite | Townhouse in Kyoto | Nov 6–8 | $683 CAD total |   | $683 CAD total | , |  ·  | 4.94 out of 5 average rating | 4.94
Photo: https://a0.muscache.com/im/pictures/miso/Hosting-43987995/original/b82326c2-df75-482a-bb2e-ce857dbd8cd8.jpeg?im_w=720
Link: https://www.airbnb.ca/rooms/43987995?check_in=2026-11-06&check_out=2026-11-08&photo_id=1366939238

Popular destinations (first observed visible grid):
Penticton  | House rentals https://www.airbnb.ca/penticton-canada/stays/houses
Las Vegas  | Apartment rentals https://www.airbnb.ca/las-vegas-nv/stays/apartments
Oakville  | Monthly Rentals https://www.airbnb.ca/oakville-canada/stays/monthly
Scarborough  | Vacation rentals https://www.airbnb.ca/scarborough-toronto-canada/stays
Vancouver Island  | Cabin rentals https://www.airbnb.ca/vancouver-island-canada/stays/cabins
Montreal  | Pet-friendly rentals https://www.airbnb.ca/montreal-canada/stays/pet-friendly
Fernie  | Apartment rentals https://www.airbnb.ca/fernie-canada/stays/apartments
Mexico City Cabin rentals https://www.airbnb.ca/mexico-city/stays/cabins
Red Deer Monthly Rentals https://www.airbnb.ca/red-deer-canada/stays/monthly
Richmond Pet-friendly rentals https://www.airbnb.ca/richmond-canada/stays/pet-friendly
North York Apartment rentals https://www.airbnb.ca/north-york-toronto-canada/stays/apartments
Los Angeles Villa rentals https://www.airbnb.ca/los-angeles-ca/stays/villas
Newfoundland Apartment rentals https://www.airbnb.ca/newfoundland-canada/stays/apartments
Winnipeg Vacation rentals https://www.airbnb.ca/winnipeg-canada/stays
Quebec City Condo rentals https://www.airbnb.ca/quebec-city-canada/stays/condos
Halifax Condo rentals https://www.airbnb.ca/halifax-canada/stays/condos
Collingwood Condo rentals https://www.airbnb.ca/collingwood-canada/stays/condos
Pickering Pet-friendly rentals https://www.airbnb.ca/pickering-canada/stays/pet-friendly

Do not claim output has been visually verified or matches the official site. Later browser-based inspection and corrections are separate. This is an independent educational reconstruction, not the Airbnb service. Use only free dependencies, do not add tracking, accounts, purchase, booking, or fabricated campaigns. Generate MOBILE layout at390px, not a squeezed desktop screen.
```

## 後續校正規格（本段尚未另送出 Stitch）

依10月10日加拿大英文公開首頁的完整桌面1440×900與390×844參照重製，保留十列房源、80張當日公開照片與89項選用原始素材，不臆造房源、價格或帳戶狀態。使用Cereal字型、All／Homes／Experiences／Services、Where／When／Who搜尋、首屏／縮小固定導覽、getaway目的地與完整頁尾。窄版重排與卡片裁切必須依實際PNG，不把桌面UA結果說成實體手機。

保留原生請求、完整回應、十次查詢及10月11日唯讀查詢紀錄；原DESKTOP逾時仍未完成，新增窄版工作已有真正輸出但device回錯且有placeholder，不能把它說成成功MOBILE。兩次請求、完整原始HTML／PNG分開保存；如再校正，仍須以當前雜湊重新查看完整桌面與窄版。不得因頁高、文字或圖片載入相同而宣稱與官方一致。

微調卡片圖示、標籤間距與箭頭／愛心時需重新檢查畫面。搜尋／分類、getaway頁籤、語言／貨幣、最愛／帳戶及預訂服務未完整重製；不能虛構已可用的後端。保持研究免費，列明地區／時間／動畫／互動與部署限制。
