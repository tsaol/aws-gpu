# AWS GPU Instance Comparison

<div align="center">

一个简洁的静态网页，展示 AWS 所有 GPU 实例类型的技术规格和真实价格信息

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/tsaol/aws-gpu?style=social)](https://github.com/tsaol/aws-gpu/stargazers)

[在线演示](#) | [快速开始](#快速开始) | [部署指南](#部署)

</div>

---

## 特性

- **真实价格数据** - 集成 AWS Pricing API 的实际定价（来自 instances.vantage.sh）
- **详细实例页面** - 每个实例家族都有独立的详细页面，支持区域切换和价格对比
- **响应式设计** - 完美支持桌面和移动设备，自适应布局
- **最新实例** - 按发布时间排序，新实例优先展示并标注
- **实时筛选** - 详情页支持实时搜索和排序功能
- **多区域支持** - 显示实例在不同 AWS 区域的可用性和价格
- **无需构建** - 纯静态 HTML，开箱即用

## 目录

- [实例覆盖](#实例覆盖)
- [快速开始](#快速开始)
- [部署](#部署)
  - [本地部署](#本地运行)
  - [系统服务部署](#部署为系统服务)
  - [远程 EC2 部署](#远程部署到-ec2)
- [项目结构](#项目结构)
- [技术栈](#技术栈)
- [数据更新](#数据更新)
- [贡献](#贡献)
- [许可证](#许可证)

## 实例覆盖

### P 系列 - 通用 GPU 计算（训练和推理）

| 实例家族 | GPU 型号 | 发布年份 | 状态 |
|---------|---------|---------|------|
| **P6e** | NVIDIA GB200 Grace Blackwell | 2024 | 最新 |
| **P6** | NVIDIA B200/B300 Blackwell | 2024 | 最新 |
| **P5en** | NVIDIA H200 | 2024 | 推荐 |
| **P5** | NVIDIA H100 | 2023 | 稳定 |
| **P4d/P4de** | NVIDIA A100 | 2020 | 稳定 |
| **P3/P3dn** | NVIDIA V100 | 2017 | 成熟 |
| **P2** | NVIDIA K80 | 2016 | 旧代 |

### G 系列 - 图形与推理

| 实例家族 | GPU 型号 | 发布年份 | 状态 |
|---------|---------|---------|------|
| **G7e** | NVIDIA RTX PRO 6000 Blackwell | 2026 | 最新 |
| **G6e** | NVIDIA L40S | 2024 | 推荐 |
| **G6** | NVIDIA L4 | 2023 | 稳定 |
| **G5** | NVIDIA A10G | 2021 | 稳定 |
| **G5g** | ARM Mali-G78 | 2021 | 稳定 |
| **G4dn** | NVIDIA T4 | 2019 | 成熟 |
| **G4ad** | AMD Radeon Pro V520 | 2020 | 成熟 |

### 其他系列

- **Inf 系列** - 机器学习推理（Inf2, Inf1 - AWS Inferentia）
- **Trn 系列** - 机器学习训练（Trn2, Trn1, Trn1n - AWS Trainium）

## 快速开始

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

## 部署

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
- 开机自动启动
- 进程崩溃自动重启（10秒后）
- 日志自动管理和轮转
- 后台持续运行

### 远程部署到 EC2

#### 1. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入实例 ID
# AWS_GPU_INSTANCES="i-xxxxxxxxxxxxx,i-yyyyyyyyyyyyy"

# 加载环境变量
source .env
```

#### 2. 首次部署

```bash
./deploy_to_instances.sh
```

脚本会自动：
- 检查实例状态
- 安装 git 和 python3
- 克隆项目代码
- 配置并启动服务

#### 3. 后续更新

```bash
./update_instances.sh
```

**前置条件：**
- AWS CLI 已安装并配置
- 实例已安装 AWS Systems Manager (SSM) Agent
- 具有执行 SSM 命令的 IAM 权限

详细部署文档：[deployment.md](./deployment.md)

## 项目结构

```
aws-gpu/
├── README.md              # 项目文档
├── gpu.md                 # GPU 实例详细信息库
├── history.log            # 更新历史记录
├── index.html             # 主页面 - 实例总览
├── instances/             # 实例详情页面
│   ├── g7e.html
│   ├── p6e-gb200.html
│   ├── p5.html
│   └── ...
├── data/                  # 实例数据文件
│   ├── instances_full.json   # 原始数据（不提交）
│   ├── aws_official_specs.json # AWS 官方规格
│   ├── p6_family_all.js
│   ├── p5_family_all.js
│   └── ...
├── scripts/               # 数据处理脚本
│   ├── config.py             # 统一配置
│   ├── utils.py              # 公共工具函数
│   ├── update_all.py         # 一键更新入口
│   ├── download_data.py      # 下载数据
│   ├── convert_data.py       # 转换数据
│   ├── fetch_aws_official.py # AWS 官方数据
│   ├── generate_pages.py     # 生成 HTML
│   ├── generate_gpu_md.py    # 生成 gpu.md
│   └── legacy/               # 旧脚本备份
├── deploy.sh              # 本地部署脚本
├── deploy_to_instances.sh # EC2 远程部署
├── update_instances.sh    # EC2 远程更新
├── .env.example           # 环境变量示例
└── deployment.md          # 部署文档
```

## 技术栈

- **前端**: HTML5 + CSS3 + Vanilla JavaScript
- **数据源**: AWS Pricing API (via instances.vantage.sh)
- **服务器**: Python 内置 HTTP Server
- **部署**: systemd + AWS Systems Manager
- **版本控制**: Git + GitHub

## 数据更新

### 数据来源

项目采用**双数据源策略**，确保数据准确性和完整性：

| 数据源 | 用途 | URL |
|-------|------|-----|
| **instances.vantage.sh** (主) | 定价、可用区域、完整实例列表 | https://instances.vantage.sh/instances.json |
| **AWS 官方** (补充) | 准确的规格数据（GPU数量、显存等） | https://aws.amazon.com/ec2/instance-types/accelerated-computing/ |

**数据合并策略：**
- 规格数据（GPU数量、显存、vCPU等）→ AWS 官方优先
- 定价数据 → Vantage.sh
- 可用区域 → Vantage.sh
- 新实例（官方有、Vantage没有）→ 自动添加

### 本地数据处理流程

```bash
# 一键更新（推荐）
python3 scripts/update_all.py --all

# 或分步执行：

# 1. 下载最新数据
python3 scripts/download_data.py --all

# 2. 转换数据（自动合并 AWS 官方规格）
python3 scripts/convert_data.py

# 3. 生成 HTML 页面
python3 scripts/generate_pages.py

# 4. 更新 gpu.md 文档
python3 scripts/generate_gpu_md.py
```

### 脚本说明

| 脚本 | 功能 |
|------|------|
| `update_all.py` | 一键更新入口 |
| `download_data.py` | 下载 vantage.sh 数据 |
| `convert_data.py` | 数据转换 + AWS 官方数据合并 |
| `fetch_aws_official.py` | AWS 官方规格管理 |
| `generate_pages.py` | 生成 HTML 页面 |
| `generate_gpu_md.py` | 生成 gpu.md 文档 |
| `config.py` | 统一配置（GPU型号、显存映射等） |
| `utils.py` | 公共工具函数 |

### 数据同步机制

处理后的数据通过 **Git + GitHub** 同步到生产环境的 EC2 实例：

```
┌─────────────────────────────────────────────────────────────┐
│ 1. 数据源                                                    │
│    ├─ instances.vantage.sh (主) ─ 定价、可用区域             │
│    └─ aws.amazon.com (补充) ─ 官方规格数据                   │
└────────────────────────┬────────────────────────────────────┘
                         │ download_data.py + fetch_aws_official.py
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. 本地开发环境                                              │
│    ├─ convert_data.py ─ 数据转换 + 官方数据合并              │
│    ├─ generate_pages.py ─ 生成 HTML 页面                    │
│    └─ generate_gpu_md.py ─ 生成 gpu.md                      │
└────────────────────────┬────────────────────────────────────┘
                         │ git commit + git push
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. GitHub 仓库                                               │
│    ├─ data/*.js (处理后的数据文件)                           │
│    ├─ instances/*.html (详情页面)                           │
│    └─ index.html (主页)                                     │
└────────────────────────┬────────────────────────────────────┘
                         │ ./update_instances.sh (AWS SSM)
                         ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. 生产环境 EC2 实例                                         │
│    ├─ git pull 拉取最新代码                                  │
│    ├─ systemctl restart 重启服务                             │
│    └─ 用户访问更新后的数据                                    │
└─────────────────────────────────────────────────────────────┘
```

### 同步到 EC2 实例

完成数据处理和 Git 提交后，使用更新脚本同步到远程实例：

```bash
# 提交处理后的数据到 Git
git add data/*.js instances/*.html
git commit -m "update gpu data"
git push origin main

# 同步到所有 EC2 实例（自动执行 git pull 和服务重启）
./update_instances.sh
```

**update_instances.sh 自动完成**：
- 检查本地 Git 状态（确保已提交并推送）
- 通过 AWS SSM 在远程实例执行命令
- 远程实例执行 `git pull` 拉取最新代码
- 自动重启 `aws-gpu-server` 服务
- 用户立即看到更新后的数据

### 重要说明

**不同步到 GitHub 的文件**：
- `data/instances_full.json` (100MB 原始数据文件，已添加到 .gitignore)
- 该文件仅在本地用于数据处理，不提交到仓库

**同步到 GitHub 的文件**：
- `data/*.js` - 处理后的 JavaScript 数据文件（按 GPU 家族分类）
- `instances/*.html` - 自动生成的实例详情页面
- `index.html` - 主页面

## 浏览器兼容性

| 浏览器 | 最低版本 |
|-------|---------|
| Chrome/Edge | 90+ |
| Firefox | 88+ |
| Safari | 14+ |

## 贡献

欢迎贡献！请随时提交 Pull Request 或创建 Issue。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情

## 作者

**tsaol**

- GitHub: [@tsaol](https://github.com/tsaol)

## 相关链接

- [部署文档](./deployment.md) - 详细的部署和配置说明
- [使用案例](./casestudy.md) - AWS GPU 实例使用案例
- [数据源](./gpu.md) - GPU 实例详细信息库
- [AWS 官方文档](https://aws.amazon.com/ec2/instance-types/) - EC2 实例类型

---

<div align="center">

如果这个项目对你有帮助，请给它一个 Star！

Made with love by tsaol

</div>
