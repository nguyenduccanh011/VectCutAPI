import re

src = open('pyJianYingDraft/metadata/capcut_transition_meta.py', encoding='utf-8').read()

# Transition_meta("Name", is_vip_bool, resource_id, ...)
matches = re.findall(r'Transition_meta\("([^"]+)",\s*(True|False),', src)

vip = [n for n, v in matches if v == 'True']
free = [n for n, v in matches if v == 'False']

print(f'is_vip=True  (VIP/tải về): {len(vip)}')
print(f'is_vip=False (miễn phí):   {len(free)}')
print()
print('VIP transitions (cần tải về/mua):')
for n in sorted(set(vip)):
    print(f'  - {n}')
print()
print('Free transitions (dùng được ngay):')
for n in sorted(set(free)):
    print(f'  - {n}')
