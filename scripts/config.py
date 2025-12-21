#!/usr/bin/env python3
"""
AWS GPU 项目统一配置文件
所有脚本共享的配置信息
"""
from pathlib import Path
from datetime import datetime

# ==================== 路径配置 ====================

# 项目根目录（自动检测）
PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# 数据目录
DATA_DIR = PROJECT_ROOT / 'data'

# 实例页面目录
INSTANCES_DIR = PROJECT_ROOT / 'instances'

# 主页文件
INDEX_FILE = PROJECT_ROOT / 'index.html'

# GPU.md 文件
GPU_MD_FILE = PROJECT_ROOT / 'gpu.md'

# ==================== 数据源配置 ====================

# instances.vantage.sh 数据源
DATA_SOURCES = {
    'global': 'https://instances.vantage.sh/instances.json',
    'china': 'https://instances.vantage.sh/instances-cn.json',
}

# 原始数据文件
RAW_DATA_FILES = {
    'global': DATA_DIR / 'instances_full.json',
    'china': DATA_DIR / 'instances_full_cn.json',
}

# GPU 实例原始数据
GPU_RAW_FILES = {
    'global': DATA_DIR / 'gpu_instances_raw.json',
    'china': DATA_DIR / 'gpu_instances_raw_cn.json',
}

# ==================== GPU 型号映射 ====================

# 完整的 GPU 型号映射（按前缀匹配顺序排列，更长的前缀优先）
GPU_MODELS = {
    # P6 系列 (Blackwell)
    'p6e-gb200': 'NVIDIA GB200 Grace Blackwell',
    'p6-b300': 'NVIDIA B300 Blackwell',
    'p6-b200': 'NVIDIA B200 Blackwell',
    # P5 系列 (H100/H200)
    'p5en': 'NVIDIA H200',
    'p5e': 'NVIDIA H200',
    'p5': 'NVIDIA H100',
    # P4 系列 (A100)
    'p4de': 'NVIDIA A100',
    'p4d': 'NVIDIA A100',
    # P3 系列 (V100)
    'p3dn': 'NVIDIA V100',
    'p3': 'NVIDIA V100',
    # P2 系列 (K80)
    'p2': 'NVIDIA K80',
    # G6 系列
    'g6e': 'NVIDIA L40S',
    'g6f': 'NVIDIA L40',
    'gr6f': 'NVIDIA L40',
    'gr6': 'NVIDIA L4',
    'g6': 'NVIDIA L4',
    # G5 系列
    'g5g': 'ARM Mali-G78MP12',
    'g5': 'NVIDIA A10G',
    # G4 系列
    'g4ad': 'AMD Radeon Pro V520',
    'g4dn': 'NVIDIA T4',
    # G3 系列
    'g3s': 'NVIDIA M60',
    'g3': 'NVIDIA M60',
    # G2 系列
    'g2': 'NVIDIA GRID K520',
    # Inferentia
    'inf2': 'AWS Inferentia2',
    'inf1': 'AWS Inferentia',
    # Trainium
    'trn2': 'AWS Trainium2',
    'trn1n': 'AWS Trainium',
    'trn1': 'AWS Trainium',
    # DL 系列
    'dl2q': 'Qualcomm AI 100',
    'dl1': 'Habana Gaudi',
}

# ==================== GPU 显存映射 ====================

# 手动维护的 GPU 显存信息（数据源不提供）
GPU_MEMORY = {
    # P6 系列
    'p6e-gb200': '192 GB HBM3e',
    'p6-b300': '192 GB HBM3e',
    'p6-b200': '192 GB HBM3e',
    # P5 系列
    'p5en': '141 GB HBM3e',
    'p5e': '141 GB HBM3e',
    'p5': '80 GB HBM3',
    # P4 系列
    'p4de': '80 GB HBM2e',
    'p4d': '40 GB HBM2',
    # P3 系列
    'p3dn': '32 GB HBM2',
    'p3': '16 GB HBM2',
    # P2 系列
    'p2': '12 GB GDDR5',
    # G6 系列
    'g6e': '48 GB GDDR6',
    'g6': '24 GB GDDR6',
    'g6f': '48 GB GDDR6',
    # G5 系列
    'g5': '24 GB GDDR6',
    'g5g': '4 GB',
    # G4 系列
    'g4dn': '16 GB GDDR6',
    'g4ad': '8 GB GDDR6',
    # G3 系列
    'g3': '8 GB GDDR5',
    # Inferentia
    'inf2': '32 GB HBM',
    'inf1': '8 GB',
    # Trainium
    'trn2': '96 GB HBM3',
    'trn1': '32 GB HBM',
}

# ==================== 实例系列信息 ====================

