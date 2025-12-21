#!/usr/bin/env python3
"""
从 AWS 官方页面获取加速计算实例规格数据
作为 vantage.sh 数据源的补充

数据源: https://aws.amazon.com/cn/ec2/instance-types/accelerated-computing/
"""
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional
from urllib.request import urlopen, Request
from urllib.error import URLError

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from config import DATA_DIR, AWS_OFFICIAL_URLS, AWS_OFFICIAL_FILE, get_current_date
from utils import colorize


# ==================== 手动维护的官方数据 ====================
# 由于 AWS 页面结构复杂，部分数据需要手动维护
# 这些数据来自 AWS 官方文档，确保准确性

AWS_OFFICIAL_SPECS = {
    # P6e 系列 - Grace Blackwell
    'p6e-gb200.36xlarge': {
        'name': 'p6e-gb200.36xlarge',
        'gpu': 'NVIDIA GB200 Grace Blackwell',
        'gpuCount': 4,
        'gpuMemory': '740 GB HBM3e',
        'vcpu': 144,
        'memory': '960 GiB',
        'network': '1600 Gbps EFAv4',
        'storage': '22.5 TB NVMe SSD',
        'ebsBandwidth': '60 Gbps',
        'gpuInterconnect': '1800 GB/s NVLink',
        'gpuDirectRDMA': True,
        'source': 'aws_official',
    },
    'u-p6e-gb200x36': {
        'name': 'u-p6e-gb200x36',
        'gpu': 'NVIDIA GB200 Grace Blackwell',
        'gpuCount': 36,
        'gpuMemory': '6660 GB HBM3e',
        'vcpu': 1296,
        'memory': '8640 GiB',
        'network': '14400 Gbps EFAv4',
        'storage': '202.5 TB NVMe SSD',
        'ebsBandwidth': '540 Gbps',
        'gpuInterconnect': '1800 GB/s NVLink',
        'gpuDirectRDMA': True,
        'source': 'aws_official',
    },
    'u-p6e-gb200x72': {
        'name': 'u-p6e-gb200x72',
        'gpu': 'NVIDIA GB200 Grace Blackwell',
        'gpuCount': 72,
        'gpuMemory': '13320 GB HBM3e',
        'vcpu': 2592,
        'memory': '17280 GiB',
        'network': '28800 Gbps EFAv4',
        'storage': '405 TB NVMe SSD',
        'ebsBandwidth': '1080 Gbps',
        'gpuInterconnect': '1800 GB/s NVLink',
        'gpuDirectRDMA': True,
        'source': 'aws_official',
    },

    # P6 B200 系列
    'p6-b200.48xlarge': {
        'name': 'p6-b200.48xlarge',
        'gpu': 'NVIDIA B200',
        'gpuCount': 8,
        'gpuMemory': '1432 GB HBM3e',
        'vcpu': 192,
        'memory': '2048 GiB',
        'network': '3200 Gbps EFAv4',
        'storage': '8 x 3.84 TB NVMe SSD',
        'ebsBandwidth': '100 Gbps',
        'gpuInterconnect': '1800 GB/s NVLink',
        'gpuDirectRDMA': True,
        'source': 'aws_official',
    },

    # P5 系列
    'p5.48xlarge': {
        'name': 'p5.48xlarge',
        'gpu': 'NVIDIA H100',
        'gpuCount': 8,
        'gpuMemory': '640 GB HBM3',
        'vcpu': 192,
        'memory': '2048 GiB',
        'network': '3200 Gbps EFAv2',
        'storage': '8 x 3.84 TB NVMe SSD',
        'ebsBandwidth': '80 Gbps',
        'gpuInterconnect': '900 GB/s NVSwitch',
        'gpuDirectRDMA': True,
        'source': 'aws_official',
    },
    'p5e.48xlarge': {
        'name': 'p5e.48xlarge',
        'gpu': 'NVIDIA H200',
        'gpuCount': 8,
        'gpuMemory': '1128 GB HBM3e',
        'vcpu': 192,
        'memory': '2048 GiB',
        'network': '3200 Gbps EFAv2',
        'storage': '8 x 3.84 TB NVMe SSD',
        'ebsBandwidth': '80 Gbps',
        'gpuInterconnect': '900 GB/s NVSwitch',
        'gpuDirectRDMA': True,
        'source': 'aws_official',
    },
    'p5en.48xlarge': {
        'name': 'p5en.48xlarge',
        'gpu': 'NVIDIA H200',
        'gpuCount': 8,
        'gpuMemory': '1128 GB HBM3e',
        'vcpu': 192,
        'memory': '2048 GiB',
        'network': '3200 Gbps EFAv3',
        'storage': '8 x 3.84 TB NVMe SSD',
        'ebsBandwidth': '100 Gbps',
        'gpuInterconnect': '900 GB/s NVSwitch',
        'gpuDirectRDMA': True,
        'source': 'aws_official',
    },

    # P4d 系列
    'p4d.24xlarge': {
        'name': 'p4d.24xlarge',
        'gpu': 'NVIDIA A100',
        'gpuCount': 8,
        'gpuMemory': '320 GB HBM2',
        'vcpu': 96,
        'memory': '1152 GiB',
        'network': '400 Gbps EFA',
        'storage': '8 x 1 TB NVMe SSD',
        'ebsBandwidth': '19 Gbps',
        'gpuInterconnect': '600 GB/s NVSwitch',
        'gpuDirectRDMA': True,
        'source': 'aws_official',
    },
    'p4de.24xlarge': {
        'name': 'p4de.24xlarge',
        'gpu': 'NVIDIA A100 80GB',
        'gpuCount': 8,
        'gpuMemory': '640 GB HBM2e',
        'vcpu': 96,
        'memory': '1152 GiB',
        'network': '400 Gbps EFA',
        'storage': '8 x 1 TB NVMe SSD',
        'ebsBandwidth': '19 Gbps',
        'gpuInterconnect': '600 GB/s NVSwitch',
        'gpuDirectRDMA': True,
        'source': 'aws_official',
    },
}


