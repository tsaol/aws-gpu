#!/usr/bin/env python3
import json

print("正在读取中国区 GPU 实例数据...")
with open('/home/ubuntu/codes/aws-gpu/data/gpu_instances_raw_cn.json', 'r') as f:
    raw_instances = json.load(f)

def format_storage(inst):
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

def convert_pricing(pricing):
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

def get_gpu_info(inst):
    """获取 GPU 详细信息"""
    gpu_count = inst.get('GPU', 0)
    
    # 从实例类型推断 GPU 型号
    instance_type = inst.get('instance_type', '')
    
    gpu_models = {
        'p4d': 'NVIDIA A100',
        'p3': 'NVIDIA V100',
        'p2': 'NVIDIA K80',
        'g5': 'NVIDIA A10G',
        'g4dn': 'NVIDIA T4',
        'g3': 'NVIDIA M60',
        'g3s': 'NVIDIA M60',
        'g2': 'NVIDIA GRID K520',
    }
    
    gpu_model = 'Unknown GPU'
    for prefix, model in gpu_models.items():
        if instance_type.startswith(prefix):
            gpu_model = model
            break
    
    return {
        'model': gpu_model,
        'count': gpu_count
    }

# 转换实例数据
converted_instances = []

for inst in raw_instances:
    gpu_info = get_gpu_info(inst)
    pricing = convert_pricing(inst.get('pricing', {}))
    
    if not pricing:  # 跳过没有价格信息的实例
        continue
    
    converted = {
        'name': inst['instance_type'],
        'apiName': inst['instance_type'],
        'gpu': gpu_info['model'],
        'gpuCount': gpu_info['count'],
        'gpuMemory': f"{inst.get('gpu_memory_gb', 0)} GB per GPU" if inst.get('gpu_memory_gb') else "Unknown",
        'vcpu': inst.get('vCPU', 0),
        'memory': f"{inst.get('memory', 0)} GB",
        'network': inst.get('network_performance', 'Unknown'),
        'storage': format_storage(inst),
        'pricing': pricing,
        'availability': list(pricing.keys()),
        'generation': inst.get('generation', 'current'),
        'family': inst.get('family', 'Unknown'),
    }
    
    converted_instances.append(converted)

print(f"✅ 已转换 {len(converted_instances)} 个中国区实例")

# 按实例名称分组
families = {}
for inst in converted_instances:
    family = inst['name'].split('.')[0]
    if family not in families:
        families[family] = []
    families[family].append(inst)

# 为每个系列生成单独的文件 (带 _cn 后缀)
for family, instances in sorted(families.items()):
    output_file = f'/home/ubuntu/codes/aws-gpu/data/{family}_instances_cn.js'
    
    with open(output_file, 'w') as f:
        f.write('// Auto-generated from instances.vantage.sh China region data\n')
        f.write('// Last updated: 2025-11-30\n\n')
        f.write('var instanceData = ')
        f.write(json.dumps(instances, indent=2))
        f.write(';\n')
    
    print(f"  {family}: {len(instances)} 个实例 -> {family}_instances_cn.js")

print(f"\n✅ 所有中国区数据已生成到 data/ 目录")
print(f"   - 中国区文件: {len(families)} 个 (*_cn.js)")
