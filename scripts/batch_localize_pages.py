#!/usr/bin/env python3
"""批量中文化所有详情页面"""
from pathlib import Path
import re

def localize_page(file_path):
    """中文化单个页面"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. 面包屑导航
    content = re.sub(
        r'<a href="../index.html">← Back to Overview</a>',
        '<a href="../index.html">← 返回总览</a>',
        content
    )

    # 2. 系列名称
    content = content.replace('/ NVIDIA GPU / P Series /', '/ NVIDIA GPU / P 系列 /')
    content = content.replace('/ NVIDIA GPU / G Series /', '/ NVIDIA GPU / G 系列 /')
    content = content.replace('/ AWS Custom / Inferentia /', '/ AWS 定制 / Inferentia /')
    content = content.replace('/ AWS Custom / Trainium /', '/ AWS 定制 / Trainium /')

    # 3. 搜索框
    content = re.sub(
        r'placeholder="🔍 Filter instances\.\.\."',
        'placeholder="🔍 筛选实例..."',
        content
    )

    # 4. 区域下拉菜单
    content = re.sub(
        r'<optgroup label="Main Regions">',
        '<optgroup label="主要区域">',
        content
    )
    content = re.sub(
        r'<optgroup label="China Regions">',
        '<optgroup label="中国区域">',
        content
    )

    # 5. 区域名称
    region_map = {
        'US East \\(N\\. Virginia\\)': '美国东部（弗吉尼亚北部）',
        'US East \\(Ohio\\)': '美国东部（俄亥俄）',
        'US West \\(N\\. California\\)': '美国西部（加利福尼亚北部）',
        'US West \\(Oregon\\)': '美国西部（俄勒冈）',
        'Europe \\(Ireland\\)': '欧洲（爱尔兰）',
        'Europe \\(Frankfurt\\)': '欧洲（法兰克福）',
        'Asia Pacific \\(Singapore\\)': '亚太（新加坡）',
        'Asia Pacific \\(Tokyo\\)': '亚太（东京）',
        'China \\(Beijing\\)': '中国（北京）',
        'China \\(Ningxia\\)': '中国（宁夏）',
    }

    for eng, chn in region_map.items():
        content = re.sub(eng, chn, content)

    # 6. 按钮文字
    content = re.sub(
        r'onclick="clearFilter\(\)">Clear Filter<',
        'onclick="clearFilter()">清除筛选<',
        content
    )
    content = re.sub(
        r'onclick="window\.location\.href=\'\.\.\/index\.html\'">← Back<',
        'onclick="window.location.href=\'../index.html\'">← 返回<',
        content
    )

    # 7. 表头
    thead_map = {
        'Instance Type': '实例类型',
        'GPU/Accelerator': 'GPU 型号',
        'GPU Model': 'GPU 型号',
        'GPU Count': 'GPU 数量',
        'Count': '数量',
        'vCPUs': 'vCPU',
        'System Memory': '系统内存',
        'Network': '网络',
        'Storage': '存储',
        'Pricing': '价格',
        'Availability': '可用性',
    }

    for eng, chn in thead_map.items():
        # 只替换 <th> 标签内的
        content = re.sub(
            f'<th[^>]*>{eng}</th>',
            lambda m: m.group(0).replace(eng, chn),
            content
        )
        content = re.sub(
            f'<th[^>]*>{eng}<',
            lambda m: m.group(0).replace(eng, chn),
            content
        )

    # 8. 统计信息
    content = re.sub(
        r'Showing <strong',
        '显示 <strong',
        content
    )
    content = re.sub(
        r'</strong> of <strong',
        '</strong> / 共 <strong',
        content
    )
    content = re.sub(
        r'</strong> instances',
        '</strong> 个实例',
        content
    )
    content = re.sub(
        r'Pricing for <strong',
        '价格区域：<strong',
        content
    )
    content = re.sub(
        r'region \|',
        ' |',
        content
    )
    # 删除 "Real pricing data from..." 这行
    content = re.sub(
        r'\s*\|\s*Real pricing data from[^<]+',
        '',
        content
    )
    content = re.sub(
        r'\s*\|\s*真实价格数据来自[^<]+',
        '',
        content
    )

    # 9. 页脚
    content = re.sub(
        r'AWS GPU Instance Comparison',
        'AWS GPU 实例对比',
        content
    )
    content = re.sub(
        r'Back to Overview',
        '返回总览',
        content
    )
    content = re.sub(
        r'Data updated:',
        '数据更新：',
        content
    )
    content = re.sub(
        r'Prices subject to change\.',
        '价格可能变动。',
        content
    )

    # 10. JavaScript 中的区域名称映射
    js_region_section = re.search(r'const regionNames = \{[^}]+\};', content, re.DOTALL)
    if js_region_section:
        old_js = js_region_section.group(0)
        new_js = old_js
        for eng, chn in region_map.items():
            eng_clean = eng.replace('\\(', '(').replace('\\)', ')').replace('\\.', '.')
            new_js = new_js.replace(f'"{eng_clean}"', f'"{chn}"')
        content = content.replace(old_js, new_js)

    # 11. 价格标签（在 JavaScript 模板字符串中）
    content = re.sub(
        r'<span class="price-label">On-Demand:</span>',
        '<span class="price-label">按需：</span>',
        content
    )
    content = re.sub(
        r'<span class="price-label">Spot:</span>',
        '<span class="price-label">竞价：</span>',
        content
    )
    content = re.sub(
        r'<span class="price-label">1yr Reserved:</span>',
        '<span class="price-label">1年预留：</span>',
        content
    )

    # 12. 价格单位
    content = re.sub(
        r'\$\$\{pricing\.onDemand\.toFixed\(2\)\}/hr',
        '$$${pricing.onDemand.toFixed(2)}/小时',
        content
    )
    content = re.sub(
        r'\$\$\{pricing\.spot\.toFixed\(2\)\}/hr',
        '$$${pricing.spot.toFixed(2)}/小时',
        content
    )
    content = re.sub(
        r'\$\$\{pricing\.reserved\.toFixed\(2\)\}/hr',
        '$$${pricing.reserved.toFixed(2)}/小时',
        content
    )

    # 13. 可用性标签
    content = re.sub(
        r"'<span class=\"badge badge-region\">Available</span>'",
        "'<span class=\"badge badge-region\">可用</span>'",
        content
    )
    content = re.sub(
        r"'<span style=\"color: #999;\">Not Available</span>'",
        "'<span style=\"color: #999;\">不可用</span>'",
        content
    )
    content = re.sub(
        r'<span style="color: #999;">Not Available</span>',
        '<span style="color: #999;">不可用</span>',
        content
    )

    # 14. NEW 标签
    content = re.sub(
        r"'<span class=\"badge badge-new\">NEW</span>'",
        "'<span class=\"badge badge-new\">新品</span>'",
        content
    )
    content = re.sub(
        r'<span class="badge badge-new">NEW',
        '<span class="badge badge-new">新品',
        content
    )

    return content != original_content, content

def main():
    instances_dir = Path('/home/ubuntu/codes/aws-gpu/instances')

    print("🌏 批量中文化所有详情页面\n")

    # 获取所有 HTML 文件，排除 g6.html（已手动完成）
    html_files = [f for f in instances_dir.glob('*.html') if f.name != 'g6.html']

    print(f"找到 {len(html_files)} 个待处理页面（g6.html 已完成）\n")

    updated = 0
    skipped = 0

    for html_file in sorted(html_files):
        print(f"处理: {html_file.name}", end=' ... ')

        changed, new_content = localize_page(html_file)

        if changed:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("✅ 已更新")
            updated += 1
        else:
            print("⏭️  无需更新")
            skipped += 1

    print(f"\n📊 完成统计:")
    print(f"   总文件数: {len(html_files) + 1} (含 g6.html)")
    print(f"   本次更新: {updated}")
    print(f"   无需更新: {skipped}")
    print(f"   已完成: g6.html")

    print(f"\n✨ 所有页面已中文化完成！")

if __name__ == '__main__':
    main()
