#!/usr/bin/env python3
"""
生成 gpu.md 文档
从数据源自动生成 GPU 实例详细信息文档
"""
import sys
from pathlib import Path
from typing import Dict, List

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import (
    DATA_DIR, GPU_MD_FILE, FAMILY_INFO, GPU_MEMORY,
    get_current_date
)
from utils import read_js_data, colorize, group_by_family


# GPU.md 文档结构配置
SERIES_ORDER = ['P', 'G', 'Inf', 'Trn', 'DL']
SERIES_TITLES = {
    'P': 'P 系列（训练型）',
    'G': 'G 系列（推理/图形）',
    'Inf': 'Inferentia 系列（推理）',
    'Trn': 'Trainium 系列（训练）',
    'DL': 'DL 系列（深度学习）',
}

# 额外的手动信息（数据源不提供）
EXTRA_INFO = {
    'p6-b200': {
        'workload': '训练/推理',
        'scenarios': '下一代 AI 训练、超大模型推理、科学计算',
        'features': ['NVLink 5', '第五代 Tensor Core', '8 TB/s 显存带宽'],
    },
    'p6-b300': {
        'workload': '训练/推理',
        'scenarios': '顶级训练性能、需要更大系统内存的场景',
        'features': ['NVLink 5', '第五代 Tensor Core', '更大系统内存'],
    },
    'p5en': {
        'workload': '训练/推理',
        'scenarios': '大规模 LLM 训练、高性能推理、分布式训练',
        'features': ['EFAv3 网络', '3200 Gbps 带宽', 'NVLink 4'],
    },
    'p5e': {
        'workload': '训练/推理',
        'scenarios': '大模型训练、高性能推理',
        'features': ['EFA 网络', '1600 Gbps 带宽'],
    },
    'p5': {
        'workload': '训练/推理',
        'scenarios': '大规模 LLM 训练、生成式 AI、科学计算',
        'features': ['EFAv2 网络', '3200 Gbps 带宽', 'NVLink 4'],
    },
    'p4de': {
        'workload': '训练',
        'scenarios': '大模型训练、需要更大显存的场景',
        'features': ['80GB 显存', 'EFA 网络', 'NVLink'],
    },
    'p4d': {
        'workload': '训练',
        'scenarios': 'ML/DL 训练、自然语言处理、计算机视觉',
        'features': ['EFA 网络', '400 Gbps 带宽', 'NVLink'],
    },
    'g6e': {
        'workload': '推理',
        'scenarios': '大模型推理(13B参数)、AI视频生成、3D渲染',
        'features': ['L40S GPU', '48GB 显存', '第四代 Tensor Core'],
    },
    'g6': {
        'workload': '推理',
        'scenarios': '成本优化推理、视频转码、图形渲染',
        'features': ['L4 GPU', '24GB 显存', '性价比高'],
    },
    'g5': {
        'workload': '推理',
        'scenarios': 'ML 推理、图形渲染、游戏流',
        'features': ['A10G GPU', '24GB 显存', '高性价比'],
    },
}


def get_price_from_instances(instances: List[Dict], region: str = 'us-east-1') -> float:
    """从实例列表获取代表性价格"""
    for inst in instances:
        pricing = inst.get('pricing', {}).get(region, {})
        if 'onDemand' in pricing:
            return pricing['onDemand']
    return 0.0


