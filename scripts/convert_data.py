#!/usr/bin/env python3
"""
转换 AWS 实例数据
从原始 JSON 数据提取 GPU 实例并转换为项目格式

数据源:
  1. instances.vantage.sh - 主数据源（定价、可用区域）
  2. AWS 官方页面 - 补充数据源（规格数据更准确）
"""
import json
import sys
from pathlib import Path
from typing import List, Dict

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    DATA_DIR, RAW_DATA_FILES, GPU_RAW_FILES,
    GPU_MEMORY, get_current_date
)
from utils import (
    convert_instance, group_by_family, write_js_data,
    read_js_data, colorize
)
from fetch_aws_official import get_aws_official_specs, merge_with_vantage_data


def extract_gpu_instances(input_file: Path, output_file: Path, region_type: str = 'global') -> List[Dict]:
    """从原始数据中提取 GPU 实例"""
    print(f"\n📤 提取 GPU 实例 ({region_type})...")
    print(f"   输入: {input_file}")

    if not input_file.exists():
        print(f"   {colorize('❌', 'red')} 文件不存在: {input_file}")
        return []

    with open(input_file, 'r', encoding='utf-8') as f:
        all_instances = json.load(f)

    print(f"   总实例数: {len(all_instances)}")

    # 提取 GPU 实例（GPU > 0）
    gpu_instances = [inst for inst in all_instances if inst.get('GPU', 0) > 0]
    gpu_instances.sort(key=lambda x: x['instance_type'])

    print(f"   GPU 实例数: {colorize(str(len(gpu_instances)), 'green')}")

    # 保存原始 GPU 实例数据
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(gpu_instances, f, indent=2)

    print(f"   输出: {output_file}")

    return gpu_instances


def convert_instances(
    raw_instances: List[Dict],
    region_type: str = 'global',
    include_preview: bool = True
) -> List[Dict]:
    """转换实例格式"""
    print(f"\n🔄 转换实例数据 ({region_type})...")

    is_china = region_type == 'china'
    converted = []

    for inst in raw_instances:
        result = convert_instance(inst, is_china=is_china, include_preview=include_preview)
        if result:
            converted.append(result)

    print(f"   转换完成: {colorize(str(len(converted)), 'green')} 个实例")
    return converted


def save_by_family(
    instances: List[Dict],
    suffix: str = '',
    comment: str = 'Auto-generated from instances.vantage.sh data'
) -> Dict[str, int]:
    """按系列保存实例数据"""
    print(f"\n💾 按系列保存数据...")

    families = group_by_family(instances)
    saved = {}

    for family, family_instances in sorted(families.items()):
        filename = f'{family}_instances{suffix}.js'
        output_file = DATA_DIR / filename
        write_js_data(output_file, family_instances, comment=comment)
        saved[family] = len(family_instances)
        print(f"   {family}: {len(family_instances)} 个实例 -> {filename}")

    return saved


def save_all_instances(instances: List[Dict], suffix: str = '') -> None:
    """保存所有实例合并文件"""
    filename = f'all_gpu_instances{suffix}.js'
    output_file = DATA_DIR / filename

    date = get_current_date()
    comment = f'Auto-generated from instances.vantage.sh data'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f'// {comment}\n')
        f.write(f'// Last updated: {date}\n')
        f.write(f'// Total GPU instances: {len(instances)}\n\n')
        f.write('const allGPUInstances = ')
        f.write(json.dumps(instances, indent=2, ensure_ascii=False))
        f.write(';\n')

    print(f"   合并文件: {filename} ({len(instances)} 个实例)")


def merge_family_data(family_prefix: str, extra_info: Dict = None) -> None:
    """合并特定系列的数据并补充信息"""
    print(f"\n🔗 合并 {family_prefix.upper()} 系列数据...")

    # 查找所有匹配的数据文件
    pattern = f'{family_prefix}*_instances.js'
    files = sorted(DATA_DIR.glob(pattern))

    # 排除已合并的文件
    files = [f for f in files if '_family_all' not in f.name and '_cn' not in f.name]

    if not files:
        print(f"   未找到 {family_prefix} 系列数据文件")
        return

    all_instances = []
    for file in files:
        try:
            instances = read_js_data(file)
            all_instances.extend(instances)
            print(f"   读取: {file.name} ({len(instances)} 个实例)")
        except Exception as e:
            print(f"   {colorize('⚠️', 'yellow')} 读取失败 {file.name}: {e}")

    if not all_instances:
        return

    # 补充额外信息
    if extra_info:
        for inst in all_instances:
            family = inst['name'].split('.')[0]
            if family in extra_info:
                inst.update(extra_info[family])

    # 按实例名称排序
    all_instances.sort(key=lambda x: x['name'])

    # 保存合并文件
    output_file = DATA_DIR / f'{family_prefix}_family_all.js'
    comment = f'Auto-generated {family_prefix.upper()} Family data from instances.vantage.sh'

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f'// {comment}\n')
        f.write(f'// Last updated: {get_current_date()}\n')
        f.write(f'// Includes: {", ".join(sorted(set(i["name"].split(".")[0] for i in all_instances)))}\n\n')
        f.write('var instanceData = ')
        f.write(json.dumps(all_instances, indent=2, ensure_ascii=False))
        f.write(';\n')

    print(f"   {colorize('✅', 'green')} 已生成: {output_file.name} ({len(all_instances)} 个实例)")


