#!/usr/bin/env python3
import json
import glob

print("合并 P6 家族数据...")

# 读取所有 P6 相关的数据文件
p6_files = glob.glob('/home/ubuntu/codes/aws-gpu/data/p6*.js')
print(f"找到 {len(p6_files)} 个 P6 系列文件")

all_p6_instances = []

for file in sorted(p6_files):
    print(f"  读取: {file}")
    with open(file, 'r') as f:
        content = f.read()
        json_start = content.find('[')
        json_data = content[json_start:-2]
        instances = json.loads(json_data)
        all_p6_instances.extend(instances)

print(f"\n总共 {len(all_p6_instances)} 个 P6 系列实例")

# 标记为新实例
for inst in all_p6_instances:
    inst['isNew'] = True
    inst['year'] = "2024-2025"
    # 补充 GPU Memory
    inst['gpuMemory'] = "192 GB HBM3e per GPU"

# 保存合并后的数据
output_file = '/home/ubuntu/codes/aws-gpu/data/p6_family_all.js'
with open(output_file, 'w') as f:
    f.write('// Auto-generated P6 Family data from instances.vantage.sh\n')
    f.write('// Last updated: 2025-11-30\n')
    f.write('// Includes: p6-b200, p6-b300 variants\n\n')
    f.write('const instanceData = ')
    f.write(json.dumps(all_p6_instances, indent=2))
    f.write(';\n')

print(f"\n✅ 已生成: {output_file}")
print("\nP6 系列实例:")
for inst in all_p6_instances:
    print(f"  - {inst['name']}: {inst['gpu']}, 可用区域: {len(inst['availability'])}")
