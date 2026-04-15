import json

path = r'C:\Users\DELL\AppData\Local\CapCut\User Data\Projects\com.lveditor.draft\dfd_cat_1776073660_3c2f9a7a\draft_content.json'
with open(path, 'r', encoding='utf-8') as f:
    d = json.load(f)

print('TOP-LEVEL KEYS:')
for k in d.keys():
    val = d[k]
    if isinstance(val, list):
        print(f'  {k}: list[{len(val)}]')
    elif isinstance(val, dict):
        sub = list(val.keys())[:5]
        print(f'  {k}: dict keys={sub}')
    else:
        print(f'  {k}: {type(val).__name__} = {str(val)[:60]}')

print()
print('materials sub-keys:')
for k, v in d.get('materials', {}).items():
    if isinstance(v, list):
        print(f'  materials.{k}: list[{len(v)}]')
    else:
        print(f'  materials.{k}: {type(v).__name__}')

print()
print('tracks:')
for t in d.get('tracks', []):
    segs = t.get('segments', [])
    ttype = t.get('type')
    tname = t.get('name', '')
    print(f'  type={ttype} name={repr(tname)} segments={len(segs)}')

print()
print('canvas_config:')
cc = d.get('canvas_config', {})
print(f'  {cc.get("width")}x{cc.get("height")} ratio={cc.get("ratio")}')