def get_aws_official_specs() -> Dict[str, dict]:
    """获取 AWS 官方规格数据"""
    return AWS_OFFICIAL_SPECS.copy()


def merge_with_vantage_data(vantage_instances: List[dict],
                            official_specs: Dict[str, dict]) -> List[dict]:
    """
    合并 vantage.sh 数据和 AWS 官方数据

    合并策略:
    - 规格数据优先使用 AWS 官方
    - 定价数据保留 vantage.sh
    - 可用区域数据保留 vantage.sh
    - 官方有但 vantage 没有的实例，添加到列表
    """
    # 创建实例名称到数据的映射
    vantage_map = {inst['name']: inst for inst in vantage_instances}
    merged = []

    # 处理 vantage 数据，用官方数据补充/覆盖规格
    for inst in vantage_instances:
        name = inst['name']
        if name in official_specs:
            # 合并数据：官方规格 + vantage 定价和可用区域
            official = official_specs[name]
            merged_inst = inst.copy()

            # 用官方数据覆盖规格字段
            for key in ['gpuCount', 'gpuMemory', 'vcpu', 'memory',
                       'network', 'storage', 'ebsBandwidth',
                       'gpuInterconnect', 'gpuDirectRDMA']:
                if key in official:
                    merged_inst[key] = official[key]

            # 标记数据来源
            merged_inst['source'] = 'merged'
            merged.append(merged_inst)
        else:
            merged.append(inst)

    # 添加官方有但 vantage 没有的实例
    for name, official in official_specs.items():
        if name not in vantage_map:
            new_inst = official.copy()
            new_inst['pricing'] = {}
            new_inst['availability'] = []
            new_inst['generation'] = 'current'
            new_inst['family'] = 'GPU instance'
            merged.append(new_inst)
            print(f"   {colorize('+', 'green')} 添加官方实例: {name}")

    return merged


def save_official_specs():
    """保存官方规格数据到文件"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    data = {
        'last_updated': get_current_date(),
        'source': 'AWS Official Documentation',
        'instances': AWS_OFFICIAL_SPECS
    }

    with open(AWS_OFFICIAL_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"{colorize('✅', 'green')} 已保存官方规格数据: {AWS_OFFICIAL_FILE}")
    return True


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(description='AWS 官方数据管理工具')
    parser.add_argument('--save', '-s', action='store_true',
                        help='保存官方规格数据到文件')
    parser.add_argument('--list', '-l', action='store_true',
                        help='列出所有官方规格数据')
    parser.add_argument('--instance', '-i', type=str,
                        help='查看指定实例的官方规格')

    args = parser.parse_args()

    print("=" * 50)
    print("🔧 AWS 官方数据管理工具")
    print("=" * 50)

    specs = get_aws_official_specs()

    if args.list:
        print(f"\n📋 官方规格数据 ({len(specs)} 个实例):")
        print("-" * 40)
        for name, data in sorted(specs.items()):
            gpu_count = data.get('gpuCount', '?')
            gpu = data.get('gpu', 'Unknown')
            print(f"  {name}: {gpu_count}x {gpu}")

    elif args.instance:
        if args.instance in specs:
            print(f"\n📋 {args.instance} 官方规格:")
            print("-" * 40)
            for key, value in specs[args.instance].items():
                print(f"  {key}: {value}")
        else:
            print(f"\n{colorize('❌', 'red')} 未找到实例: {args.instance}")
            print("可用实例:", ', '.join(sorted(specs.keys())))

    elif args.save:
        save_official_specs()

    else:
        parser.print_help()
        print(f"\n{colorize('提示:', 'yellow')} 使用 --list 查看所有官方数据")

    return 0


if __name__ == '__main__':
    sys.exit(main())
