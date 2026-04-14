"""Deep scan of all CapCut drafts for effects, transitions, animations"""
import json, os

base = r'C:\Users\DELL\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft'

all_transitions = []
all_effects = []
all_video_effects = []
all_animations = []
all_audio_effects = []
all_stickers = []
all_filters = []

for entry in os.listdir(base):
    draft = os.path.join(base, entry, 'draft_content.json')
    if not os.path.isfile(draft):
        continue
    try:
        d = json.load(open(draft, encoding='utf-8'))
    except:
        continue
    
    m = d.get('materials', {})
    
    # Transitions
    for t in m.get('transitions', []):
        all_transitions.append({
            'draft': entry,
            'name': t.get('name', ''),
            'resource_id': t.get('resource_id', ''),
            'effect_id': t.get('effect_id', ''),
            'duration': t.get('duration', 0),
            'category_name': t.get('category_name', ''),
            'is_overlap': t.get('is_overlap', False),
        })
    
    # Effects
    for e in m.get('effects', []):
        all_effects.append({
            'draft': entry,
            'name': e.get('name', ''),
            'resource_id': e.get('resource_id', ''),
            'effect_id': e.get('effect_id', ''),
            'category_name': e.get('category_name', ''),
            'type': e.get('type', ''),
        })
    
    # Video effects
    for v in m.get('video_effects', []):
        all_video_effects.append({
            'draft': entry,
            'name': v.get('name', ''),
            'resource_id': v.get('resource_id', ''),
            'effect_id': v.get('effect_id', ''),
        })
    
    # Audio effects
    for ae in m.get('audio_effects', []):
        all_audio_effects.append({
            'draft': entry,
            'name': ae.get('name', ''),
            'resource_id': ae.get('resource_id', ''),
            'effect_id': ae.get('effect_id', ''),
        })
    
    # Material animations - check deeply
    for a in m.get('material_animations', []):
        sub_anims = a.get('animations', [])
        for sa in sub_anims:
            all_animations.append({
                'draft': entry,
                'name': sa.get('name', ''),
                'resource_id': sa.get('resource_id', ''),
                'effect_id': sa.get('effect_id', sa.get('id', '')),
                'category_name': sa.get('category_name', ''),
                'type': sa.get('type', a.get('type', '')),
                'start': sa.get('start', 0),
                'duration': sa.get('duration', 0),
            })
    
    # Stickers
    for s in m.get('stickers', []):
        all_stickers.append({
            'draft': entry,
            'name': s.get('name', ''),
            'resource_id': s.get('resource_id', ''),
        })

    # Scan full materials for any key with resource_id patterns
    # Also look for filters inside 'videos' material adjustments
    for v in m.get('videos', []):
        if v.get('filter'):
            f = v['filter']
            if isinstance(f, dict) and f.get('resource_id'):
                all_filters.append({
                    'draft': entry,
                    'name': f.get('name', ''),
                    'resource_id': f.get('resource_id', ''),
                    'effect_id': f.get('effect_id', ''),
                })

# === REPORT ===
def print_section(title, items):
    if not items:
        print(f"\n{title}: (none found)")
        return
    print(f"\n{'='*60}")
    print(f"{title}: {len(items)} found")
    print(f"{'='*60}")
    seen = set()
    for item in items:
        key = item.get('resource_id', '') or item.get('name', '')
        if key in seen:
            continue
        seen.add(key)
        for k, v in item.items():
            if k != 'draft':
                print(f"  {k}: {v}")
        print(f"  (from draft: {item['draft']})")
        print()

print_section("TRANSITIONS", all_transitions)
print_section("EFFECTS", all_effects)
print_section("VIDEO EFFECTS", all_video_effects)
print_section("ANIMATIONS", all_animations)
print_section("AUDIO EFFECTS", all_audio_effects)
print_section("STICKERS", all_stickers)
print_section("FILTERS", all_filters)

# Summary
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  Transitions: {len(all_transitions)}")
print(f"  Effects: {len(all_effects)}")
print(f"  Video Effects: {len(all_video_effects)}")
print(f"  Animations: {len(all_animations)}")
print(f"  Audio Effects: {len(all_audio_effects)}")
print(f"  Stickers: {len(all_stickers)}")
print(f"  Filters: {len(all_filters)}")

# Save to JSON
output = {
    'transitions': all_transitions,
    'effects': all_effects,
    'video_effects': all_video_effects,
    'animations': all_animations,
    'audio_effects': all_audio_effects,
    'stickers': all_stickers,
    'filters': all_filters,
}
with open('capcut_discovered_data.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)
print("\nSaved to capcut_discovered_data.json")
