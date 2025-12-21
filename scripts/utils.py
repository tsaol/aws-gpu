#!/usr/bin/env python3
"""
AWS GPU 项目公共工具函数
"""
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

from config import GPU_MODELS, GPU_MEMORY, get_current_date


def format_storage(inst: Dict) -> str:
    """格式化存储信息"""
    storage = inst.get('storage', {})
    if not storage:
        return "EBS Only"

    devices = storage.get('devices', 0)
    if devices == 0:
        return "EBS Only"

    size_gb = storage.get('size', 0)
    ssd_type = storage.get('ssd_type', 'SSD')

    if devices > 1:
        return f"{size_gb} GB ({devices} × {size_gb // devices} GB {ssd_type})"
    else:
        return f"{size_gb} GB {ssd_type}"


def convert_pricing(pricing: Dict) -> Dict:
    """转换价格格式"""
    result = {}

    for region, os_pricing in pricing.items():
        linux_pricing = os_pricing.get('linux', {})
        if not linux_pricing:
            continue

        region_prices = {}

        # On-Demand 价格
        if 'ondemand' in linux_pricing:
            try:
                region_prices['onDemand'] = float(linux_pricing['ondemand'])
            except (ValueError, TypeError):
                pass

        # Spot 价格
        spot_data = linux_pricing.get('spot', {})
        if isinstance(spot_data, dict) and 'min' in spot_data:
            try:
                region_prices['spot'] = float(spot_data['min'])
            except (ValueError, TypeError):
                pass

        # Reserved 价格（1年标准预留，无预付）
        reserved_data = linux_pricing.get('reserved', {})
        if 'yrTerm1Standard.noUpfront' in reserved_data:
            try:
                region_prices['reserved'] = float(reserved_data['yrTerm1Standard.noUpfront'])
            except (ValueError, TypeError):
                pass

        if region_prices:
            result[region] = region_prices

    return result


def get_gpu_info(inst: Dict, is_china: bool = False) -> Dict:
    """获取 GPU 详细信息"""
    gpu_count = inst.get('GPU', 0)
    instance_type = inst.get('instance_type', '')

    # 查找 GPU 型号
    gpu_model = 'Unknown GPU'
    for prefix, model in GPU_MODELS.items():
        if instance_type.startswith(prefix):
            gpu_model = model
            break

    # 获取 GPU 显存
    family = instance_type.split('.')[0]
    gpu_memory = GPU_MEMORY.get(family, 'Unknown')

    return {
        'model': gpu_model,
        'count': gpu_count,
        'memory': gpu_memory
    }


def read_js_data(file_path: Path) -> List[Dict]:
    """读取 JS 数据文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 JSON 数据
    json_start = content.find('[')
    if json_start == -1:
        raise ValueError(f"无法在 {file_path} 中找到 JSON 数组")

    # 找到数组结尾
    json_end = content.rfind(']')
    if json_end == -1:
        raise ValueError(f"无法在 {file_path} 中找到 JSON 数组结尾")

    json_data = content[json_start:json_end + 1]
    return json.loads(json_data)


def write_js_data(
    file_path: Path,
    data: List[Dict],
    var_name: str = 'instanceData',
    comment: str = 'Auto-generated from instances.vantage.sh data',
    use_const: bool = False
) -> None:
    """写入 JS 数据文件"""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    keyword = 'const' if use_const else 'var'
    date = get_current_date()

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f'// {comment}\n')
        f.write(f'// Last updated: {date}\n\n')
        f.write(f'{keyword} {var_name} = ')
        f.write(json.dumps(data, indent=2, ensure_ascii=False))
        f.write(';\n')


def convert_instance(inst: Dict, is_china: bool = False, include_preview: bool = True) -> Optional[Dict]:
    """转换单个实例数据"""
    gpu_info = get_gpu_info(inst, is_china)
    pricing = convert_pricing(inst.get('pricing', {}))

    # 对于没有价格信息的实例
    if not pricing:
        if not include_preview:
            return None
        availability = []
        generation = 'preview'
    else:
        availability = list(pricing.keys())
        generation = inst.get('generation', 'current')

    return {
        'name': inst['instance_type'],
        'apiName': inst['instance_type'],
        'gpu': gpu_info['model'],
        'gpuCount': gpu_info['count'],
        'gpuMemory': gpu_info['memory'],
        'vcpu': inst.get('vCPU', 0),
        'memory': f"{inst.get('memory', 0)} GB",
        'network': inst.get('network_performance', 'Unknown'),
        'storage': format_storage(inst),
        'pricing': pricing,
        'availability': availability,
        'generation': generation,
        'family': inst.get('family', 'Unknown'),
    }


def group_by_family(instances: List[Dict]) -> Dict[str, List[Dict]]:
    """按系列分组实例"""
    families = {}
    for inst in instances:
        family = inst['name'].split('.')[0]
        if family not in families:
            families[family] = []
        families[family].append(inst)
    return families


def print_progress(current: int, total: int, prefix: str = '', suffix: str = '', length: int = 40):
    """打印进度条"""
    percent = current / total if total > 0 else 0
    filled = int(length * percent)
    bar = '█' * filled + '░' * (length - filled)
    print(f'\r{prefix} |{bar}| {percent:.1%} {suffix}', end='', flush=True)
    if current >= total:
        print()


def colorize(text: str, color: str) -> str:
    """给文本添加颜色（终端）"""
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'reset': '\033[0m',
    }
    return f"{colors.get(color, '')}{text}{colors['reset']}"


if __name__ == '__main__':
    # 测试
    print("测试 utils.py 函数")

    # 测试 GPU 信息
    test_inst = {'instance_type': 'p5.48xlarge', 'GPU': 8}
    info = get_gpu_info(test_inst)
    print(f"p5.48xlarge GPU 信息: {info}")

    # 测试存储格式化
    test_storage = {'storage': {'devices': 8, 'size': 3800, 'ssd_type': 'NVMe SSD'}}
    print(f"存储格式化: {format_storage(test_storage)}")