def generate_instance_section(family: str, instances: List[Dict]) -> str:
    """生成单个实例系列的 Markdown 内容"""
    if not instances:
        return ""

    family_info = FAMILY_INFO.get(family, {})
    extra = EXTRA_INFO.get(family, {})

    # 取第一个实例作为代表
    first_inst = instances[0]

    lines = []
    lines.append(f"#### {first_inst['name']}")
    lines.append(f"- **EC2 实例名称**: {first_inst['name']}")
    lines.append(f"- **GPU 型号**: {first_inst['gpu']}")
    lines.append(f"- **GPU 数量**: {first_inst.get('gpuCount', 'Unknown')}")

    # GPU 显存
    gpu_memory = GPU_MEMORY.get(family, first_inst.get('gpuMemory', 'Unknown'))
    lines.append(f"- **每GPU显存**: {gpu_memory}")

    lines.append(f"- **vCPU**: {first_inst.get('vcpu', 'Unknown')}")
    lines.append(f"- **系统内存**: {first_inst.get('memory', 'Unknown')}")
    lines.append(f"- **网络带宽**: {first_inst.get('network', 'Unknown')}")
    lines.append(f"- **存储**: {first_inst.get('storage', 'Unknown')}")

    # 发布时间
    year = family_info.get('year', 'Unknown')
    lines.append(f"- **发布时间**: {year}年")

    # Workload 类型
    if extra.get('workload'):
        lines.append(f"- **Workload类型**: {extra['workload']}")

    # 适用场景
    if extra.get('scenarios'):
        lines.append(f"- **适用场景**: {extra['scenarios']}")

    # 特性
    if extra.get('features'):
        features = '、'.join(extra['features'])
        lines.append(f"- **特性**: {features}")

    # 价格
    price = get_price_from_instances(instances)
    if price > 0:
        lines.append(f"- **价格参考**: ~${price:.2f}/小时")

    lines.append("")
    return '\n'.join(lines)


def generate_series_section(series: str, families: Dict[str, List[Dict]]) -> str:
    """生成系列章节"""
    series_families = {
        f: insts for f, insts in families.items()
        if FAMILY_INFO.get(f, {}).get('series') == series
    }

    if not series_families:
        return ""

    lines = []
    lines.append(f"### {SERIES_TITLES.get(series, series + ' 系列')}")
    lines.append("")

    # 按家族排序（新的在前）
    sorted_families = sorted(
        series_families.items(),
        key=lambda x: (FAMILY_INFO.get(x[0], {}).get('year', '2000'), x[0]),
        reverse=True
    )

    for family, instances in sorted_families:
        lines.append(generate_instance_section(family, instances))

    lines.append("---")
    lines.append("")
    return '\n'.join(lines)


def generate_gpu_md() -> str:
    """生成完整的 gpu.md 内容"""
    date = get_current_date()

    # 读取所有实例数据
    all_instances = []
    for data_file in DATA_DIR.glob('*_instances.js'):
        if '_cn' in data_file.name or '_family_all' in data_file.name or 'all_gpu' in data_file.name:
            continue
        try:
            instances = read_js_data(data_file)
            all_instances.extend(instances)
        except Exception:
            pass

    # 按系列分组
    families = group_by_family(all_instances)

    # 生成文档
    lines = []

    # 头部
    lines.append("# AWS GPU 实例详细信息")
    lines.append("")
    lines.append(f"> 最后更新: {date}")
    lines.append("> 数据来源: [instances.vantage.sh](https://instances.vantage.sh/)")
    lines.append("")

    # 目录
    lines.append("## 目录")
    lines.append("")
    for series in SERIES_ORDER:
        title = SERIES_TITLES.get(series, series)
        lines.append(f"- [{title}](#{series.lower()}-系列)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 各系列内容
    for series in SERIES_ORDER:
        content = generate_series_section(series, families)
        if content:
            lines.append(content)

    # 尾部
    lines.append("## 注意事项")
    lines.append("")
    lines.append("- 价格为 us-east-1 区域按需价格参考，实际以 AWS 官网为准")
    lines.append("- GPU 显存、网络带宽等规格可能因实例大小而异")
    lines.append("- 部分新实例可能处于预览状态，可用区域有限")
    lines.append("")

    return '\n'.join(lines)


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='生成 gpu.md 文档')
    parser.add_argument('--output', '-o', type=str, help='输出文件路径')
    parser.add_argument('--preview', '-p', action='store_true', help='预览输出（不写入文件）')

    args = parser.parse_args()

    print("=" * 50)
    print("📝 GPU.md 文档生成工具")
    print("=" * 50)

    # 生成内容
    content = generate_gpu_md()

    if args.preview:
        print("\n" + "=" * 50)
        print("预览:")
        print("=" * 50)
        print(content[:2000] + "..." if len(content) > 2000 else content)
        return 0

    # 确定输出路径
    output_path = Path(args.output) if args.output else GPU_MD_FILE

    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"\n{colorize('✅', 'green')} 已生成: {output_path}")
    print(f"   文件大小: {len(content)} 字符")

    return 0


if __name__ == '__main__':
    sys.exit(main())
