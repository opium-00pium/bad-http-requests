<div align="center">
  <h1>🔥 BAD HTTP REQUESTS 🔥</h1>
  <h3>BY 0pium</h3>
  <p>
    一个快速、简洁的命令行工具，用于扫描Web服务器上启用的潜在不安全HTTP方法。
  </p>
  
  <p>
    <a href="https://github.com/opium-00pium/bad-http-requests/actions/workflows/release.yml"><img src="https://github.com/opium-00pium/bad-http-requests/actions/workflows/release.yml/badge.svg" alt="Build Status"></a>
    <a href="https://github.com/opium-00pium/bad-http-requests/releases/latest"><img src="https://img.shields.io/github/v/release/opium-00pium/bad-http-requests?label=latest%20release&color=blue" alt="Latest Release"></a>
    <img src="https://img.shields.io/badge/Python-3.10+-blueviolet" alt="Python Version">
  </p>
</div>

---

<p align="center">
  <img src="img/screenshot.png" alt="Tool Demo">
</p>

## ➤ 核心功能

- **🚀 广泛扫描**: 检测十余种潜在危险的HTTP方法，包括 `PUT`, `DELETE`, `COPY`, `MOVE`, `TRACE` 等。
- **🎨 彩色高亮**: 使用直观的颜色（红/黄/绿）区分危险、可疑和安全的方法，结果一目了然。
- **⚙️ 高度自定义**: 支持通过 `-H` 添加自定义请求头（如`Authorization`），通过 `-d` 为`POST/PUT`请求附加数据。
- **📦 自动构建**: 通过GitHub Actions在每次代码推送到`main`分支后自动构建Windows `.exe` 文件。
- **💡 轻量快速**: 无需复杂依赖，执行迅速。

## ➤ 为何关注危险HTTP方法?

错误的服务器配置可能允许攻击者执行高风险操作，从而导致严重的安全漏洞。本工具旨在快速发现这些配置问题。

| 方法          | 潜在风险                                                     |
| :------------ | :----------------------------------------------------------- |
| `PUT`         | 上传任意文件，例如WebShell，导致远程代码执行。               |
| `DELETE`      | 删除服务器上的任意文件或资源，破坏网站或服务。               |
| `COPY` / `MOVE` | 复制或移动服务器上的文件，可能泄露敏感配置或覆盖关键文件。 |
| `TRACE`       | 用于跨站追踪（XST）攻击，可能窃取用户的Cookie。            |
| `CONNECT`     | 将服务器变成攻击跳板（代理），用于攻击其他系统。             |
| `SEARCH`      | 泄露未公开的文件信息，或通过复杂查询导致服务器拒绝服务（DoS）。 |

## ➤ 如何使用

我们提供两种使用方式：为普通用户准备的开箱即用的`.exe`文件，和为开发者准备的源码运行方式。

### 方式一：直接运行 (Windows用户推荐)

1.  访问本仓库的 [**Releases**](https://github.com/opium-00pium/bad-http-requests/releases) 页面。
2.  下载最新版本的 `bad_http_req.exe` 文件。
3.  打开PowerShell，进入文件所在目录，然后运行：

    ```powershell
    # 基础用法
    ./bad_http_req.exe -u http://example.com/api/user
    ```

### 方式二：从源码运行 (所有平台)

1.  确保您已安装 Python 3。
2.  克隆本仓库：
    ```bash
    git clone https://github.com/opium-00pium/bad-http-requests.git
    cd bad-http-requests
    ```
3.  安装依赖库：
    ```bash
    pip install requests
    ```
4.  运行脚本：
    ```bash
    # 基础用法
    python bad_http_req.py -u http://example.com/api/user
    ```

## ➤ 高级用法示例

利用 `-H` 和 `-d` 参数，您可以模拟更复杂的请求。

### 添加认证Token

当测试需要登录才能访问的接口时，这非常有用。

```bash
python bad_http_req.py -u http://api.example.com/v1/user -H "Authorization: Bearer yourSecretTokenGoesHere"
```

### 发送POST数据

模拟登录或提交表单。**注意：如果JSON数据中包含双引号，请用单引号将整个数据包起来。**

```bash
python bad_http_req.py -u http://api.example.com/v1/login -d '{"username":"admin","password":"password123"}'
```

### 组合使用

您可以将所有参数组合起来，进行一次非常具体的、高度自定义的扫描。

```bash
python bad_http_req.py -u http://api.example.com/v1/messages -H "Authorization: Bearer yourSecretTokenGoesHere" -H "Content-Type: application/json" -d '{"recipient":"user_a","message":"Hello World"}'
```

## ➤ 开发与贡献

欢迎提交Pull Request或提出Issues！

## ➤ ⚠️ 免责声明

本工具仅供授权的渗透测试和安全教育目的使用。严禁在未经目标系统所有者明确许可的情况下使用本工具进行扫描或攻击。

对于因滥用本工具而导致的任何法律责任或损害，作者概不负责。请在法律和道德允许的范围内使用。
