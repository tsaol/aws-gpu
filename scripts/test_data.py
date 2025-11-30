#!/usr/bin/env python3
"""测试 P5 数据完整性和正确性"""
import json

print("📊 测试 P5 系列数据\n")

# 读取数据文件
with open('/home/ubuntu/codes/aws-gpu/data/p5_family_all.js', 'r') as f:
    content = f.read()
    json_start = content.find('[')
    json_data = content[json_start:-2]
    data = json.loads(json_data)

print(f"✅ 数据文件加载成功")
print(f"   实例数量: {len(data)}\n")

# 测试每个实例
for inst in data:
    print(f"📦 {inst['name']}")
    print(f"   GPU: {inst['gpu']} x{inst['gpuCount']}")
    print(f"   Memory: {inst['gpuMemory']}")
    print(f"   可用区域: {len(inst['availability'])} 个")
    
    # 检查关键字段
    required_fields = ['name', 'gpu', 'gpuCount', 'vcpu', 'memory', 'pricing', 'availability']
    missing = [f for f in required_fields if f not in inst]
    if missing:
        print(f"   ⚠️  缺少字段: {missing}")
    else:
        print(f"   ✅ 所有必需字段完整")
    
    # 检查价格数据
    pricing_regions = len(inst['pricing'])
    print(f"   有价格的区域: {pricing_regions} 个")
    
    # 显示几个示例价格
    sample_regions = list(inst['pricing'].keys())[:3]
    for region in sample_regions:
        price = inst['pricing'][region].get('onDemand', 'N/A')
        print(f"      {region}: ${price}/hr")
    
    # 验证可用性和价格一致性
    pricing_set = set(inst['pricing'].keys())
    availability_set = set(inst['availability'])
    if pricing_set == availability_set:
        print(f"   ✅ 价格区域与可用性一致")
    else:
        print(f"   ⚠️  不匹配:")
        print(f"      只有价格: {pricing_set - availability_set}")
        print(f"      只标记可用: {availability_set - pricing_set}")
    
    print()

print(f"\n🎉 测试完成！")
print(f"   总实例数: {len(data)}")
print(f"   总区域数: {len(set(r for inst in data for r in inst['availability']))}")
