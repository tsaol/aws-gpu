#!/usr/bin/env python3
"""
生成 GPU 实例详情页面
自动生成所有 GPU 实例系列的 HTML 详情页面
"""
import json
import re
import sys
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    DATA_DIR, INSTANCES_DIR, INDEX_FILE,
    FAMILY_INFO, get_current_date
)
from utils import read_js_data, colorize

# HTML 模板（保持与原有格式一致）
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - AWS GPU Instance Comparison</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background: #f5f7fa; color: #1a202c; line-height: 1.6; }}
        .container {{ max-width: 1800px; margin: 0 auto; background: white; }}
        header {{ background: linear-gradient(135deg, #232f3e 0%, #2c3e50 100%); color: white; padding: 24px 32px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ font-size: 2em; font-weight: 600; margin-bottom: 8px; }}
        .breadcrumb {{ color: #cbd5e0; font-size: 0.9em; margin-top: 8px; }}
        .breadcrumb a {{ color: #ff9900; text-decoration: none; transition: color 0.2s; }}
        .breadcrumb a:hover {{ color: #ffb84d; text-decoration: underline; }}
        .info-bar {{ padding: 20px 32px; background: #f7fafc; border-bottom: 1px solid #e2e8f0; display: flex; flex-wrap: wrap; gap: 24px; }}
        .info-item {{ display: flex; flex-direction: column; }}
        .info-label {{ font-size: 0.75em; color: #718096; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }}
        .info-value {{ font-size: 1.1em; font-weight: 600; color: #2d3748; }}
        .controls {{ padding: 20px 32px; background: white; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }}
        .control-group {{ display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }}
        .filter-input {{ flex: 1; min-width: 250px; padding: 10px 16px; border: 2px solid #e2e8f0; border-radius: 6px; font-size: 0.95em; transition: all 0.2s; }}
        .filter-input:focus {{ outline: none; border-color: #ff9900; box-shadow: 0 0 0 3px rgba(255, 153, 0, 0.1); }}
        .region-select {{ padding: 10px 16px; border: 2px solid #e2e8f0; border-radius: 6px; font-size: 0.95em; background: white; cursor: pointer; transition: all 0.2s; min-width: 200px; }}
        .region-select:focus {{ outline: none; border-color: #ff9900; box-shadow: 0 0 0 3px rgba(255, 153, 0, 0.1); }}
        .btn {{ padding: 10px 20px; border: none; border-radius: 6px; font-size: 0.9em; font-weight: 500; cursor: pointer; transition: all 0.2s; }}
        .btn-primary {{ background: #ff9900; color: white; }}
        .btn-primary:hover {{ background: #e88b00; transform: translateY(-1px); box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
        .btn-secondary {{ background: #e2e8f0; color: #4a5568; }}
        .btn-secondary:hover {{ background: #cbd5e0; }}
        .table-container {{ overflow-x: auto; padding: 0; }}
        table {{ width: 100%; border-collapse: collapse; font-size: 0.9em; }}
        thead {{ background: #2d3748; color: white; position: sticky; top: 0; z-index: 10; }}
        th {{ padding: 14px 12px; text-align: left; font-weight: 600; white-space: nowrap; cursor: pointer; user-select: none; transition: background 0.2s; }}
        th:hover {{ background: #1a202c; }}
        th.sortable::after {{ content: " ⇅"; opacity: 0.3; font-size: 0.8em; }}
        th.sort-asc::after {{ content: " ↑"; opacity: 1; color: #ff9900; }}
        th.sort-desc::after {{ content: " ↓"; opacity: 1; color: #ff9900; }}
        td {{ padding: 16px 12px; border-bottom: 1px solid #f0f0f0; vertical-align: top; }}
        tbody tr {{ transition: background 0.15s; }}
        tbody tr:hover {{ background: #f7fafc; }}
        .instance-name {{ font-family: 'SF Mono', 'Monaco', 'Courier New', monospace; font-weight: 700; color: #2d3748; font-size: 1.05em; }}
        .api-name {{ font-family: 'SF Mono', 'Monaco', monospace; color: #718096; font-size: 0.85em; margin-top: 2px; }}
        .badge {{ display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 0.75em; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
        .badge-new {{ background: #c6f6d5; color: #22543d; }}
        .badge-region {{ background: #e6f7ff; color: #0066cc; font-size: 0.7em; padding: 2px 8px; }}
        .price-grid {{ display: flex; flex-direction: column; gap: 4px; }}
        .price-item {{ display: flex; justify-content: space-between; align-items: center; font-size: 0.9em; }}
        .price-label {{ color: #718096; font-size: 0.85em; }}
        .price-value {{ font-weight: 600; color: #2d3748; }}
        .spec-value {{ font-weight: 600; color: #2d3748; }}
        .spec-unit {{ color: #a0aec0; font-size: 0.85em; margin-left: 2px; }}
        .stats {{ padding: 24px 32px; background: #edf2f7; text-align: center; font-size: 0.9em; color: #4a5568; }}
        footer {{ background: #2d3748; color: #cbd5e0; text-align: center; padding: 20px; font-size: 0.85em; }}
        footer a {{ color: #ff9900; text-decoration: none; }}
        footer a:hover {{ text-decoration: underline; }}
        @media (max-width: 768px) {{ .info-bar {{ padding: 16px 20px; }} .controls {{ padding: 16px 20px; }} .control-group {{ width: 100%; }} .filter-input, .region-select {{ width: 100%; }} th, td {{ padding: 10px 8px; font-size: 0.85em; }} }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{title}</h1>
            <div class="breadcrumb">
                <a href="../index.html">← Back to Overview</a> / {breadcrumb}
            </div>
        </header>
        <div class="info-bar">
            <div class="info-item"><span class="info-label">GPU/Accelerator</span><span class="info-value">{description}</span></div>
            <div class="info-item"><span class="info-label">Instance Count</span><span class="info-value" id="instanceCount">{instance_count} Variants</span></div>
            <div class="info-item"><span class="info-label">Release Year</span><span class="info-value">{year}</span></div>
            <div class="info-item"><span class="info-label">Use Case</span><span class="info-value">{use_case}</span></div>
            <div class="info-item"><span class="info-label">Current Region</span><span class="info-value" id="currentRegionLabel">US East (N. Virginia)</span></div>
        </div>
        <div class="controls">
            <div class="control-group">
                <input type="text" id="filterInput" class="filter-input" placeholder="🔍 Filter instances...">
                <select id="regionSelect" class="region-select" onchange="changeRegion(this.value)">
                    <optgroup label="Main Regions">
                        <option value="us-east-1">US East (N. Virginia)</option>
                        <option value="us-east-2">US East (Ohio)</option>
                        <option value="us-west-1">US West (N. California)</option>
                        <option value="us-west-2">US West (Oregon)</option>
                        <option value="eu-west-1">Europe (Ireland)</option>
                        <option value="eu-central-1">Europe (Frankfurt)</option>
                        <option value="ap-southeast-1">Asia Pacific (Singapore)</option>
                        <option value="ap-northeast-1">Asia Pacific (Tokyo)</option>
                    </optgroup>
                    <optgroup label="China Regions">
                        <option value="cn-north-1">China (Beijing)</option>
                        <option value="cn-northwest-1">China (Ningxia)</option>
                    </optgroup>
                </select>
            </div>
            <div class="control-group">
                <button class="btn btn-secondary" onclick="clearFilter()">Clear Filter</button>
                <button class="btn btn-primary" onclick="window.location.href='../index.html'">← Back</button>
            </div>
        </div>
        <div class="table-container">
            <table id="instanceTable">
                <thead><tr>
                    <th class="sortable" onclick="sortTable(0)">Instance Type</th>
                    <th class="sortable" onclick="sortTable(1)">GPU/Accelerator</th>
                    <th class="sortable" onclick="sortTable(2)">Count</th>
                    <th class="sortable" onclick="sortTable(3)">vCPUs</th>
                    <th class="sortable" onclick="sortTable(4)">System Memory</th>
                    <th class="sortable" onclick="sortTable(5)">Network</th>
                    <th class="sortable" onclick="sortTable(6)">Storage</th>
                    <th>Pricing (<span id="regionCode">us-east-1</span>)</th>
                    <th>Availability</th>
                </tr></thead>
                <tbody id="instanceTableBody"></tbody>
            </table>
        </div>
        <div class="stats">
            Showing <strong id="visibleCount">0</strong> of <strong id="totalCount">0</strong> instances |
            Pricing for <strong id="statsRegion">us-east-1</strong> region |
            Real pricing data from <strong>instances.vantage.sh</strong> (AWS Pricing API)
        </div>
        <footer>
            <p>AWS GPU Instance Comparison | <a href="../index.html">Back to Overview</a></p>
            <p style="margin-top: 8px; font-size: 0.9em; opacity: 0.8;">Data updated: {date}. Prices subject to change.</p>
        </footer>
    </div>
    <script src="../data/{family}_instances.js"></script>
    <script>
        let currentRegion = "us-east-1";
        const regionNames = {{"us-east-1": "US East (N. Virginia)", "us-east-2": "US East (Ohio)", "us-west-1": "US West (N. California)", "us-west-2": "US West (Oregon)", "eu-west-1": "Europe (Ireland)", "eu-central-1": "Europe (Frankfurt)", "ap-southeast-1": "Asia Pacific (Singapore)", "ap-northeast-1": "Asia Pacific (Tokyo)", "cn-north-1": "China (Beijing)", "cn-northwest-1": "China (Ningxia)"}};
        function renderTable() {{
            const tbody = document.getElementById('instanceTableBody');
            tbody.innerHTML = '';
            instanceData.forEach(instance => {{
                const pricing = instance.pricing[currentRegion];
                const isAvailable = instance.availability.includes(currentRegion);
                const row = document.createElement('tr');
                if (!isAvailable) row.style.opacity = '0.5';
                row.innerHTML = `<td><div class="instance-name">${{instance.name}}</div><div class="api-name">${{instance.apiName || instance.name}}</div>${{instance.isNew ? '<span class="badge badge-new">NEW</span>' : ''}}</td><td><div class="spec-value">${{instance.gpu}}</div></td><td><span class="spec-value">${{instance.gpuCount || 0}}</span><span class="spec-unit">×</span></td><td><span class="spec-value">${{instance.vcpu}}</span><span class="spec-unit">vCPUs</span></td><td><span class="spec-value">${{instance.memory.replace(' GB', '')}}</span><span class="spec-unit">GB</span></td><td><span class="spec-unit">${{instance.network}}</span></td><td><span class="spec-unit">${{instance.storage}}</span></td><td>${{isAvailable && pricing ? `<div class="price-grid"><div class="price-item"><span class="price-label">On-Demand:</span><span class="price-value">$${{pricing.onDemand.toFixed(2)}}/hr</span></div></div>` : '<span style="color: #999;">Not Available</span>'}}</td><td>${{isAvailable ? '<span class="badge badge-region">Available</span>' : '<span style="color: #999;">Not Available</span>'}}</td>`;
                tbody.appendChild(row);
            }});
            updateVisibleCount();
        }}
        function changeRegion(region) {{ currentRegion = region; document.getElementById('regionCode').textContent = region; document.getElementById('statsRegion').textContent = region; document.getElementById('currentRegionLabel').textContent = regionNames[region] || region; renderTable(); }}
        const filterInput = document.getElementById('filterInput');
        filterInput.addEventListener('input', function() {{ const filterValue = this.value.toLowerCase(); document.querySelectorAll('#instanceTableBody tr').forEach(row => {{ row.style.display = row.textContent.toLowerCase().includes(filterValue) ? '' : 'none'; }}); updateVisibleCount(); }});
        function clearFilter() {{ filterInput.value = ''; document.querySelectorAll('#instanceTableBody tr').forEach(row => row.style.display = ''); updateVisibleCount(); }}
        function updateVisibleCount() {{ const rows = document.querySelectorAll('#instanceTableBody tr'); document.getElementById('visibleCount').textContent = Array.from(rows).filter(row => row.style.display !== 'none').length; document.getElementById('totalCount').textContent = instanceData.length; }}
        let currentSort = {{ column: -1, ascending: true }};
        function sortTable(columnIndex) {{ const tbody = document.getElementById('instanceTableBody'); const rows = Array.from(tbody.querySelectorAll('tr')); const isAscending = currentSort.column === columnIndex ? !currentSort.ascending : true; document.querySelectorAll('th').forEach((h, i) => {{ h.classList.remove('sort-asc', 'sort-desc'); if (i === columnIndex) h.classList.add(isAscending ? 'sort-asc' : 'sort-desc'); }}); rows.sort((a, b) => {{ const aVal = a.cells[columnIndex].textContent.trim(), bVal = b.cells[columnIndex].textContent.trim(); const aNum = parseFloat(aVal.replace(/[^0-9.-]/g, '')), bNum = parseFloat(bVal.replace(/[^0-9.-]/g, '')); if (!isNaN(aNum) && !isNaN(bNum)) return isAscending ? aNum - bNum : bNum - aNum; return isAscending ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal); }}); rows.forEach(row => tbody.appendChild(row)); currentSort = {{ column: columnIndex, ascending: isAscending }}; }}
        renderTable();
    </script>
</body>
</html>'''


def get_breadcrumb(family: str, family_info: dict) -> str:
    """生成面包屑导航"""
    series = family_info.get('series', 'GPU')
    if series == 'P':
        return f"NVIDIA GPU / P Series / {family.upper()}"
    elif series == 'G':
        return f"NVIDIA GPU / G Series / {family.upper()}"
    elif series == 'Inf':
        return f"AWS Custom / Inferentia / {family.upper()}"
    elif series == 'Trn':
        return f"AWS Custom / Trainium / {family.upper()}"
    else:
        return f"GPU Instances / {family.upper()}"


def generate_page(family: str, family_info: dict, instance_count: int) -> str:
    """生成单个系列的 HTML 页面"""
    return HTML_TEMPLATE.format(
        title=family_info['title'],
        description=family_info['description'],
        instance_count=instance_count,
        year=family_info['year'],
        use_case=family_info['use_case'],
        family=family,
        breadcrumb=get_breadcrumb(family, family_info),
        date=get_current_date()
    )


def update_index_links():
    """更新 index.html 中的实例链接"""
    print("\n🔗 更新 index.html 链接...")

    if not INDEX_FILE.exists():
        print(f"   {colorize('⚠️', 'yellow')} index.html 不存在")
        return

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 获取已生成的页面列表
    generated_pages = [f.stem for f in INSTANCES_DIR.glob('*.html')]

    # 匹配没有链接的实例名称
    pattern = r'<td class="instance-name">\s*([A-Za-z][0-9a-z-]+)\s*</td>'

    def add_link(match):
        full_match = match.group(0)
        instance_name = match.group(1)
        family_lower = instance_name.lower()

        if '<a href=' in full_match:
            return full_match

        if family_lower in generated_pages:
            return f'<td class="instance-name"><a href="instances/{family_lower}.html">{instance_name}</a></td>'
        return full_match

    content = re.sub(pattern, add_link, content, flags=re.IGNORECASE)

    changes = content.count('<a href="instances/') - original_content.count('<a href="instances/')

    if changes > 0:
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   {colorize('✅', 'green')} 已添加 {changes} 个新链接")
    else:
        print(f"   ℹ️  没有需要更新的链接")


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='生成 GPU 实例详情页面')
    parser.add_argument('--family', '-f', type=str, help='只生成指定系列的页面')
    parser.add_argument('--no-links', action='store_true', help='不更新 index.html 链接')

    args = parser.parse_args()

    print("=" * 50)
    print("🚀 GPU 实例页面生成工具")
    print("=" * 50)

    INSTANCES_DIR.mkdir(exist_ok=True)

    generated = []
    skipped = []

    # 遍历数据文件
    data_files = sorted(DATA_DIR.glob('*_instances.js'))

    for data_file in data_files:
        family = data_file.stem.replace('_instances', '')

        # 跳过特殊文件
        if family in ['all_gpu'] or '_family_all' in family or '_cn' in family:
            continue

        # 如果指定了系列，只处理指定的
        if args.family and family != args.family:
            continue

        # 检查配置
        if family not in FAMILY_INFO:
            print(f"⚠️  {family}: 缺少配置信息，跳过")
            skipped.append(family)
            continue

        # 读取数据
        try:
            instances = read_js_data(data_file)
            instance_count = len(instances)
        except Exception as e:
            print(f"⚠️  {family}: 数据读取失败 ({e})，跳过")
            skipped.append(family)
            continue

        # 生成页面
        html = generate_page(family, FAMILY_INFO[family], instance_count)
        output_file = INSTANCES_DIR / f'{family}.html'

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ {family}: 已生成 ({instance_count} 个实例)")
        generated.append(family)

    # 更新链接
    if not args.no_links:
        update_index_links()

    # 总结
    print("\n" + "=" * 50)
    print("📊 生成总结")
    print("=" * 50)
    print(f"成功生成: {colorize(str(len(generated)), 'green')} 个页面")
    print(f"跳过: {len(skipped)} 个")

    if generated:
        print(f"\n{colorize('🎉 页面生成完成！', 'green')}")

    return 0 if generated else 1


if __name__ == '__main__':
    sys.exit(main())
