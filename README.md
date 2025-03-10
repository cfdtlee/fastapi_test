# URL 处理工具

这是一个使用 FastAPI 和 Next.js 构建的 URL 处理工具。

## 项目结构

- `/backend` - FastAPI 后端
- `/frontend` - Next.js 前端

## 部署说明

### 后端部署 (Railway)
1. 部署 `/backend` 目录
2. 设置环境变量 `FRONTEND_URL` 为前端 URL

### 前端部署 (Railway)
1. 部署 `/frontend` 目录
2. 设置环境变量 `NEXT_PUBLIC_API_URL` 为后端 URL 