def apply_aws_official_specs(instances: List[Dict], use_official: bool = True) -> List[Dict]:
    """
    应用 AWS 官方规格数据

    策略:
    - 规格数据（GPU数量、显存、vCPU等）使用 AWS 官方
    - 定价数据保留 vantage.sh
    - 官方有但 vantage 没有的实例，添加到列表
    """
    if not use_official:
        return instances

    print(f"\n🔗 合并 AWS 官方规格数据...")

    official_specs = get_aws_official_specs()
    print(f"   AWS 官方数据: {len(official_specs)} 个实例")

    merged = merge_with_vantage_data(instances, official_specs)

    # 统计
    merged_count = sum(1 for inst in merged if inst.get('source') == 'merged')
    added_count = sum(1 for inst in merged if inst.get('source') == 'aws_official')

    print(f"   已合并: {colorize(str(merged_count), 'green')} 个实例")
    if added_count > 0:
        print(f"   新增: {colorize(str(added_count), 'cyan')} 个实例")

    return merged


def process_global_data(use_official: bool = True) -> bool:
    """处理全球数据"""
    print("\n" + "=" * 50)
    print("🌍 处理全球数据")
    print("=" * 50)

    input_file = RAW_DATA_FILES['global']
    if not input_file.exists():
        print(f"{colorize('❌', 'red')} 原始数据文件不存在: {input_file}")
        print("请先运行: python3 download_data.py")
        return False

    # 1. 提取 GPU 实例
    gpu_instances = extract_gpu_instances(input_file, GPU_RAW_FILES['global'], 'global')
    if not gpu_instances:
        return False

    # 2. 转换格式
    converted = convert_instances(gpu_instances, 'global', include_preview=True)

    # 3. 合并 AWS 官方规格数据
    converted = apply_aws_official_specs(converted, use_official)

    # 4. 按系列保存
    save_by_family(converted)

    # 5. 保存合并文件
    save_all_instances(converted)

    # 6. 合并 P5 系列
    p5_extra = {
        'p5en': {'isNew': True, 'year': '2024'},
        'p5e': {'isNew': True, 'year': '2024'},
        'p5': {'isNew': False, 'year': '2023'},
    }
    merge_family_data('p5', p5_extra)

    # 7. 合并 P6 系列
    p6_extra = {
        'p6-b200': {'isNew': True, 'year': '2025'},
        'p6-b300': {'isNew': True, 'year': '2025'},
        'p6e-gb200': {'isNew': True, 'year': '2025'},
    }
    merge_family_data('p6', p6_extra)

    return True


def process_china_data() -> bool:
    """处理中国区数据"""
    print("\n" + "=" * 50)
    print("🇨🇳 处理中国区数据")
    print("=" * 50)

    input_file = RAW_DATA_FILES['china']
    if not input_file.exists():
        print(f"{colorize('⚠️', 'yellow')} 中国区数据文件不存在: {input_file}")
        print("跳过中国区数据处理")
        return True

    # 1. 提取 GPU 实例
    gpu_instances = extract_gpu_instances(input_file, GPU_RAW_FILES['china'], 'china')
    if not gpu_instances:
        return True  # 不算失败

    # 2. 转换格式（中国区不包含预览实例）
    converted = convert_instances(gpu_instances, 'china', include_preview=False)

    # 3. 按系列保存（带 _cn 后缀）
    save_by_family(
        converted,
        suffix='_cn',
        comment='Auto-generated from instances.vantage.sh China region data'
    )

    return True


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='转换 AWS 实例数据')
    parser.add_argument('--global', '-g', dest='process_global', action='store_true',
                        help='处理全球数据')
    parser.add_argument('--china', '-c', dest='process_china', action='store_true',
                        help='处理中国区数据')
    parser.add_argument('--all', '-a', action='store_true',
                        help='处理所有数据')
    parser.add_argument('--no-official', action='store_true',
                        help='不使用 AWS 官方数据补充')
    parser.add_argument('--official-only', action='store_true',
                        help='仅更新 AWS 官方数据（不重新下载 vantage）')

    args = parser.parse_args()

    # 默认处理全部
    if not (args.process_global or args.process_china or args.all):
        args.all = True

    use_official = not args.no_official

    print("=" * 50)
    print("🔧 AWS 实例数据转换工具")
    print("=" * 50)
    print(f"数据目录: {DATA_DIR}")
    print(f"AWS 官方数据: {'启用' if use_official else '禁用'}")

    success = True

    if args.process_global or args.all:
        if not process_global_data(use_official=use_official):
            success = False

    if args.process_china or args.all:
        if not process_china_data():
            success = False

    # 总结
    print("\n" + "=" * 50)
    print("📊 转换总结")
    print("=" * 50)

    if success:
        print(f"\n{colorize('🎉 数据转换完成！', 'green')}")
        print("\n下一步:")
        print("  - 运行 generate_pages.py 生成 HTML 页面")
        print("  - 运行 generate_gpu_md.py 更新 gpu.md")
        return 0
    else:
        print(f"\n{colorize('❌ 数据转换失败', 'red')}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
