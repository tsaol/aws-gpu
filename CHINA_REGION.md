# 中国区数据支持说明

## 📊 数据文件结构

项目现在支持独立的中国区数据文件：

### 文件命名规则
- **全球数据**: `data/{family}_instances.js` （例如：`g5_instances.js`）
- **中国区数据**: `data/{family}_instances_cn.js` （例如：`g5_instances_cn.js`）

### 可用的中国区数据文件
目前有 8 个 GPU 系列在中国区可用：

| 系列 | 全球文件 | 中国区文件 | 实例数 |
|------|---------|-----------|--------|
| G5 | `g5_instances.js` | `g5_instances_cn.js` | 8 |
| G4DN | `g4dn_instances.js` | `g4dn_instances_cn.js` | 6 |
| G3 | `g3_instances.js` | `g3_instances_cn.js` | 3 |
| G3S | `g3s_instances.js` | `g3s_instances_cn.js` | 1 |
| P4D | `p4d_instances.js` | `p4d_instances_cn.js` | 1 |
| P3 | `p3_instances.js` | `p3_instances_cn.js` | 3 |
| P2 | `p2_instances.js` | `p2_instances_cn.js` | 3 |
| INF1 | `inf1_instances.js` | `inf1_instances_cn.js` | 4 |

## 🌍 中国区域

中国区数据包含以下 AWS 中国区域的价格：

- `cn-north-1` - 中国（北京）
- `cn-north-1-pkx-1` - 中国（北京本地区）
- `cn-northwest-1` - 中国（宁夏）

## 💰 价格示例

以 G5.xlarge 为例：

**全球区域**:
- us-east-1: $1.006/小时
- ap-northeast-1: $1.459/小时
- eu-central-1: $1.258/小时

**中国区域**:
- cn-north-1: ¥9.51/小时
- cn-north-1-pkx-1: ¥9.51/小时
- cn-northwest-1: ¥6.70/小时 ⭐ (便宜约30%)

## 🔧 前端集成建议

### 方案 1: 动态加载（推荐）

根据用户选择的区域动态加载对应的数据文件：

```javascript
function loadInstanceData(family, isChinaRegion) {
  const suffix = isChinaRegion ? '_cn' : '';
  const scriptSrc = `data/${family}_instances${suffix}.js`;
  
  return fetch(scriptSrc)
    .then(response => response.text())
    .then(text => {
      // 解析 JS 文件并提取数据
      const data = extractInstanceData(text);
      return data;
    });
}

// 用户切换区域时调用
function onRegionChange(region) {
  const isChinaRegion = region.startsWith('cn-');
  loadInstanceData('g5', isChinaRegion)
    .then(data => renderTable(data));
}
```

### 方案 2: 预加载两套数据

在页面加载时同时加载全球和中国数据：

```html
<!-- 全球数据 -->
<script src="data/g5_instances.js"></script>

<!-- 中国区数据 -->
<script>
  let instanceDataCN;
  fetch('data/g5_instances_cn.js')
    .then(r => r.text())
    .then(text => {
      // 解析并存储中国区数据
      instanceDataCN = extractInstanceData(text);
    });
</script>
```

### 方案 3: 区域过滤

如果不想修改太多代码，可以保持现有结构，但在显示时过滤：

```javascript
function filterByRegion(instances, region) {
  return instances.filter(inst => {
    return inst.availability.includes(region);
  });
}
```

## 📝 数据更新流程

当需要更新数据时：

```bash
# 1. 下载最新数据
curl -o data/instances_full.json https://instances.vantage.sh/instances.json
curl -o data/instances_full_cn.json https://instances.vantage.sh/instances-cn.json

# 2. 提取 GPU 实例（全球）
python3 scripts/extract_gpu_instances.py

# 3. 提取 GPU 实例（中国）
python3 scripts/extract_gpu_instances_cn.py

# 4. 转换格式（全球）
python3 scripts/convert_to_awsgpu_format.py

# 5. 转换格式（中国）
python3 scripts/convert_to_awsgpu_format_cn.py
```

## 🎯 实施步骤

要在前端支持中国区切换，需要：

1. **修改详情页 HTML** (例如 `instances/g5.html`)：
   - 检测用户选择的区域
   - 动态加载对应的数据文件（`g5_instances.js` 或 `g5_instances_cn.js`）
   - 根据区域显示价格符号（`$` 或 `¥`）

2. **更新区域选择器**：
   - 当用户切换到中国区域时，加载 `*_cn.js` 文件
   - 当用户切换到其他区域时，加载标准 `*.js` 文件

3. **货币显示**：
   - 全球区域：显示 `$`
   - 中国区域：显示 `¥`

## ✅ 已完成

- ✅ 下载中国区原始数据
- ✅ 创建独立的数据提取脚本
- ✅ 创建独立的格式转换脚本
- ✅ 生成所有中国区数据文件
- ✅ 验证数据完整性和准确性
- ✅ 部署到生产服务器

## ⏳ 待完成

- ⏳ 前端页面支持动态加载中国区数据
- ⏳ 区域切换时自动切换数据源
- ⏳ 价格显示支持人民币符号（¥）

## 📚 参考资料

- instances.vantage.sh 数据源: https://instances.vantage.sh/
- 全球数据: https://instances.vantage.sh/instances.json
- 中国数据: https://instances.vantage.sh/instances-cn.json
