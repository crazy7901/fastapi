### 第一步：dockerfile文件的建立
```Dockerfile
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制项目依赖文件
COPY requirements.txt requirements.txt

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 8000

# 启动 FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 第二步：

1. **构建 Docker 镜像**

   在确认 `requirements.txt` 中使用了 `oss2` 并更新了 Dockerfile 之后，重新构建 Docker 镜像：

    ```bash
    #docker build -t my-fastapi-app .
   docker buildx build --platform linux/amd64 -t my-fastapi-app .
    ```

2. **运行容器**

   然后再次运行容器：

    ```bash
    docker run -d -p 8000:8000 --name my-fastapi-app my-fastapi-app
    ```


### 第三步：


```bash
# 本地机器上导出镜像
#docker save -o my-fastapi-app.tar crazy7901/my-fastapi-app:v1
#docker save -o my-fastapi-app.tar my-fastapi-app
docker save -o my-fastapi-app.tar linux/my-fastapi-app:v1.0

# 打标签
docker tag my-fastapi-app linux/my-fastapi-app:v1.0

# 上传到dockerhub
docker push linux/my-fastapi-app:v1.0

# 使用 scp 或其他工具将 tar 文件上传到云服务器
scp -r /Users/chen/PycharmProjects/fastapi/my-fastapi-app.tar root@8.152.0.110:/images/my-fastapi-app.tar
# 云服务器上导入镜像
docker load -i my-fastapi-app.tar

# 更新新的镜像包

#停止并移除正在运行的旧容器
docker stop container-id
docker rm container-id

# 使用新导入的镜像启动新的容器
docker run -d -p 8000:8000 --name my-fastapi-app my-fastapi-app
docker run -d -p 8000:8000 --name my-fastapi-app linux/my-fastapi-app:v1.0
```


### 番外：上传到docker hub并拉取
很好！现在，你已经成功构建了 Docker 镜像，并确认它可以正常运行。接下来，你可以将这个容器部署到云服务器上。以下是具体的步骤：

### 1. **准备云服务器**
确保你已经有一个运行中的云服务器（如 AWS EC2、Google Cloud VM、Azure VM 或其他提供商的服务器），并且可以通过 SSH 访问。

### 2. **将 Docker 镜像推送到 Docker Registry**
首先，你需要将本地构建好的 Docker 镜像推送到 Docker Registry，例如 Docker Hub。

#### 登录 Docker Hub
```bash
docker login
```

#### 为 Docker 镜像打标签
```bash
docker tag my-fastapi-app crazy7901/my-fastapi-app:v1
```

将 `username` 替换为你的 Docker Hub 用户名，`v1` 为版本号。

#### 推送镜像到 Docker Hub
```bash
docker push crazy7901/my-fastapi-app:v1.1
```

### 3. **在云服务器上拉取并运行 Docker 镜像**
完成上一步后，登录到你的云服务器并执行以下操作。

#### 登录云服务器
使用 SSH 登录到你的云服务器：

```bash
ssh username@your-server-ip
```

#### 安装 Docker（如果尚未安装）
如果你的云服务器还没有安装 Docker，首先安装 Docker。

- **Ubuntu:**

    ```bash
    sudo apt-get update
    sudo apt-get install -y docker.io
    ```

- **CentOS:**

    ```bash
    sudo yum install -y docker
    ```

启动并启用 Docker 服务：

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

#### 从 Docker Hub 拉取镜像
```bash
docker pull username/my-fastapi-app:v1
```

#### 运行容器
```bash
docker run -d -p 8000:8000 --name my-fastapi-app username/my-fastapi-app:v1
```

在这个命令中：
- `-d` 选项表示容器将以分离模式（后台）运行。
- `-p 8000:8000` 映射容器的 8000 端口到云服务器的 8000 端口。
- `--name my-fastapi-app` 为容器指定了一个名称。

### 4. **设置防火墙规则**
确保你的云服务器允许外部访问 8000 端口。如果你使用的是 AWS EC2、Google Cloud、Azure VM 等，可能需要在安全组或防火墙设置中允许该端口。

### 5. **访问部署的应用**
在浏览器中访问 `http://your-server-ip:8000`，你应该能看到你的 FastAPI 应用已成功运行在云服务器上。

### 6. **（可选）配置持久化存储和环境变量**
如果你的应用需要持久化数据，或者依赖于某些环境变量，你可以使用 Docker 的卷（Volumes）和环境变量功能：

- **挂载卷**：

    ```bash
    docker run -d -p 8000:8000 -v /host/path:/container/path --name my-fastapi-app username/my-fastapi-app:v1
    ```

- **设置环境变量**：

    ```bash
    docker run -d -p 8000:8000 -e MY_ENV_VAR=value --name my-fastapi-app username/my-fastapi-app:v1
    ```

至此，你的 Docker 容器已经成功部署到云服务器上，并可供外部访问。