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

# --- 新家族的落地检查 ---
# 2026-08 数据源新增 g7，但三处配置都漏了它：GPU_MODELS 没有 'g7'（前缀匹配落到
# 'Unknown GPU'）、GPU_MEMORY 没有、FAMILY_INFO 没有（导致 generate_pages 跳过）。
# 数据里出现一个新家族时，这几项必须同时补齐，否则页面会显示 Unknown 或缺页。
sys.path.insert(0, str(ROOT / 'scripts'))
from config import GPU_MODELS, GPU_MEMORY, FAMILY_INFO  # noqa: E402

families = sorted({i['name'].split('.')[0] for i in instances if i.get('name')})

# u-p6e-gb200x36 / x72 是 GB200 UltraServer（整机柜规格，无 apiName、无独立
# 实例类型），首页由 P6e 那一行代表，不该要求它们有自己的详情页与配置。
ULTRASERVER_PREFIX = 'u-'
page_families = [f for f in families if not f.startswith(ULTRASERVER_PREFIX)]

unknown_gpu = sorted({i['name'].split('.')[0] for i in instances
                      if i.get('gpu') in (None, '', 'Unknown GPU')})
check('没有家族的 GPU 型号是 Unknown', not unknown_gpu,
      f'缺 GPU_MODELS 条目: {unknown_gpu}')

unknown_mem = sorted({i['name'].split('.')[0] for i in instances
                      if i.get('gpuMemory') in (None, '', 'Unknown')})
check('没有家族的 GPU 显存是 Unknown', not unknown_mem,
      f'缺 GPU_MEMORY 条目: {unknown_mem}')

no_info = [f for f in page_families if f not in FAMILY_INFO]
check('每个家族都有 FAMILY_INFO', not no_info,
      f'generate_pages 会跳过这些家族: {no_info}')

no_page = [f for f in page_families
           if not (ROOT / 'instances' / f'{f}.html').exists()]
check('每个家族都有详情页', not no_page,
      f'缺 instances/*.html: {no_page}')

# 前缀匹配的顺序陷阱：更长的键必须排在它的前缀之前，
# 否则 g7e.* 会先命中 'g7'、gr6f.* 会先命中 'gr6'。
keys = list(GPU_MODELS)
shadowed = [(long, short) for i, short in enumerate(keys)
            for long in keys[i + 1:] if long.startswith(short)]
check('GPU_MODELS 没有被前缀遮蔽的键', not shadowed,
      f'这些键永远匹配不到（需调整顺序）: {shadowed}')

# 首页表格是手写的，新家族要手动加行，否则数据有了但页面看不到
missing_row = [f for f in page_families
               if f'instances/{f}.html' not in html]
check('首页表格覆盖所有家族', not missing_row,
      f'数据里有但首页没链接: {missing_row}')

print(f'\n{checks - len(failures)}/{checks} 通过')
if failures:
    print('失败项: ' + ', '.join(failures))
    sys.exit(1)
sys.exit(0)
