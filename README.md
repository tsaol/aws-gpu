# AWS GPU Instance Comparison

一个简洁的静态网页，以表格形式展示 AWS 所有 GPU 实例类型的技术规格和真实价格信息，方便快速查阅和对比。

## 特性

- ✅ **真实价格数据** - 集成 AWS Pricing API 的实际定价（来自 instances.vantage.sh）
- ✅ **详细实例页面** - 每个实例家族都有独立的详细页面，支持区域切换和价格对比
- ✅ **响应式设计** - 支持桌面和移动设备，自适应布局
- ✅ **按发布时间排序** - 新实例优先展示，标注最新发布
- ✅ **实时筛选** - 详情页支持实时搜索和排序功能
- ✅ **多区域支持** - 显示实例在不同 AWS 区域的可用性和价格

## 实例覆盖

### P 系列 - 通用 GPU 计算（训练和推理）
- P6 (GB200 Grace Blackwell) - 2025
- P5 (H100) - 2023
- P4d/P4de (A100) - 2020
- P3/P3dn (V100) - 2017
- P2 (K80) - 2016

### G 系列 - 图形密集型（渲染和推理）
- G6e, G6, G5, G5g, G4dn, G4ad

### Inf 系列 - 机器学习推理（AWS Inferentia）
- Inf2, Inf1

### Trn 系列 - 机器学习训练（AWS Trainium）
- Trn1, Trn1n

## 快速开始

### 本地运行

直接在浏览器中打开 `index.html` 或使用 Python 启动本地服务器：

```bash
python3 -m http.server 3000
```

然后访问 `http://localhost:3000`

### 部署为系统服务

使用提供的部署脚本一键部署为 systemd 服务：

```bash
# 使用默认配置（端口 3000，当前目录）
sudo ./deploy.sh

# 自定义端口和路径
sudo ./deploy.sh 8080 /path/to/project
```

服务特性：
- ✅ 系统重启后自动启动
- ✅ 进程崩溃后自动重启（10秒后）
- ✅ 日志由 systemd journal 自动管理
- ✅ 在后台持续运行

查看服务状态：
```bash
sudo systemctl status aws-gpu-server
sudo journalctl -u aws-gpu-server -f
```

详细部署说明请参见 [deployment.md](./deployment.md)

## 远程部署到 EC2

### 环境变量配置

1. 复制环境变量示例文件：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入你的 EC2 实例 ID：
```bash
AWS_GPU_INSTANCES="i-xxxxxxxxxxxxx,i-yyyyyyyyyyyyy"
```

3. 加载环境变量：
```bash
source .env
```

### 首次部署

```bash
./deploy_to_instances.sh
```

### 后续更新

```bash
./update_instances.sh
```

**前置条件：**
- 已安装并配置 AWS CLI
- 实例已安装 AWS Systems Manager (SSM) Agent
- 具有足够的 IAM 权限执行 SSM 命令

## 项目结构

```
aws-gpu/
├── index.html              # 主页面 - 实例总览列表
├── instances/              # 实例详情页面目录
│   ├── p6.html
│   ├── p5.html
│   ├── g6.html
│   └── ...
├── data/                   # 实例数据文件
│   ├── p6_family_all.js
│   ├── p5_family_all.js
│   └── ...
├── scripts/                # 数据处理脚本
│   ├── extract_gpu_instances.py
│   ├── convert_to_awsgpu_format.py
│   └── generate_instance_pages.py
├── deploy.sh               # 本地部署脚本
├── deploy_to_instances.sh  # EC2 远程部署脚本
├── update_instances.sh     # EC2 远程更新脚本
├── .env.example            # 环境变量示例
├── deployment.md           # 部署文档
├── casestudy.md           # 使用案例
└── README.md              # 本文档
```

## 技术栈

- **前端**: 纯静态 HTML + CSS + JavaScript
- **数据源**: AWS Pricing API（通过 instances.vantage.sh）
- **服务器**: Python 内置 HTTP 服务器
- **部署**: systemd 服务 + AWS SSM
- **版本控制**: Git + GitHub

## 数据更新

实例数据来自 `data/` 目录下的 JavaScript 文件。更新数据：

1. 下载最新的实例数据（从 instances.vantage.sh）
2. 使用 `scripts/extract_gpu_instances.py` 提取 GPU 实例
3. 使用 `scripts/convert_to_awsgpu_format.py` 转换格式
4. 使用 `scripts/generate_instance_pages.py` 生成页面

## 浏览器兼容性

支持所有现代浏览器：
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## 许可证

MIT License

## 作者

tsaol

## 项目仓库

https://github.com/tsaol/aws-gpu

## 相关文档

- [deployment.md](./deployment.md) - 详细部署和服务配置文档
- [casestudy.md](./casestudy.md) - AWS GPU 实例使用案例
- [gpu.md](./gpu.md) - GPU 实例详细信息库