# 用于生成页面的系列配置
FAMILY_INFO = {
    'p6-b200': {
        'title': 'P6-B200 Instance Family',
        'description': 'NVIDIA B200 Blackwell',
        'use_case': 'Next-Gen AI Training & Inference',
        'year': '2025',
        'series': 'P',
    },
    'p6-b300': {
        'title': 'P6-B300 Instance Family',
        'description': 'NVIDIA B300 Blackwell',
        'use_case': 'Next-Gen AI Training & Inference',
        'year': '2025',
        'series': 'P',
    },
    'p6e-gb200': {
        'title': 'P6e-GB200 UltraServers',
        'description': 'NVIDIA GB200 Grace Blackwell Superchip',
        'use_case': 'Ultra-Scale AI Training',
        'year': '2025',
        'series': 'P',
    },
    'p5en': {
        'title': 'P5en Instance Family',
        'description': 'NVIDIA H200 Tensor Core',
        'use_case': 'Large-scale Training with Enhanced Memory',
        'year': '2024',
        'series': 'P',
    },
    'p5e': {
        'title': 'P5e Instance Family',
        'description': 'NVIDIA H200 Tensor Core',
        'use_case': 'High Performance Training',
        'year': '2024',
        'series': 'P',
    },
    'p5': {
        'title': 'P5 Instance Family',
        'description': 'NVIDIA H100 Tensor Core',
        'use_case': 'Large-scale Training & Inference',
        'year': '2023',
        'series': 'P',
    },
    'p4d': {
        'title': 'P4d Instance Family',
        'description': 'NVIDIA A100 Tensor Core',
        'use_case': 'Large-scale ML Training',
        'year': '2020',
        'series': 'P',
    },
    'p4de': {
        'title': 'P4de Instance Family',
        'description': 'NVIDIA A100 Tensor Core (80GB)',
        'use_case': 'ML Training with Large Models',
        'year': '2021',
        'series': 'P',
    },
    'p3': {
        'title': 'P3 Instance Family',
        'description': 'NVIDIA V100 Tensor Core',
        'use_case': 'ML Training & HPC',
        'year': '2017',
        'series': 'P',
    },
    'p3dn': {
        'title': 'P3dn Instance Family',
        'description': 'NVIDIA V100 Tensor Core (Network Optimized)',
        'use_case': 'Distributed ML Training',
        'year': '2018',
        'series': 'P',
    },
    'p2': {
        'title': 'P2 Instance Family',
        'description': 'NVIDIA K80',
        'use_case': 'ML Training (Previous Generation)',
        'year': '2016',
        'series': 'P',
    },
    'g6e': {
        'title': 'G6e Instance Family',
        'description': 'NVIDIA L40S',
        'use_case': 'Graphics & AI Inference',
        'year': '2024',
        'series': 'G',
    },
    'g6': {
        'title': 'G6 Instance Family',
        'description': 'NVIDIA L4 Tensor Core',
        'use_case': 'Cost-effective AI Inference',
        'year': '2023',
        'series': 'G',
    },
    'g5': {
        'title': 'G5 Instance Family',
        'description': 'NVIDIA A10G Tensor Core',
        'use_case': 'Graphics Workloads & ML Inference',
        'year': '2021',
        'series': 'G',
    },
    'g5g': {
        'title': 'G5g Instance Family',
        'description': 'ARM Mali-G78MP12 GPU',
        'use_case': 'Android Game Streaming',
        'year': '2021',
        'series': 'G',
    },
    'g4dn': {
        'title': 'G4dn Instance Family',
        'description': 'NVIDIA T4 Tensor Core',
        'use_case': 'ML Inference & Graphics',
        'year': '2019',
        'series': 'G',
    },
    'g4ad': {
        'title': 'G4ad Instance Family',
        'description': 'AMD Radeon Pro V520',
        'use_case': 'Graphics & Remote Workstations',
        'year': '2020',
        'series': 'G',
    },
    'inf2': {
        'title': 'Inf2 Instance Family',
        'description': 'AWS Inferentia2',
        'use_case': 'High Performance ML Inference',
        'year': '2023',
        'series': 'Inf',
    },
    'inf1': {
        'title': 'Inf1 Instance Family',
        'description': 'AWS Inferentia',
        'use_case': 'Cost-effective ML Inference',
        'year': '2019',
        'series': 'Inf',
    },
    'trn1': {
        'title': 'Trn1 Instance Family',
        'description': 'AWS Trainium',
        'use_case': 'Deep Learning Training',
        'year': '2022',
        'series': 'Trn',
    },
    'trn1n': {
        'title': 'Trn1n Instance Family',
        'description': 'AWS Trainium (Network Optimized)',
        'use_case': 'Distributed DL Training',
        'year': '2023',
        'series': 'Trn',
    },
    'trn2': {
        'title': 'Trn2 Instance Family',
        'description': 'AWS Trainium2',
        'use_case': 'Next-Gen DL Training',
        'year': '2024',
        'series': 'Trn',
    },
}

# ==================== 工具函数 ====================

def get_current_date():
    """获取当前日期字符串"""
    return datetime.now().strftime('%Y-%m-%d')


def get_family_from_instance(instance_type: str) -> str:
    """从实例类型获取系列名称"""
    return instance_type.split('.')[0]


def get_gpu_model(instance_type: str) -> str:
    """根据实例类型获取 GPU 型号"""
    for prefix, model in GPU_MODELS.items():
        if instance_type.startswith(prefix):
            return model
    return 'Unknown GPU'


def get_gpu_memory(instance_type: str) -> str:
    """根据实例类型获取 GPU 显存"""
    family = get_family_from_instance(instance_type)
    return GPU_MEMORY.get(family, 'Unknown')


if __name__ == '__main__':
    print(f"项目根目录: {PROJECT_ROOT}")
    print(f"数据目录: {DATA_DIR}")
    print(f"GPU 型号数量: {len(GPU_MODELS)}")
    print(f"系列配置数量: {len(FAMILY_INFO)}")
