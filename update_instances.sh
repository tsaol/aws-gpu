#!/bin/bash

# AWS GPU 实例更新脚本
# 用于更新部署在 EC2 实例上的 aws-gpu 项目

set -e

# 配置
INSTANCES=(
    "[已删除]"  # [已删除]
    "[已删除]"  # (gpu whole picture -2) [已删除]
)

PROJECT_DIR="/home/ubuntu/codes/aws-gpu"
SERVICE_NAME="aws-gpu-server"

echo "=========================================="
echo "AWS GPU 项目更新脚本"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 AWS CLI
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ 错误: 未找到 AWS CLI${NC}"
    exit 1
fi

# 检查是否已推送到 GitHub
echo "📝 检查 Git 状态..."
if ! git diff-index --quiet HEAD --; then
    echo -e "${RED}❌ 错误: 有未提交的更改${NC}"
    echo "请先提交所有更改："
    echo "  git add ."
    echo "  git commit -m '更新说明'"
    exit 1
fi

# 检查是否已推送
LOCAL_COMMIT=$(git rev-parse HEAD)
REMOTE_COMMIT=$(git rev-parse origin/main 2>/dev/null || echo "unknown")

if [ "$LOCAL_COMMIT" != "$REMOTE_COMMIT" ]; then
    echo -e "${YELLOW}⚠️  本地提交领先远程仓库${NC}"
    echo "是否推送到 GitHub? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        echo "📤 推送到 GitHub..."
        git push origin main
        echo -e "${GREEN}✅ 推送成功${NC}"
    else
        echo -e "${RED}❌ 取消更新${NC}"
        exit 1
    fi
fi

echo ""
echo "🚀 开始更新 ${#INSTANCES[@]} 个实例..."
echo ""

# 更新函数
update_instance() {
    local instance_id=$1
    local instance_name=$2

    echo "=========================================="
    echo "📦 更新实例: $instance_name"
    echo "   ID: $instance_id"
    echo "=========================================="

    # 检查实例状态
    echo "1️⃣  检查实例状态..."
    local state=$(aws ec2 describe-instances \
        --instance-ids "$instance_id" \
        --query 'Reservations[0].Instances[0].State.Name' \
        --output text)

    if [ "$state" != "running" ]; then
        echo -e "${RED}❌ 实例状态: $state (未运行)${NC}"
        return 1
    fi

    echo -e "${GREEN}✅ 实例状态: $state${NC}"

    # 创建更新命令脚本
    local update_script="
        set -e
        cd $PROJECT_DIR || exit 1

        echo '2️⃣  拉取最新代码...'
        git fetch origin
        git reset --hard origin/main

        echo '3️⃣  检查服务状态...'
        if sudo systemctl is-active --quiet $SERVICE_NAME; then
            echo '   服务正在运行，重启服务...'
            sudo systemctl restart $SERVICE_NAME
            sleep 2
            if sudo systemctl is-active --quiet $SERVICE_NAME; then
                echo '   ✅ 服务重启成功'
            else
                echo '   ❌ 服务重启失败'
                sudo systemctl status $SERVICE_NAME
                exit 1
            fi
        else
            echo '   ⚠️  服务未运行，启动服务...'
            if [ -f deploy.sh ]; then
                sudo ./deploy.sh 3000 $PROJECT_DIR
            else
                sudo systemctl start $SERVICE_NAME
            fi
        fi

        echo '4️⃣  验证服务...'
        sudo systemctl status $SERVICE_NAME --no-pager -l

        echo ''
        echo '✅ 更新完成'
    "

    # 使用 SSM 执行命令
    echo "2️⃣  执行更新..."
    local command_id=$(aws ssm send-command \
        --instance-ids "$instance_id" \
        --document-name "AWS-RunShellScript" \
        --parameters "commands=[\"$update_script\"]" \
        --query 'Command.CommandId' \
        --output text)

    if [ -z "$command_id" ]; then
        echo -e "${RED}❌ 发送命令失败${NC}"
        return 1
    fi

    echo "   命令 ID: $command_id"
    echo "   等待执行完成..."

    # 等待命令完成
    for i in {1..60}; do
        local status=$(aws ssm get-command-invocation \
            --command-id "$command_id" \
            --instance-id "$instance_id" \
            --query 'Status' \
            --output text 2>/dev/null || echo "Pending")

        if [ "$status" = "Success" ]; then
            echo -e "${GREEN}✅ 命令执行成功${NC}"

            # 显示输出
            echo ""
            echo "📋 执行输出:"
            echo "----------------------------------------"
            aws ssm get-command-invocation \
                --command-id "$command_id" \
                --instance-id "$instance_id" \
                --query 'StandardOutputContent' \
                --output text
            echo "----------------------------------------"
            return 0
        elif [ "$status" = "Failed" ]; then
            echo -e "${RED}❌ 命令执行失败${NC}"
            echo ""
            echo "📋 错误输出:"
            echo "----------------------------------------"
            aws ssm get-command-invocation \
                --command-id "$command_id" \
                --instance-id "$instance_id" \
                --query 'StandardErrorContent' \
                --output text
            echo "----------------------------------------"
            return 1
        fi

        printf "."
        sleep 2
    done

    echo ""
    echo -e "${RED}❌ 超时: 命令未在 120 秒内完成${NC}"
    return 1
}

# 更新所有实例
success_count=0
failed_count=0

for instance_id in "${INSTANCES[@]}"; do
    # 获取实例名称
    instance_name=$(aws ec2 describe-instances \
        --instance-ids "$instance_id" \
        --query 'Reservations[0].Instances[0].Tags[?Key==`Name`].Value' \
        --output text)

    if update_instance "$instance_id" "$instance_name"; then
        ((success_count++))
    else
        ((failed_count++))
    fi

    echo ""
done

# 总结
echo "=========================================="
echo "📊 更新总结"
echo "=========================================="
echo -e "成功: ${GREEN}${success_count}${NC} 个实例"
echo -e "失败: ${RED}${failed_count}${NC} 个实例"
echo ""

if [ $failed_count -eq 0 ]; then
    echo -e "${GREEN}🎉 所有实例更新成功！${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  部分实例更新失败${NC}"
    exit 1
fi
