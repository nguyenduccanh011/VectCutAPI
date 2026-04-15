"""Scan CapCut effect cache to extract all metadata"""
import json, os

base = r'C:\Users\DELL\AppData\Local\CapCut\User Data\Cache\effect'
results = []

for root, dirs, files in os.walk(base):
    if 'config.json' in files:
        path = os.path.join(root, 'config.json')
        try:
            d = json.load(open(path, encoding='utf-8'))
            name = d.get('name', '')
            version = d.get('version', '')
            links = d.get('effect', {}).get('Link', [])
            link_types = [l.get('type', '') for l in links]

            parts = os.path.relpath(root, base).split(os.sep)
            resource_id = parts[0] if parts else ''
            md5_folder = parts[1] if len(parts) > 1 else ''

            params = []
            for l in links:
                extra = l.get('extra', {})
                for p in extra.get('composer_param', []):
                    params.append(p.get('key', ''))

            results.append({
                'resource_id': resource_id,
                'md5': md5_folder,
                'name': name,
                'types': link_types,
                'params': params,
            })
        except:
            pass

print(f"Found {len(results)} effects in cache\n")

# Show effects with adjustable params
print("Effects with adjustable params:")
for r in results:
    if r['params']:
        rid = r['resource_id']
        n = r['name']
        p = r['params']
        print(f"  {rid}: {n} => {p}")

print()

# Now scan all draft_content.json to find transitions
print("=" * 60)
print("SCANNING DRAFTS FOR TRANSITIONS & EFFECTS")
print("=" * 60)

drafts_base = r'C:\Users\DELL\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft'
for entry in os.listdir(drafts_base):
    draft_file = os.path.join(drafts_base, entry, 'draft_content.json')
    if not os.path.isfile(draft_file):
        continue
    
    try:
        d = json.load(open(draft_file, encoding='utf-8'))
    except:
        continue

    materials = d.get('materials', {})
    
    # Transitions
    transitions = materials.get('transitions', [])
    if transitions:
        print(f"\n--- DRAFT: {entry} ---")
        print(f"  Transitions ({len(transitions)}):")
        for t in transitions:
            print(f"    name={t.get('name','?')}")
            print(f"    resource_id={t.get('resource_id','?')}")
            print(f"    effect_id={t.get('effect_id','?')}")
            print(f"    duration={t.get('duration',0)}")
            print(f"    category={t.get('category_name','?')}")
            print()
    
    # Effects
    effects = materials.get('effects', [])
    if effects:
        print(f"  Effects ({len(effects)}):")
        for e in effects:
            print(f"    name={e.get('name','?')}, rid={e.get('resource_id','?')}, eid={e.get('effect_id','?')}")
    
    # Video effects
    vfx = materials.get('video_effects', [])
    if vfx:
        print(f"  Video Effects ({len(vfx)}):")
        for v in vfx:
            print(f"    name={v.get('name','?')}, rid={v.get('resource_id','?')}, eid={v.get('effect_id','?')}")
    
    # Animations
    anims = materials.get('material_animations', [])
    if anims:
        print(f"  Animations ({len(anims)}):")
        for a in anims:
            for subtype in ['intro', 'outro', 'loop_animation']:
                if a.get(subtype):
                    data = a[subtype]
                    print(f"    [{subtype}] name={data.get('name','?')}, rid={data.get('resource_id','?')}, eid={data.get('effect_id','?')}")
    
    # Audio effects
    audio_fx = materials.get('audio_effects', [])
    if audio_fx:
        print(f"  Audio Effects ({len(audio_fx)}):")
        for ae in audio_fx:
            print(f"    name={ae.get('name','?')}, rid={ae.get('resource_id','?')}")

    # Stickers
    stickers = materials.get('stickers', [])
    if stickers:
        print(f"  Stickers ({len(stickers)}):")
        for s in stickers:
            print(f"    name={s.get('name','?')}, rid={s.get('resource_id','?')}")

    # Texts with animations
    texts = materials.get('texts', [])
    for tx in texts:
        if tx.get('content'):
            print(f"  Text: {tx.get('content','')[:50]}")

print("\n\nDONE.")
