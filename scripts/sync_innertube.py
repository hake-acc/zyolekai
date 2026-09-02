#!/usr/bin/env python3
"""
ZyoleKai Automated YouTube InnerTube Synchronization Engine
Pulls live, keyless, real-time statistics (subscribers, views, video counts, avatars)
from YouTube for all 15 signed ZyoleKai creators and saves to src/data/creators.json.
"""

import os
import sys
import json
import re
import time

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

def parse_views_number(v_str):
    if not v_str: return 0
    v_str = str(v_str).replace(',', '').strip()
    match = re.search(r'([\d.]+)\s*([KMBkmb])?', v_str)
    if not match: return 0
    num = float(match.group(1))
    unit = match.group(2)
    if unit:
        unit = unit.upper()
        if unit == 'K': num *= 1_000
        elif unit == 'M': num *= 1_000_000
        elif unit == 'B': num *= 1_000_000_000
    return int(num)

def format_short_number(num):
    if num >= 1_000_000_000:
        val = num / 1_000_000_000
        return f"{val:.1f}B".replace(".0B", "B")
    elif num >= 1_000_000:
        val = num / 1_000_000
        return f"{val:.1f}M".replace(".0M", "M")
    elif num >= 1_000:
        val = num / 1_000
        return f"{val:.1f}K".replace(".0K", "K")
    return str(num)

def run_sync():
    print("=== [ZyoleKai InnerTube Auto-Sync Engine] ===")
    
    try:
        import innertube
    except ImportError:
        print("[!] Note: 'innertube' package not found in current environment. Using cached creators data.")
        return 0

    import urllib.request
    try:
        from PIL import Image
        has_pil = True
    except ImportError:
        has_pil = False

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, '..'))
    data_path = os.path.join(project_root, 'src', 'data', 'creators.json')
    avatars_dir = os.path.join(project_root, 'public', 'avatars')
    os.makedirs(avatars_dir, exist_ok=True)

    if not os.path.exists(data_path):
        print(f"[!] Warning: {data_path} not found.")
        return 0

    with open(data_path, 'r', encoding='utf-8') as f:
        creators = json.load(f)

    try:
        client = innertube.InnerTube('WEB')
    except Exception as e:
        print(f"[!] Failed to initialize InnerTube client: {e}. Preserving cache.")
        return 0

    updated_count = 0

    for idx, c in enumerate(creators):
        cid = c.get('channelId')
        name = c.get('name', 'Unknown')
        slug = c.get('slug', f'creator-{idx+1}')

        if not cid:
            continue

        print(f"[{idx+1}/{len(creators)}] Syncing {name} ({cid})...")

        try:
            data = client.browse(browse_id=cid)
            ph = data.get('header', {}).get('pageHeaderRenderer', {}).get('content', {}).get('pageHeaderViewModel', {})

            # 1. Avatar extraction
            avatar_sources = ph.get('image', {}).get('decoratedAvatarViewModel', {}).get('avatar', {}).get('avatarViewModel', {}).get('image', {}).get('sources', [])
            if avatar_sources:
                remote_avatar_url = avatar_sources[-1]['url']
                dest_png = os.path.join(avatars_dir, f"{slug}.png")
                dest_webp = os.path.join(avatars_dir, f"{slug}.webp")
                try:
                    req = urllib.request.Request(remote_avatar_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=8) as resp:
                        with open(dest_png, 'wb') as out_f:
                            out_f.write(resp.read())
                    if has_pil:
                        im = Image.open(dest_png)
                        im.save(dest_webp, 'WEBP', lossless=True, quality=100)
                    c['avatar'] = f"/avatars/{slug}.webp"
                    c['avatarUrl'] = f"/avatars/{slug}.webp"
                except Exception as av_err:
                    print(f"   [!] Avatar download warning for {name}: {av_err}")

            # 2. Subscribers and video counts
            meta_rows = ph.get('metadata', {}).get('contentMetadataViewModel', {}).get('metadataRows', [])
            for row in meta_rows:
                for part in row.get('metadataParts', []):
                    txt = part.get('text', {}).get('content', '')
                    if 'subscriber' in txt.lower():
                        c['subscribers'] = txt
                        sub_n = parse_views_number(txt)
                        if sub_n > 0:
                            c['subscribersShort'] = format_short_number(sub_n)
                    elif 'video' in txt.lower():
                        c['videoCount'] = txt

            # 3. Total views via about continuation token
            desc = ph.get('description', {}).get('descriptionPreviewViewModel', {})
            cmd = desc.get('rendererContext', {}).get('commandContext', {}).get('onTap', {}).get('innertubeCommand', {})
            ep = cmd.get('showEngagementPanelEndpoint', {})
            panel = ep.get('engagementPanel', {}).get('engagementPanelSectionListRenderer', {})
            contents = panel.get('content', {}).get('sectionListRenderer', {}).get('contents', [])

            token = None
            for item in contents:
                cont = item.get('itemSectionRenderer', {}).get('contents', [{}])[0].get('continuationItemRenderer', {})
                t = cont.get('continuationEndpoint', {}).get('continuationCommand', {}).get('token')
                if t:
                    token = t
                    break

            if token:
                cont_res = client.browse(continuation=token)
                raw_cont = json.dumps(cont_res)
                views_matches = re.findall(r'([\d,]+)\s+views', raw_cont)
                if views_matches:
                    total_views_num = int(views_matches[0].replace(',', ''))
                    c['totalViews'] = f"{total_views_num:,} views"
                    c['totalViewsShort'] = format_short_number(total_views_num)

            print(f"   [OK] {name} synced: Subs={c.get('subscribersShort')}, Videos={c.get('videoCount')}")
            updated_count += 1
            time.sleep(0.3)
        except Exception as err:
            print(f"   [!] Error syncing {name}: {err}")

    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(creators, f, indent=2)

    print(f"\n[OK] Successfully updated {updated_count}/{len(creators)} creators with live InnerTube data!")
    return 0

if __name__ == '__main__':
    sys.exit(run_sync())
