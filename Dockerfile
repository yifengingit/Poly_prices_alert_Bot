# 使用官方 Python 3.12 轻量级镜像
FROM python:3.12-slim-bookworm

# 安装 uv 包管理器
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 设置工作目录
WORKDIR /app

# 设置环境变量
# 确保 Python 输出直接打印到终端，不缓存
ENV PYTHONUNBUFFERED=1
# 编译字节码以加快启动速度
ENV UV_COMPILE_BYTECODE=1

# 1. 先只复制依赖文件，利用 Docker 缓存层
COPY pyproject.toml uv.lock .python-version ./

# 2. 安装依赖
# --frozen: 严格按照 lock 文件安装
# --no-dev: 生产环境不需要开发依赖
RUN uv sync --frozen --no-dev

# 3. 复制项目所有代码
COPY . .

# 4. 将 .venv 加入 PATH，这样可以直接使用 `python` 而不是 `.venv/bin/python`
ENV PATH="/app/.venv/bin:$PATH"

# 启动命令
# 运行 Telegram Bot
CMD ["python", "backend/app/bot/main.py"]
