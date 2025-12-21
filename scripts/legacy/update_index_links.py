#!/usr/bin/env python3
"""更新 index.html 中的实例家族链接"""
from pathlib import Path
import re

# 已生成页面的实例家族
GENERATED_PAGES = [
    'p5', 'p4de', 'p4d', 'p3dn', 'p3', 'p2',
    'g6e', 'g6', 'g5', 'g5g', 'g4dn', 'g4ad',
    'inf2', 'inf1', 'trn1', 'trn1n'
]

def add_link(match):
    """为实例名称添加链接"""
    full_match = match.group(0)
    instance_name = match.group(1)
    
    # 转换为小写用于匹配文件名
    family_lower = instance_name.lower()
    
    # 检查是否有对应的页面
    if family_lower in GENERATED_PAGES:
        # 已经有链接了，不用修改
        if '<a href=' in full_match:
            return full_match
        # 添加链接
        return f'<td class="instance-name"><a href="instances/{family_lower}.html">{instance_name}</a></td>'
    else:
        # 没有对应页面，保持原样
        return full_match

def main():
    index_file = Path('/home/ubuntu/codes/aws-gpu/index.html')
    
    print("📝 更新 index.html 中的实例链接\n")
    
    # 读取文件
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # 匹配所有实例名称的 td 标签（不包含已有链接的）
    # 匹配模式：<td class="instance-name">P5</td> 或 <td class="instance-name"> P5 </td>
    pattern = r'<td class="instance-name">\s*([A-Z][0-9a-z]+)\s*</td>'
    
    # 替换所有匹配项
    content = re.sub(pattern, add_link, content)
    
    # 统计修改数量
    changes = content.count('<a href="instances/') - original_content.count('<a href="instances/')
    
    if changes > 0:
        # 保存文件
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 已添加 {changes} 个新链接")
        
        # 列出所有链接
        print(f"\n📎 当前所有实例链接:")
        for family in GENERATED_PAGES:
            if f'instances/{family}.html' in content:
                print(f"   - {family.upper()} → instances/{family}.html")
    else:
        print("ℹ️  没有需要更新的链接（所有链接已存在）")

if __name__ == '__main__':
    main()
