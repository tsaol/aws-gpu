#!/usr/bin/env python3
import json

print("正在读取全球实例数据...")
with open('/home/ubuntu/codes/aws-gpu/data/instances_full.json', 'r') as f:
    all_instances = json.load(f)

print(f"全球总实例数: {len(all_instances)}")

# 提取 GPU 实例（GPU > 0 的实例）
gpu_instances = [inst for inst in all_instances if inst.get('GPU', 0) > 0]
print(f"全球 GPU 实例数: {len(gpu_instances)}")

# 按实例名称排序
gpu_instances.sort(key=lambda x: x['instance_type'])

# 保存 GPU 实例数据
with open('/home/ubuntu/codes/aws-gpu/data/gpu_instances_raw.json', 'w') as f:
    json.dump(gpu_instances, f, indent=2)

print(f"\n✅ 已提取 {len(gpu_instances)} 个全球 GPU 实例")

# 显示 GPU 实例类型
print("\n全球 GPU 实例类型统计:")
families = {}
for inst in gpu_instances:
    family = inst['instance_type'].split('.')[0]
    if family not in families:
        families[family] = 0
    families[family] += 1

for family, count in sorted(families.items()):
    print(f"  {family}: {count} 个实例")
