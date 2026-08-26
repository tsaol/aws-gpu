#!/usr/bin/env python3
"""检查 index.html 显示的统计值与 data/ 是否一致。

背景：index.html 是手工维护的，「最后更新」和「GPU 实例总数」曾经写死在 HTML 里。
2026-08 发现页面显示 2026-01-21 / 30+，而 data/ 实际是 2026-04-25 / 91 条，
两边漂了四个月没人发现。修法是让页面从 data/meta.js 读，本测试守住这个不变量。

用法：
    python3 scripts/test_meta_consistency.py
退出码 0 表示全部通过，非 0 表示有不一致。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'
META = ROOT / 'data' / 'meta.js'
ALL_DATA = ROOT / 'data' / 'all_gpu_instances.js'

failures = []
checks = 0


def check(name, cond, detail=''):
    global checks
    checks += 1
    if cond:
        print(f'  PASS  {name}')
    else:
        print(f'  FAIL  {name}' + (f' — {detail}' if detail else ''))
        failures.append(name)


def load_js_object(path, var_name):
    """从 `const X = {...};` 或 `const X = [...];` 里取出 JSON。"""
    text = path.read_text(encoding='utf-8')
    m = re.search(rf'const\s+{var_name}\s*=\s*', text)
    if not m:
        raise ValueError(f'{path.name}: 找不到 {var_name}')
    body = text[m.end():].rstrip()
    if body.endswith(';'):
        body = body[:-1]
    return json.loads(body)


print('检查 index.html 与 data/ 的统计一致性\n')

# --- 前置：文件都在 ---
check('data/meta.js 存在', META.exists(),
      '需要先跑 python3 scripts/update_all.py --convert')
check('data/all_gpu_instances.js 存在', ALL_DATA.exists())
check('index.html 存在', INDEX.exists())
if failures:
    print(f'\n{len(failures)} 项失败，无法继续')
    sys.exit(1)

meta = load_js_object(META, 'gpuDataMeta')
instances = load_js_object(ALL_DATA, 'allGPUInstances')
html = INDEX.read_text(encoding='utf-8')

# --- meta 自身要和真实数据对得上 ---
check('meta.totalInstances 等于实际条目数',
      meta['totalInstances'] == len(instances),
      f"meta={meta['totalInstances']} 实际={len(instances)}")

check('meta.lastUpdated 是 YYYY-MM-DD',
      bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(meta.get('lastUpdated', '')))),
      f"got {meta.get('lastUpdated')!r}")

fams = {i['name'].split('.')[0] for i in instances if i.get('name')}
check('meta.totalFamilies 等于实际家族数',
      meta['totalFamilies'] == len(fams),
      f"meta={meta['totalFamilies']} 实际={len(fams)}")

# --- index.html 必须走动态路径，不能再写死 ---
check('index.html 引入了 data/meta.js',
      'src="data/meta.js"' in html)

check('存在 #last-updated 占位元素',
      'id="last-updated"' in html)

check('存在 #total-instances 占位元素',
      'id="total-instances"' in html)

check('有 JS 写入 #last-updated',
      re.search(r"getElementById\(['\"]last-updated['\"]\)", html) is not None,
      '占位元素存在但没人赋值，这正是原 bug 的形态')

check('有 JS 写入 #total-instances',
      re.search(r"getElementById\(['\"]total-instances['\"]\)", html) is not None,
      '占位元素存在但没人赋值，这正是原 bug 的形态')

# --- HTML 里的兜底值不能与 data/ 矛盾 ---
m = re.search(r'id="last-updated"[^>]*>([^<]*)<', html)
if m:
    fallback = m.group(1).strip()
    check('#last-updated 兜底值与 meta 一致',
          fallback in ('-', '', meta['lastUpdated']),
          f"HTML={fallback!r} meta={meta['lastUpdated']!r}；"
          '兜底值若过期，JS 失效时页面会显示错误日期')

m = re.search(r'id="total-instances"[^>]*>([^<]*)<', html)
if m:
    fallback = m.group(1).strip()
    check('#total-instances 兜底值与 meta 一致',
          fallback in ('-', '', str(meta['totalInstances'])),
          f"HTML={fallback!r} meta={meta['totalInstances']}")

# --- 页面正文里不该再出现游离的硬编码日期 ---
stray = [d for d in set(re.findall(r'最后更新[:：]\s*(\d{4}-\d{2}-\d{2})', html))
         if d != meta['lastUpdated']]
check('正文没有过期的硬编码「最后更新」日期', not stray,
      f'发现 {stray}')

print(f'\n{checks - len(failures)}/{checks} 通过')
if failures:
    print('失败项: ' + ', '.join(failures))
    sys.exit(1)
sys.exit(0)
