#!/usr/bin/env python3
"""Record the October 5 references, observed checks, and unfinished work."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / '.stitch-work/current-official'


def write(name, data):
    (WORK/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')


def main():
    runway_geometry={
        'desktop':{'viewport':[1280,720],'body_height':4991,
                   'hero_title':[58.75,299.53125,520.4921875,43.890625],
                   'platform_title':[128,883.421875,1024,116.484375],
                   'platform_heading_y':[1055.90625,1055.90625,1055.90625]},
        'mobile':{'viewport':[390,844],'body_height':9334,
                  'hero_title':[50.5859375,219.609375,288.828125,64.390625],
                  'platform_title':[20,934,350,158.375],
                  'platform_heading_y':[1148.375,1725.921875,2284.1796875]},
    }
    uber_geometry={
        'desktop':{'viewport':[1280,720],'hero_title':[64,160,459,128],
                   'section_heading_y':{'explore':651,'account':1242.875,'reserve':1642.75,
                                        'city_hub':2270.625,'driver':2863.625,'business':3561.625,'apps':4088.625},
                   'footer_heading_y':4727.0625,'body_height':5446},
        'mobile':{'viewport':[390,844],'hero_title':[24,136,342,88],
                  'section_heading_y':{'explore':560,'account':923.234375,'reserve':1510.46875,
                                       'city_hub':2342.703125,'driver':2950.703125,'business':3692.703125,'apps':4390.703125},
                  'footer_heading_y':[5092.140625,5439.078125,5894.015625,6060.953125],
                  'body_height':6756},
    }
    common={'observed_at':'2026-10-05','observation_method':'Dated live official DOM and browser screenshots; independent public HTTP status recorded separately.',
            'viewports':{'desktop':[1280,720],'mobile':[390,844]},
            'public_deployment_comparison':'Pending. Native Sites API confirms a public audience, while the saved browser permission blocks the deployed user-site domain.'}
    write('runwayml-reference.json',{**common,'reference_url':'https://runway.com/',
        'browser_entry_url':'https://runwayml.com/','reference_basis':'Current public homepage after the brand-domain redirect',
        'source_snapshot':'runwayml-source-current.html','source_metadata':'runwayml-source-metadata.json',
        'source_body_preserved':True,'design_analysis':'runwayml-design-system.md',
        'browser_source':'runwayml-browser-source.json','asset_provenance':'runwayml-asset-provenance.json',
        'player_provenance':'runwayml-player-provenance.json','geometry':runway_geometry,
        'font_family':'ABC Normal','news_observed':['Introducing Team Plan','Introducing Solaris','The Next Phase of Enterprise Video Generation','Introducing GWM Worlds 2']})
    write('uber-reference.json',{**common,'reference_url':'https://www.uber.com/ca/en/',
        'reference_basis':'Current public Canadian-English URL; dated browser geographic variant',
        'geographic_variant':'Taipei, CA; Uber Formosa Co. Ltd. footer',
        'source_metadata':'uber-source-metadata.json','source_http_status':406,'source_body_preserved':False,
        'browser_source':'uber-browser-source.json','design_analysis':'uber-design-system.md',
        'asset_provenance':'uber-asset-provenance.json','geometry':uber_geometry,
        'font_families':['Uber Move','Uber Move Text'],
        'sections_observed':['Go anywhere with Uber','Explore what you can do with Uber','Log in to see your account details','Plan for later','Planning your next getaway?','Drive when you want, make what you need','The Uber you know, reimagined for business','It’s easier in the apps']})
    verified={
        'runwayml':[
            'Official homepage inspected at 1280×720 and 390×844; dated independent HTTP 200 HTML snapshot retained.',
            'Three genuine native Stitch UI exports retained unchanged with screen IDs, request strings, checksums and actual thumbnail sizes. MOBILE generation and one correction both returned DESKTOP metadata; this is not presented as successful mobile generation.',
            'Original public source CSS, wordmark, partner marks, news artwork and three ABC Normal fonts retained. The generator-created robot image is not used in the displayed draft.',
            'Desktop/mobile hero and platform headings and default body heights match the recorded official reference. No horizontal overflow at both checked widths.',
            'Five Creative tabs selected in order with exactly one visible panel and one video per panel; three platform buttons and three Dev tabs tested.',
            'Mobile menu opened at x0 y64 width390; Escape closed it. No console error in the checked mobile session.',
        ],
        'uber':[
            'Official Canadian URL inspected at 1280×720 and 390×844. Independent HTTP request returned 406; no raw source HTML is claimed.',
            'Four genuine native Stitch UI exports retained unchanged with IDs, request strings, checksums and thumbnail sizes; one correction returned a MOBILE screen and an additional DESKTOP screen.',
            'Four original Uber font files saved with SHA-256 provenance. Official hero/account/travel illustrations, service icons, Reserve background and driver/business imagery used from observed public URLs.',
            'Hero and all seven later section heading positions match the recorded official reference at both checked viewports. All four footer heading positions match at both widths.',
            'Pickup and destination accept local preview text. Date and time accept a local value; Next and price/account actions point to the original official service without submitting a local request.',
            'Mobile menu opened and Escape closed it. No horizontal overflow or completed broken image in the checked mobile session; no console error in the checked session.',
        ],
    }
    remaining={
        'runwayml':[
            'Exact frame-by-frame media playback, transitions and timing. The checked local hero video remained readyState 0/currentTime 0 with its original poster visible; actual playback is not verified.',
            'Complete desktop/mobile comparison of alternate platform states, Robotics card icons, documentation CTA styling, news cards and footer.',
            'Exact native mega-menu, mobile navigation, language and cookie controls; current menu is a simplified verified-link panel.',
            'A native Stitch MOBILE screen, tablet breakpoints and public deployment comparison.',
        ],
        'uber':[
            'Complete visual review of navigation, all original icons, app-store badges, date/time selector styling, city selection and footer/legal spacing.',
            'Full official ride, location, reservation, authentication and regional interactions. The static study opens the official service for these actions.',
            'Other geographic and language variants, tablet breakpoints and public deployment comparison.',
            'The checked bodies were 5430px desktop and 6720px mobile versus 5446px and 6756px references; later legal/store/footer details are not marked matched.',
        ],
    }
    discrepancies={
        'runwayml':[
            'Desktop export substituted Space Grotesk/Inter and a generated robot-cooking image; its claims of exact source fidelity are not accepted as evidence.',
            'Both requests for mobile returned DESKTOP metadata. All original exports and correction outputs are retained; no additional blind retry was made.',
        ],
        'uber':[
            'The desktop generator changed the heading to Go anywhere and get anything and omitted or replaced account, Reserve and City Hub sections.',
            'Mobile outputs also changed copy and invented City Hub/app-download details. The displayed draft follows the independently observed official copy and artwork.',
        ],
    }
    progress=json.loads((WORK/'progress.json').read_text())
    for brand in ['runwayml','uber']:
        geometry=runway_geometry if brand=='runwayml' else uber_geometry
        rendered=json.loads(json.dumps(geometry))
        if brand=='uber':
            rendered['desktop']['body_height']=5430
            rendered['mobile']['body_height']=6720
        review={'accepted':False,'reviewed_at':'2026-10-05','reference':brand+'-reference.json',
                'native_exports':brand+'-stitch-generated.json','asset_provenance':brand+'-asset-provenance.json',
                'verified':verified[brand],'remaining':remaining[brand],
                'native_export_discrepancies':discrepancies[brand],
                'rendered_measurements':rendered,'build_source':'scripts/refine_'+('runway' if brand=='runwayml' else brand)+'_draft.py',
                'draft_integrity':{'sha256':hashlib.sha256((WORK/(brand+'.html')).read_bytes()).hexdigest()}}
        write(brand+'-review.json',review)
        generated=json.loads((WORK/(brand+'-stitch-generated.json')).read_text())
        reference=json.loads((WORK/(brand+'-reference.json')).read_text())
        mobile=next((s['name'] for s in generated['screens'] if s['actual_device_type']=='MOBILE'),None)
        progress[brand]={'status':'in_visual_review','reference_url':reference['reference_url'],
            'observed_at':'2026-10-05','native_screen':generated['screens'][0]['name'],
            'native_mobile_screen':mobile,'stitch_project':generated['project']['name'],
            'stitch_design_system':generated['design_system'],'preview':brand+'.html',
            'reference':brand+'-reference.json','review':brand+'-review.json',
            'verified':verified[brand],'remaining':remaining[brand],
            'review_note':('10 月 5 日官網草稿；桌機與手機主要版面已校正，影片及完整互動仍待驗收。' if brand=='runwayml' else '10 月 5 日官網草稿；主要版面已校正，地域變體及完整互動仍待驗收。')}
    write('progress.json',progress)
    count=sum(p['status'] in ['in_visual_review','draft_unverified'] for p in progress.values())
    assert len(progress)==74 and count==58
    print(json.dumps({'drafts':count,'accepted':0,'remaining':74-count}))


if __name__=='__main__':
    main()
