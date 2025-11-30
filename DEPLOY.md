# 🚀 PolyStatics Server Deployment Guide

本指南将帮助你将 Telegram 机器人部署到 Linux 服务器 (VPS)。

## 1. 准备工作 (Prerequisites)

你需要一台 Linux 服务器（推荐 Ubuntu 22.04 或 Debian 12）。
你需要安装 **Docker** 和 **Docker Compose**。

### 在服务器上安装 Docker (如果尚未安装)
```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 启动 Docker 并设置开机自启
sudo systemctl start docker
sudo systemctl enable docker
```

## 2. 部署步骤 (Deployment Steps)

### 步骤 A: 上传代码
你可以通过 `git` 拉取代码，或者直接上传文件。
确保服务器上有以下文件：
- `Dockerfile`
- `docker-compose.yml`
- `pyproject.toml`
- `uv.lock`
- `.python-version`
- `backend/` (文件夹)
- `.env` (配置文件)

**⚠️ 注意**: 不要上传 `.venv` 文件夹，Docker 会自动创建。

### 步骤 B: 配置环境变量 (.env)
在服务器项目目录下创建 `.env` 文件，并填入你的配置：
```bash
nano .env
```
内容示例：
```ini
TELEGRAM_BOT_TOKEN=你的Token
TELEGRAM_CHAT_ID=你的ChatID
# 如果有其他变量也请添加
```

### 步骤 C: 启动服务
在项目根目录下运行：

```bash
# 构建并后台启动
docker compose up -d --build
```

### 步骤 D: 查看状态
```bash
# 查看容器是否在运行
docker compose ps

# 查看实时日志
docker compose logs -f
```

## 3. 常用维护命令 (Maintenance)

*   **停止服务**: `docker compose down`
*   **重启服务**: `docker compose restart`
*   **更新代码后重新部署**:
    1.  `git pull` (拉取新代码)
    2.  `docker compose up -d --build` (重新构建并启动)
