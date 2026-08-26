#!/bin/bash
# 部署侧的自动更新：从远端拉取最新数据并重启静态服务。
#
# 数据本身由 GitHub Actions 每周刷新并提交（见 .github/workflows/update-data.yml），
# 这台机器只负责同步，不在本地跑下载与转换 —— 这样线上内容永远等于仓库内容，
# 不会出现「机器上的数据和 git 里不一致」的分叉。
#
# 安装（重要）：拷到仓库外再执行，不要直接跑仓库里的这份。
#   sudo install -m 755 scripts/pull_and_restart.sh /usr/local/bin/aws-gpu-update.sh
# 因为脚本会 git reset --hard，如果它自己就在被重置的目录里，
# 遇到「目标提交尚未包含此脚本」的情况会把自己删掉，然后报 exit 127。
#
# 用法（root，通常由 cron 调用）:
#   /usr/local/bin/aws-gpu-update.sh [branch]
#
# 踩过的两个坑，所以下面两行不能省：
#   1. cron/SSM 以 root 运行时 HOME 可能为空，git config --global 会写不到任何地方
#   2. 仓库属主是 ec2-user 而执行者是 root，git 会因 "dubious ownership" 拒绝操作，
#      而且失败是静默的 —— 服务重启照样成功，代码却没更新
set -uo pipefail

export HOME=/root
REPO=/home/ubuntu/codes/aws-gpu
BRANCH="${1:-main}"
SERVICE=aws-gpu-server
RUN_USER=ec2-user

log() { echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] $*"; }

git config --global --get-all safe.directory | grep -qx "$REPO" \
    || git config --global --add safe.directory "$REPO"

cd "$REPO" || { log "FATAL: $REPO 不存在"; exit 1; }

BEFORE=$(git rev-parse HEAD)

if ! git fetch --quiet origin "$BRANCH"; then
    log "FATAL: git fetch 失败"
    exit 1
fi

AFTER=$(git rev-parse "origin/$BRANCH")

if [ "$BEFORE" = "$AFTER" ]; then
    log "已是最新 ($BEFORE)，无需重启"
    exit 0
fi

log "更新 $BEFORE -> $AFTER"
git reset --hard --quiet "origin/$BRANCH" || { log "FATAL: reset 失败"; exit 1; }
chown -R "$RUN_USER:$RUN_USER" "$REPO"

systemctl restart "$SERVICE" || { log "FATAL: 重启 $SERVICE 失败"; exit 1; }
sleep 3

# 上线校验：只确认服务活着不够，要真的取到页面
CODE=$(curl -s -o /dev/null -w '%{http_code}' -m 15 http://127.0.0.1:3000/ || echo 000)
if [ "$CODE" != "200" ]; then
    log "FATAL: 重启后首页返回 $CODE，回滚到 $BEFORE"
    git reset --hard --quiet "$BEFORE"
    chown -R "$RUN_USER:$RUN_USER" "$REPO"
    systemctl restart "$SERVICE"
    exit 1
fi

log "OK: 已更新到 $(git log --oneline -1)"
