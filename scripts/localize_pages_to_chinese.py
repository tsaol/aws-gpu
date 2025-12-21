#!/usr/bin/env python3
"""批量将所有详情页面本地化为中文"""
from pathlib import Path
import re

# 英文到中文的映射
TRANSLATIONS = {
    # 表头
    'Instance Type': '实例类型',
    'GPU/Accelerator': 'GPU/加速器',
    'GPU Model': 'GPU 型号',
    'GPU Count': 'GPU 数量',
    'Count': '数量',
    'vCPUs': 'vCPU',
    'System Memory': '系统内存',
    'Network': '网络',
    'Storage': '存储',
    'Pricing': '价格',
    'Availability': '可用性',

    # 按钮和控件
    'Filter instances...': '筛选实例...',
    'Clear Filter': '清除筛选',
    'Back': '返回',
    'Back to Overview': '返回总览',

    # 统计信息
    'Showing': '显示',
    'of': '共',
    'instances': '个实例',
    'Pricing for': '价格区域：',
    'region': '区域',
    'Real pricing data from': '真实价格数据来自',
    'AWS Pricing API': 'AWS 定价 API',

    # 价格标签
    'On-Demand:': '按需：',
    'Spot:': '竞价：',
    '1yr Reserved:': '1年预留：',

    # 可用性标签
    'Available': '可用',
    'Not Available': '不可用',

    # 页脚
    'AWS GPU Instance Comparison': 'AWS GPU 实例对比',
    'Data updated:': '数据更新：',
    'Prices subject to change.': '价格可能变动。',

    # 标签
    'NEW': '新品',
    'GPUs': '个 GPU',
    'GB': 'GB',
    'Gigabit': 'Gbps',
    'Hrs': '小时',

    # 信息栏标签
    'GPU/Accelerator': 'GPU/加速器',
    'Instance Count': '实例数量',
    'Release Year': '发布年份',
    'Use Case': '使用场景',
    'Current Region': '当前区域',
    'Variants': '个变体',

    # 区域名称
    'Main Regions': '主要区域',
    'China Regions': '中国区域',
    'US East (N. Virginia)': '美国东部（弗吉尼亚北部）',
    'US East (Ohio)': '美国东部（俄亥俄）',
    'US West (N. California)': '美国西部（加利福尼亚北部）',
    'US West (Oregon)': '美国西部（俄勒冈）',
    'Europe (Ireland)': '欧洲（爱尔兰）',
    'Europe (Frankfurt)': '欧洲（法兰克福）',
    'Asia Pacific (Singapore)': '亚太（新加坡）',
    'Asia Pacific (Tokyo)': '亚太（东京）',
    'China (Beijing)': '中国（北京）',
    'China (Ningxia)': '中国（宁夏）',
}

def translate_content(content):
    """翻译页面内容"""
    # 按从长到短排序，避免部分替换问题
    sorted_translations = sorted(TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)

    for english, chinese in sorted_translations:
        # 使用正则确保完整单词匹配（避免部分替换）
        # 但保留 HTML 标签内的属性
        content = re.sub(
            r'(?<=>)' + re.escape(english) + r'(?=<)',  # 在标签之间
            chinese,
            content
        )
        # 还要替换纯文本中的
        content = content.replace(english, chinese)

    return content

def main():
    instances_dir = Path('/home/ubuntu/codes/aws-gpu/instances')

    print("🌏 批量本地化详情页面为中文\n")

    html_files = list(instances_dir.glob('*.html'))

    if not html_files:
        print("❌ 未找到 HTML 文件")
        return

    print(f"找到 {len(html_files)} 个页面文件\n")

    updated_count = 0

    for html_file in sorted(html_files):
        print(f"处理: {html_file.name}")

        # 读取文件
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 翻译内容
        content = translate_content(content)

        # 检查是否有更改
        if content != original_content:
            # 保存文件
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"  ✅ 已更新")
            updated_count += 1
        else:
            print(f"  ⏭️  无需更新")

    print(f"\n📊 完成统计:")
    print(f"   总文件数: {len(html_files)}")
    print(f"   已更新: {updated_count}")
    print(f"   未改变: {len(html_files) - updated_count}")

    if updated_count > 0:
        print(f"\n✨ 所有页面已本地化为中文！")

if __name__ == '__main__':
    main()
