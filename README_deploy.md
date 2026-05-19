# 部署说明

## 文件结构

```
实验室index排机/
├── app.py                  # Flask 服务
├── auto_schedule.py        # 排机核心逻辑
├── hybrid_group_mapping.py # 映射表
├── requirements.txt
├── templates/
│   └── index.html
├── uploads/                # 自动创建，临时存放上传文件
└── outputs/                # 自动创建，存放排机结果
```

## 腾讯云服务器部署步骤

### 1. 上传代码

```bash
# 在本地执行，把整个目录上传到服务器
scp -r /path/to/实验室index排机 ubuntu@<服务器IP>:~/lab_schedule
```

### 2. 安装依赖

```bash
cd ~/lab_schedule
pip3 install -r requirements.txt
```

### 3. 开放端口

在**腾讯云控制台 → 安全组**，添加入站规则：
- 协议：TCP
- 端口：19527
- 来源：0.0.0.0/0

### 4. 启动服务（后台常驻）

```bash
# 使用 nohup 后台运行
nohup python3 app.py > app.log 2>&1 &

# 查看日志
tail -f app.log
```

### 5. 访问

浏览器打开：`http://<服务器IP>:19527`

---

## 可选：使用 systemd 守护进程（推荐）

创建 `/etc/systemd/system/lab_schedule.service`：

```ini
[Unit]
Description=Lab Schedule Web App
After=network.target

[Service]
WorkingDirectory=/root/lab_schedule
ExecStart=/usr/bin/python3 /root/lab_schedule/app.py
Restart=always
User=root

[Install]
WantedBy=multi-user.target
```

```bash
systemctl daemon-reload
systemctl enable lab_schedule
systemctl start lab_schedule
systemctl status lab_schedule
```

## 注意事项

- `uploads/` 目录里的临时文件会在处理完后自动删除
- `outputs/` 目录里的结果文件会一直保留，可定期手动清理，或加一个 cron 定时清理：
  ```
  0 3 * * * find /root/lab_schedule/outputs -mtime +7 -delete
  ```
