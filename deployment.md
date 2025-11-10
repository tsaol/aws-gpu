# AWS GPU 实例列表

一个简洁的静态网页，以表格形式展示 AWS 所有 GPU 实例类型的技术规格和基本信息，方便快速查阅和对比。

## 项目说明

本项目提供了 AWS GPU 实例的完整信息，包括：
- P 系列 - 通用 GPU 计算实例
- G 系列 - 图形密集型实例
- Inf 系列 - 机器学习推理专用实例
- Trn 系列 - 机器学习训练专用实例

## 快速使用

### 方式一：直接打开
直接在浏览器中打开 `index.html` 文件即可查看。

### 方式二：本地服务器
使用 Python 启动本地服务器：
```bash
python3 -m http.server 3000
```

然后在浏览器访问 `http://localhost:3000`

## 部署为系统服务（推荐）

如果你希望服务在后台持续运行，并在系统重启后自动启动，可以设置为 systemd 服务。

### 快速部署（使用脚本）

项目提供了自动化部署脚本，一键完成所有配置：

```bash
# 使用默认配置（端口 3000，当前目录）
sudo ./deploy.sh

# 自定义端口和路径
sudo ./deploy.sh 8080 /path/to/project
```

脚本会自动：
- ✅ 检查系统环境
- ✅ 创建 systemd 服务文件
- ✅ 启用开机自动启动
- ✅ 启动服务
- ✅ 验证部署状态

---

### 手动部署（详细步骤）

如果你想了解部署细节或手动配置，可以按以下步骤操作。

#### 1. 创建服务文件

```bash
sudo tee /etc/systemd/system/aws-gpu-server.service > /dev/null << 'EOF'
[Unit]
Description=AWS GPU Static Server
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/Codes/aws-gpu
ExecStart=/usr/bin/python3 -m http.server 3000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
```

**注意**：请根据实际情况修改以下配置：
- `User=ubuntu` - 改为你的用户名
- `WorkingDirectory=/home/ubuntu/Codes/aws-gpu` - 改为你的项目路径
- `ExecStart` 中的端口号（默认 3000）

#### 2. 启用并启动服务

```bash
# 重新加载 systemd 配置
sudo systemctl daemon-reload

# 启用开机自动启动
sudo systemctl enable aws-gpu-server.service

# 启动服务
sudo systemctl start aws-gpu-server.service
```

#### 3. 服务管理命令

```bash
# 查看服务状态
sudo systemctl status aws-gpu-server

# 停止服务
sudo systemctl stop aws-gpu-server

# 重启服务
sudo systemctl restart aws-gpu-server

# 禁用开机自动启动
sudo systemctl disable aws-gpu-server
```

#### 4. 查看日志

日志由 systemd journal 自动管理，无需担心日志文件占满磁盘：

```bash
# 查看实时日志
sudo journalctl -u aws-gpu-server -f

# 查看最近 50 条日志
sudo journalctl -u aws-gpu-server -n 50

# 查看今天的日志
sudo journalctl -u aws-gpu-server --since today

# 查看最近 1 小时的日志
sudo journalctl -u aws-gpu-server --since "1 hour ago"
```

### 服务特性

- ✅ 系统重启后自动启动
- ✅ 进程崩溃后自动重启（10秒后）
- ✅ 日志由 systemd journal 自动管理（自动轮转，不占满磁盘）
- ✅ 在后台持续运行

## 项目文件

- `index.html` - 主页面，展示 GPU 实例列表
- `gpu.md` - GPU 实例详细信息库
- `requirements.md` - 项目需求文档
- `deployment.md` - 部署和服务配置文档
- `deploy.sh` - 自动化部署脚本

## 数据更新

实例数据来源于 `gpu.md` 文件，如需更新实例信息，请编辑该文件。

## 技术栈

- 纯静态 HTML + CSS
- 无需任何框架和构建工具
- Python 内置 HTTP 服务器

## 许可证

本项目基于 MIT 许可证开源。

## 作者

tsaol

## 项目仓库

https://github.com/tsaol/aws-gpu
