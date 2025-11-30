# AWS GPU Instance Comparison

<div align="center">

一个简洁的静态网页，展示 AWS 所有 GPU 实例类型的技术规格和真实价格信息

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/tsaol/aws-gpu?style=social)](https://github.com/tsaol/aws-gpu/stargazers)

[在线演示](#) | [快速开始](#快速开始) | [部署指南](#部署)

</div>

---

## ✨ 特性

- 🎯 **真实价格数据** - 集成 AWS Pricing API 的实际定价（来自 instances.vantage.sh）
- 📊 **详细实例页面** - 每个实例家族都有独立的详细页面，支持区域切换和价格对比
- 📱 **响应式设计** - 完美支持桌面和移动设备，自适应布局
- 🆕 **最新实例** - 按发布时间排序，新实例优先展示并标注
- 🔍 **实时筛选** - 详情页支持实时搜索和排序功能
- 🌍 **多区域支持** - 显示实例在不同 AWS 区域的可用性和价格
- 🚀 **无需构建** - 纯静态 HTML，开箱即用

## 📋 目录

- [实例覆盖](#-实例覆盖)
- [快速开始](#-快速开始)
- [部署](#-部署)
  - [本地部署](#本地运行)
  - [系统服务部署](#部署为系统服务)
  - [远程 EC2 部署](#远程部署到-ec2)
- [项目结构](#-项目结构)
- [技术栈](#-技术栈)
- [数据更新](#-数据更新)
- [贡献](#-贡献)
- [许可证](#-许可证)

## 🖥️ 实例覆盖

### P 系列 - 通用 GPU 计算（训练和推理）

| 实例家族 | GPU 型号 | 发布年份 | 状态 |
|---------|---------|---------|------|
| **P6** | NVIDIA GB200 Grace Blackwell | 2025 | 🆕 最新 |
| **P5** | NVIDIA H100 | 2023 | 🔥 推荐 |
| **P4d/P4de** | NVIDIA A100 | 2020 | ✅ 稳定 |
| **P3/P3dn** | NVIDIA V100 | 2017 | ✅ 成熟 |
| **P2** | NVIDIA K80 | 2016 | ⚠️ 旧代 |

### 其他系列

- **G 系列** - 图形密集型（G6e, G6, G5, G5g, G4dn, G4ad）
- **Inf 系列** - 机器学习推理（Inf2, Inf1 - AWS Inferentia）
- **Trn 系列** - 机器学习训练（Trn1, Trn1n - AWS Trainium）

## 🚀 快速开始

### 本地运行

**方式 1：直接打开**
```bash
# 直接在浏览器中打开 index.html
open index.html
```

**方式 2：本地服务器**
```bash
# 使用 Python 内置服务器
python3 -m http.server 3000

# 访问 http://localhost:3000
```

## 📦 部署

### 部署为系统服务

使用一键部署脚本配置 systemd 服务：

```bash
# 使用默认配置（端口 3000）
sudo ./deploy.sh

# 自定义端口和路径
sudo ./deploy.sh 8080 /path/to/project
```

**服务管理命令：**
```bash
# 查看服务状态
sudo systemctl status aws-gpu-server

# 查看实时日志
sudo journalctl -u aws-gpu-server -f

# 重启服务
sudo systemctl restart aws-gpu-server
```

**服务特性：**
- ✅ 开机自动启动
- ✅ 进程崩溃自动重启（10秒后）
- ✅ 日志自动管理和轮转
- ✅ 后台持续运行

### 远程部署到 EC2

#### 1️⃣ 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入实例 ID
# AWS_GPU_INSTANCES="i-xxxxxxxxxxxxx,i-yyyyyyyyyyyyy"

# 加载环境变量
source .env
```

#### 2️⃣ 首次部署

```bash
./deploy_to_instances.sh
```

脚本会自动：
- ✅ 检查实例状态
- ✅ 安装 git 和 python3
- ✅ 克隆项目代码
- ✅ 配置并启动服务

#### 3️⃣ 后续更新

```bash
./update_instances.sh
```

**前置条件：**
- AWS CLI 已安装并配置
- 实例已安装 AWS Systems Manager (SSM) Agent
- 具有执行 SSM 命令的 IAM 权限

详细部署文档：[deployment.md](./deployment.md)

## 📁 项目结构

```
aws-gpu/
├── 📄 README.md              # 项目文档
├── 🌐 index.html             # 主页面 - 实例总览
├── 📂 instances/             # 实例详情页面
│   ├── p6.html
│   ├── p5.html
│   └── ...
├── 📂 data/                  # 实例数据文件
│   ├── p6_family_all.js
│   ├── p5_family_all.js
│   └── ...
├── 📂 scripts/               # 数据处理脚本
│   ├── extract_gpu_instances.py
│   ├── convert_to_awsgpu_format.py
│   └── generate_instance_pages.py
├── 🚀 deploy.sh              # 本地部署脚本
├── 🌍 deploy_to_instances.sh # EC2 远程部署
├── 🔄 update_instances.sh    # EC2 远程更新
├── ⚙️ .env.example           # 环境变量示例
└── 📚 deployment.md          # 部署文档
```

## 🛠️ 技术栈

- **前端**: HTML5 + CSS3 + Vanilla JavaScript
- **数据源**: AWS Pricing API (via instances.vantage.sh)
- **服务器**: Python 内置 HTTP Server
- **部署**: systemd + AWS Systems Manager
- **版本控制**: Git + GitHub

## 🔄 数据更新

实例数据存储在 `data/` 目录。更新流程：

```bash
# 1. 下载最新数据
curl -o data/instances_full.json https://instances.vantage.sh/instances.json

# 2. 提取 GPU 实例
python3 scripts/extract_gpu_instances.py

# 3. 转换为项目格式
python3 scripts/convert_to_awsgpu_format.py

# 4. 生成实例页面
python3 scripts/generate_instance_pages.py
```

## 🌐 浏览器兼容性

| 浏览器 | 最低版本 |
|-------|---------|
| Chrome/Edge | 90+ |
| Firefox | 88+ |
| Safari | 14+ |

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request 或创建 Issue。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情

## 👤 作者

**tsaol**

- GitHub: [@tsaol](https://github.com/tsaol)

## 🔗 相关链接

- [部署文档](./deployment.md) - 详细的部署和配置说明
- [使用案例](./casestudy.md) - AWS GPU 实例使用案例
- [数据源](./gpu.md) - GPU 实例详细信息库
- [AWS 官方文档](https://aws.amazon.com/ec2/instance-types/) - EC2 实例类型

---

<div align="center">

如果这个项目对你有帮助，请给它一个 ⭐️！

Made with ❤️ by tsaol

</div>
