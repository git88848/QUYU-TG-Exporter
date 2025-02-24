# 🚀 趋于飞机数据一键导出工具 (TG-Exporter)

一款功能强大的 Telegram 数据导出工具，支持多种数据类型导出和 Excel 格式保存。 🔥

## 🛠️ 部署说明

### 💻 系统要求
- 🪟 Windows/Linux/MacOS 操作系统
- 🐍 Python 3.7 或更高版本
- 🌐 网络能够访问 Telegram

### 📦 依赖安装
```bash
pip install telethon openpyxl
```

### ⚙️ 配置说明
1. 🔑 获取 Telegram API 凭据
   - 访问 https://my.telegram.org/apps
   - 登录您的 Telegram 账号
   - 创建一个新的应用程序
   - 记录下 `api_id` 和 `api_hash`

2. 🔧 修改配置信息
   - 打开 `tg_export.py`
   - 修改 `API_ID` 和 `API_HASH` 为你的值

## 🎯 使用说明

### 🚀 启动方式
```bash
python tg_export.py
```

### 📱 首次登录
- ☎️ 输入手机号 (格式：+8613812345678)
- 🔑 输入 Telegram 验证码
- 🔐 如有两步验证，输入密码

### 📂 支持导出
- 👥 联系人信息
  - 📱 用户ID和手机号
  - 👤 用户名和姓名
  - ⭐ 账号状态

- 👥 群组信息
  - 🆔 群组ID
  - 📝 群组名称
  - 🔗 邀请链接
  - ⭐ 群组状态

- 📢 频道信息
  - 🆔 频道ID
  - 📝 频道名称
  - 🔗 频道链接
  - ⭐ 频道状态

- 🤖 机器人信息
  - 🆔 机器人ID
  - 👤 用户名
  - 📝 机器人名称
  - ⭐ 状态信息

### 📊 导出格式
- 📑 Excel 文件格式
- 📋 自动调整列宽
- 🎨 清晰的数据分类
- 📁 独立的导出目录

## 📝 更新日志

### ✨ v1.0.0 (2025-02-25)
#### 🌟 首次发布
- 📱 支持联系人导出
- 👥 支持群组信息导出
- 📢 支持频道信息导出
- 🤖 支持机器人信息导出
- 🎨 美观的 Excel 格式
- 🔄 自动列宽调整
- 📊 详细的状态显示
- 🔗 支持导出邀请链接

## 🛠️ 技术特点
- 🔍 异步数据获取
- 📊 Excel 格式保存
- 🎯 智能状态检测
- 🔗 自动链接获取
- 💾 数据分类存储
- ⚡ 完整的错误处理

## 💫 联系方式与社群

### 🌟 Telegram 社群
- 📢 官方频道：[@QUYUkjpd](https://t.me/QUYUkjpd)
- 👥 交流群：[@QUYUkjq](https://t.me/QUYUkjq)
- 👨‍💻 作者：[@Lawofforce](https://t.me/Lawofforce)

🌈 欢迎加入我们的社群，获取最新更新和技术支持！

## 🎁 赞助支持

✨ 如果觉得这个程序对你有帮助，欢迎赞助支持！

### 💎 TRC20-USDT 钱包地址
```
TQ2gs6167orQSVWVNHWrKq9SZ8a5WRETZs
```
👆 点击上方复制按钮即可复制

<img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=TQ2gs6167orQSVWVNHWrKq9SZ8a5WRETZs" alt="TRC20-USDT 二维码" width="200"/>

🌟 您的支持是我们持续改进的动力！

## ⚠️ 免责声明
🔒 本工具仅供学习研究使用，请遵守相关法律法规，不得用于非法用途。使用本工具所产生的一切后果由使用者自行承担。使用本工具时请遵守相关法律法规和 Telegram 的服务条款。
