# UI 测试

两份文件：

- **`ui-test-config.json`** — 手工维护的输入。加页面、加断言、加交互都改这里。
- **`ui-test-cases.json`** — 由 config 爬站生成的用例（当前 48 条），提交进仓库便于 CI 复跑
  和 review diff。config 改了要重新生成。

配套 skill 在 `~/.claude/skills/ui-test/`。

## 跑法

```bash
# 需要 Python 3.10+：bedrock-agentcore 的真 SDK 要求 >=3.10，
# 在 3.9 上 pip 只会装到一个 0.0.1 空壳（import 成功但没有子模块）
python3.11 -m venv ~/tmp/uitest-venv
~/tmp/uitest-venv/bin/pip install bedrock-agentcore playwright boto3 nest-asyncio
~/tmp/uitest-venv/bin/python -m playwright install chromium

VENV=~/tmp/uitest-venv/bin/python
SKILL=~/.claude/skills/ui-test/scripts

# Phase 1：爬站生成用例（改了 config 才需要）
$VENV $SKILL/build_tests.py --config tests/ui-test-config.json \
                            --output tests/ui-test-cases.json

# Phase 2：执行
$VENV $SKILL/run_tests.py --cases tests/ui-test-cases.json \
                          --screenshot-dir ~/tmp/gpu-ui-screenshots
```

## 这套用例在守什么

除了常规的 200 / 文本 / 元素 / 响应式，重点是几条**回归守卫**，
对应的都是真实发生过的 bug：

| 断言 | 防的是什么 |
|---|---|
| `expect_no_text: "Unknown GPU"` | 数据源新增家族但 `GPU_MODELS` 没补条目（g7 曾如此） |
| `expect_no_text: "最后更新: 2026-01-21"` | 页面日期写死、与 `data/` 漂了四个月 |
| `expect_no_text: "30+"` | 实例总数写死，不随数据变化 |
| 三个 `order_changes` 交互 | 表头带 `.sortable` 和箭头但没绑 JS，点了没反应 |
| `a[href='instances/g7.html']` 存在 | 新家族进了数据却没进首页表格 |

`scripts/test_meta_consistency.py` 是同一批不变量的静态检查版（不需要浏览器，
CI 里更快）。两者互补：那个查源码一致性，这个查渲染后的真实行为。

## 注意

**同一页的多个 interaction 共用一次页面加载。** runner 只在 URL 变化时才重新导航，
所以往搜索框 `fill` 之后，筛选状态会一直保留到该页所有后续交互。
config 里的顺序是刻意的：先导航断言 → 再排序 → 最后筛选 → 收尾点「清空筛选」。
如果把筛选提前，后面的用例会去等一个在 DOM 里但被筛掉（不可见）的元素，30 秒超时。
