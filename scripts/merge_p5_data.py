#!/usr/bin/env python3
import json
import glob

# 读取所有 P5 相关的数据文件
p5_files = glob.glob('/home/ubuntu/codes/aws-gpu/data/p5*.js')
print(f"找到 {len(p5_files)} 个 P5 系列文件:")

all_p5_instances = []

for file in sorted(p5_files):
    print(f"  - {file}")
    with open(file, 'r') as f:
        content = f.read()
        # 提取 JSON 数据（去掉 const instanceData = 前缀）
        json_start = content.find('[')
        json_data = content[json_start:-2]  # 去掉最后的 ;\n
        instances = json.loads(json_data)
        all_p5_instances.extend(instances)

print(f"\n总共 {len(all_p5_instances)} 个 P5 系列实例")

# 补充一些额外信息
for inst in all_p5_instances:
    name = inst['name']
    
    # 补充 GPU Memory
    if 'p5en' in name or 'p5e' in name:
        inst['gpuMemory'] = "141 GB HBM3e per GPU"
    elif 'p5' in name:
        inst['gpuMemory'] = "80 GB HBM3 per GPU"
    
    # 补充网络信息
    if 'p5en' in name:
        inst['network'] = "3200 Gbps (EFAv3)"
    elif 'p5e' in name:
        inst['network'] = "1600 Gbps (EFA)"
    elif 'p5.48xlarge' in name:
        inst['network'] = "3200 Gbps (EFA v2)"
    
    # 补充存储信息更详细
    if '48xlarge' in name:
        inst['storage'] = "30.4 TB (8 × 3.8TB NVMe SSD)"
    
    # 标记为新实例
    inst['isNew'] = 'p5en' in name or 'p5e' in name
    inst['year'] = "2024" if inst['isNew'] else "2023"

# 按实例名称排序（p5en > p5e > p5）
all_p5_instances.sort(key=lambda x: (0 if 'p5en' in x['name'] else 1 if 'p5e' in x['name'] else 2, x['name']))

# 保存合并后的数据
output_file = '/home/ubuntu/codes/aws-gpu/data/p5_family_all.js'
with open(output_file, 'w') as f:
    f.write('// Auto-generated P5 Family data from instances.vantage.sh\n')
    f.write('// Last updated: 2025-11-30\n')
    f.write('// Includes: p5, p5e, p5en variants\n\n')
    f.write('var instanceData = ')
    f.write(json.dumps(all_p5_instances, indent=2))
    f.write(';\n')

print(f"\n✅ 已生成合并文件: {output_file}")
print("\nP5 系列实例:")
for inst in all_p5_instances:
    print(f"  - {inst['name']}: {inst['gpu']}, 可用区域数: {len(inst['availability'])}")
