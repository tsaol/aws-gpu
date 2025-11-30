#!/bin/bash

# AWS GPU 项目首次部署脚本
# 用于在 EC2 实例上首次部署 aws-gpu 项目

# 不使用 set -e，手动处理错误
# set -e

# 配置
# 从环境变量读取实例ID，格式：AWS_GPU_INSTANCES="instance-id-1,instance-id-2"
if [ -z "$AWS_GPU_INSTANCES" ]; then
    echo "❌ 错误: 未设置环境变量 AWS_GPU_INSTANCES"
    echo "请设置环境变量："
    echo "  export AWS_GPU_INSTANCES=\"instance-id-1,instance-id-2\""
    exit 1
fi

# 将逗号分隔的字符串转换为数组
IFS=',' read -ra INSTANCES <<< "$AWS_GPU_INSTANCES"

GIT_REPO="https://github.com/tsaol/aws-gpu.git"
PROJECT_DIR="/home/ubuntu/codes/aws-gpu"
SERVICE_PORT=3000

echo "=========================================="
echo "AWS GPU 项目首次部署脚本"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 检查 AWS CLI
if ! command -v aws &> /dev/null; then
    echo -e "${RED}❌ 错误: 未找到 AWS CLI${NC}"
    exit 1
fi

echo "🚀 开始部署到 ${#INSTANCES[@]} 个实例..."
echo ""

# 部署函数
deploy_instance() {
    local instance_id=$1
    local instance_name=$2

    echo "=========================================="
    echo "📦 部署实例: $instance_name"
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

    # 使用 SSM 执行命令 - 分步执行，避免复杂参数
    echo "2️⃣  安装依赖..."

    # 步骤1: 安装 git 和 python3
    local cmd1_id=$(aws ssm send-command \
        --instance-ids "$instance_id" \
        --document-name "AWS-RunShellScript" \
        --parameters 'commands=["sudo apt-get update -qq && sudo apt-get install -y git python3 > /dev/null 2>&1 && echo Dependencies installed"]' \
        --timeout-seconds 300 \
        --query 'Command.CommandId' \
        --output text)

    if [ -z "$cmd1_id" ]; then
        echo -e "${RED}❌ 发送命令失败${NC}"
        return 1
    fi

    # 等待完成
    wait_for_command "$cmd1_id" "$instance_id" || return 1

    echo "3️⃣  克隆项目..."

    # 步骤2: 克隆项目
    local cmd2_id=$(aws ssm send-command \
        --instance-ids "$instance_id" \
        --document-name "AWS-RunShellScript" \
        --parameters "commands=[\"mkdir -p /home/ubuntu/codes && cd /home/ubuntu/codes && rm -rf aws-gpu && git clone $GIT_REPO && echo Project cloned\"]" \
        --timeout-seconds 180 \
        --query 'Command.CommandId' \
        --output text)

    if [ -z "$cmd2_id" ]; then
        echo -e "${RED}❌ 发送命令失败${NC}"
        return 1
    fi

    wait_for_command "$cmd2_id" "$instance_id" || return 1

    echo "4️⃣  执行部署脚本..."

    # 步骤3: 运行部署脚本
    local cmd3_id=$(aws ssm send-command \
        --instance-ids "$instance_id" \
        --document-name "AWS-RunShellScript" \
        --parameters "commands=[\"cd $PROJECT_DIR && chmod +x deploy.sh && sudo ./deploy.sh $SERVICE_PORT $PROJECT_DIR\"]" \
        --timeout-seconds 180 \
        --query 'Command.CommandId' \
        --output text)

    if [ -z "$cmd3_id" ]; then
        echo -e "${RED}❌ 发送命令失败${NC}"
        return 1
    fi

    wait_for_command "$cmd3_id" "$instance_id" || return 1

    echo ""
    echo -e "${GREEN}✅ 部署完成${NC}"
    return 0
}

# 等待命令完成的函数
wait_for_command() {
    local command_id=$1
    local instance_id=$2

    echo "   命令 ID: $command_id"
    echo -n "   等待执行"

    for i in {1..90}; do
        local status=$(aws ssm get-command-invocation \
            --command-id "$command_id" \
            --instance-id "$instance_id" \
            --query 'Status' \
            --output text 2>/dev/null || echo "Pending")

        if [ "$status" = "Success" ]; then
            echo ""
            echo -e "   ${GREEN}✅ 执行成功${NC}"

            # 显示输出
            local output=$(aws ssm get-command-invocation \
                --command-id "$command_id" \
                --instance-id "$instance_id" \
                --query 'StandardOutputContent' \
                --output text)

            if [ ! -z "$output" ]; then
                echo "   输出: $output"
            fi
            return 0
        elif [ "$status" = "Failed" ]; then
            echo ""
            echo -e "   ${RED}❌ 执行失败${NC}"

            # 显示错误
            local error=$(aws ssm get-command-invocation \
                --command-id "$command_id" \
                --instance-id "$instance_id" \
                --query 'StandardErrorContent' \
                --output text)

            if [ ! -z "$error" ]; then
                echo "   错误: $error"
            fi
            return 1
        fi

        printf "."
        sleep 2
    done

    echo ""
    echo -e "   ${RED}❌ 超时${NC}"
    return 1
}

# 部署所有实例
success_count=0
failed_count=0

for instance_id in "${INSTANCES[@]}"; do
    # 获取实例名称
    instance_name=$(aws ec2 describe-instances \
        --instance-ids "$instance_id" \
        --query 'Reservations[0].Instances[0].Tags[?Key==`Name`].Value' \
        --output text)

    if deploy_instance "$instance_id" "$instance_name"; then
        ((success_count++))
    else
        ((failed_count++))
    fi

    echo ""
done

# 总结
echo "=========================================="
echo "📊 部署总结"
echo "=========================================="
echo -e "成功: ${GREEN}${success_count}${NC} 个实例"
echo -e "失败: ${RED}${failed_count}${NC} 个实例"
echo ""

if [ $failed_count -eq 0 ]; then
    echo -e "${GREEN}🎉 所有实例部署成功！${NC}"
    echo ""
    echo "📝 后续更新请使用: ./update_instances.sh"
    exit 0
else
    echo -e "${YELLOW}⚠️  部分实例部署失败${NC}"
    exit 1
fi
