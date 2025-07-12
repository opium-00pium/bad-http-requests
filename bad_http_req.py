# bad_http_req.py
# Author: 0pium

import requests
import argparse
import sys
import os
from urllib.parse import urlparse

# 在Windows上尝试启用ANSI转义序列，以便颜色可以正常显示
if sys.platform == "win32":
    os.system("")

# 设置一个更像真实浏览器的User-Agent
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    CYAN = '\033[96m'

def print_banner():
    """打印一个漂亮的横幅"""
    banner_width = 49
    title = f"{Colors.CYAN}BAD HTTP REQUESTS{Colors.RESET}".center(banner_width + len(Colors.CYAN) + len(Colors.RESET))
    author = f"{Colors.YELLOW}BY 0pium{Colors.RESET}".center(banner_width + len(Colors.YELLOW) + len(Colors.RESET))

    banner_str = f"""
    {Colors.RED}###################################################{Colors.RESET}
    #{" ".center(banner_width)}#
    #{title}#
    #{author}#
    #{" ".center(banner_width)}#
    {Colors.RED}###################################################{Colors.RESET}
    """
    print(banner_str)

def check_http_methods(url):
    """
    对给定的URL测试HTTP方法
    """
    print(f"[*] 正在扫描目标URL: {Colors.CYAN}{url}{Colors.RESET}\n")

    # 禁用requests库关于InsecureRequestWarning的警告
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    try:
        response = requests.options(url, headers=HEADERS, timeout=10, verify=False)
        print(f"[*] 首先尝试 {Colors.YELLOW}OPTIONS{Colors.RESET} 方法...")
        if 'allow' in response.headers:
            allowed_methods = response.headers['allow']
            print(f"{Colors.GREEN}[+] 服务器通过 OPTIONS 响应明确表示支持以下方法: {allowed_methods}{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}[-] OPTIONS 响应头中未找到 'Allow' 字段。将进行逐一方法测试。{Colors.RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}[!] 发送 OPTIONS 请求失败: {e}{Colors.RESET}")

    print("\n[*] 开始逐一扫描所有潜在的HTTP方法...")

    methods_to_test = [
        'GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'PATCH', 'TRACE',
        'COPY', 'MOVE', 'SEARCH', 'OPTIONS', 'CONNECT', 'TEST', 'GARBAGE'
    ]

    enabled_methods = []

    for method in methods_to_test:
        try:
            response = requests.request(method, url, headers=HEADERS, timeout=10, verify=False)

            if response.status_code == 405:
                status_colored = f"{Colors.GREEN}{response.status_code} Method Not Allowed{Colors.RESET}"
            elif 200 <= response.status_code < 300:
                status_colored = f"{Colors.RED}{response.status_code} {response.reason}{Colors.RESET} <-- 危险! 方法可能已启用!"
                enabled_methods.append(method)
            elif response.status_code == 501:
                status_colored = f"{Colors.GREEN}{response.status_code} Not Implemented{Colors.RESET}"
            else:
                status_colored = f"{Colors.YELLOW}{response.status_code} {response.reason}{Colors.RESET}"

            print(f"    - 测试方法 {method:<8}: 收到状态码 -> {status_colored}")

        except requests.exceptions.RequestException as e:
            print(f"    - 测试方法 {method:<8}: 请求失败 -> {Colors.RED}{e}{Colors.RESET}")

    print("\n[*] 扫描完成！")
    if enabled_methods:
        print(f"{Colors.RED}[!] 总结: 发现以下潜在危险的HTTP方法被启用: {', '.join(enabled_methods)}{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] 建议: 请审查服务器配置，禁用所有非必要的HTTP方法。{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}[+] 总结: 未发现明显启用的危险HTTP方法。服务器配置看起来比较安全。{Colors.RESET}")


if __name__ == '__main__':
    print_banner()
    parser = argparse.ArgumentParser(
        description='BAD HTTP REQUESTS - A tool to scan for potentially insecure HTTP methods.',
        epilog='Use with caution and only on authorized systems. Happy hacking!'
    )
    parser.add_argument('-u', '--url', required=True, help='The target URL to scan (e.g., "http://example.com/test")')

    args = parser.parse_args()

    parsed_url = urlparse(args.url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print(f"\n{Colors.RED}[!] 错误: 无效的URL格式。请输入完整的URL，例如 'http://ip:port' 或 'https://example.com'。{Colors.RESET}")
        sys.exit(1)

    check_http_methods(args.url)