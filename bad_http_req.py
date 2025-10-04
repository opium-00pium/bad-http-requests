# bad_http_req.py
# Author: 0pium
# Version: 3.0 (Advanced)

import requests
import argparse
import sys
import os
import json
from urllib.parse import urlparse

# 在Windows上尝试启用ANSI转义序列，以便颜色可以正常显示
if sys.platform == "win32":
    os.system("")

# 默认的User-Agent
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
}

class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'

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

def check_http_methods(url, custom_data=None, custom_headers=None):
    """
    对给定的URL测试HTTP方法，支持自定义数据和请求头
    """
    print(f"[*] 正在扫描目标URL: {Colors.CYAN}{url}{Colors.RESET}\n")

    # 合并默认请求头和用户自定义请求头
    final_headers = DEFAULT_HEADERS.copy()
    if custom_headers:
        final_headers.update(custom_headers)
    
    # 打印出最终使用的请求头和数据（如果存在）
    print(f"[*] 使用以下请求头进行扫描:")
    for key, value in final_headers.items():
        print(f"    {Colors.BOLD}{key}{Colors.RESET}: {value}")
    if custom_data:
        print(f"[*] 将为POST/PUT请求附加以下数据:")
        print(f"    {custom_data}")
    print("-" * 50)


    # 禁用requests库关于InsecureRequestWarning的警告
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

    try:
        response = requests.options(url, headers=final_headers, timeout=10, verify=False)
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
        'COPY', 'MOVE', 'SEARCH', 'OPTIONS', 'CONNECT', 'TEST', 'GARBAGE',
        'PROPFIND', 'PROPPATCH', 'MKCOL', 'LOCK', 'UNLOCK'
    ]

    enabled_methods = []

    for method in methods_to_test:
        try:
            # 准备请求参数
            request_kwargs = {'headers': final_headers, 'timeout': 10, 'verify': False}
            
            # 如果是POST或PUT请求，并且用户提供了数据，则附加数据
            if method in ['POST', 'PUT'] and custom_data:
                # 尝试将数据作为JSON发送，这是API最常见的方式
                try:
                    request_kwargs['json'] = json.loads(custom_data)
                except json.JSONDecodeError:
                    # 如果不是有效的JSON，则作为原始数据发送
                    request_kwargs['data'] = custom_data

            response = requests.request(method, url, **request_kwargs)

            if response.status_code == 405:
                status_colored = f"{Colors.GREEN}{response.status_code} Method Not Allowed{Colors.RESET}"
            elif 200 <= response.status_code < 300:
                status_colored = f"{Colors.RED}{response.status_code} {response.reason}{Colors.RESET} <-- {Colors.BOLD}危险! 方法可能已启用!{Colors.RESET}"
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
    else:
        print(f"{Colors.GREEN}[+] 总结: 未发现明显启用的危险HTTP方法。{Colors.RESET}")


if __name__ == '__main__':
    print_banner()
    parser = argparse.ArgumentParser(
        description=f'{Colors.BOLD}BAD HTTP REQUESTS{Colors.RESET} - 一款支持自定义请求头和数据，用于扫描潜在不安全HTTP方法的工具。',
        epilog='使用示例: python bad_http_req.py -u "http://example.com" -H "Authorization: Bearer <token>"',
        formatter_class=argparse.RawTextHelpFormatter # 保持帮助文本的格式
    )
    parser.add_argument('-u', '--url', required=True, help='必须项：要扫描的目标URL\n(e.g., "http://example.com/api/user")')
    parser.add_argument('-d', '--data', help='可选项：为POST/PUT请求提供的请求体数据。\n通常是一个JSON字符串 (e.g., \'{"key":"value"}\')')
    parser.add_argument('-H', '--header', action='append', help='可选项：添加自定义请求头。\n此参数可使用多次 (e.g., -H "X-API-Key: 12345" -H "Content-Type: application/json")')

    args = parser.parse_args()
    
    # 解析自定义请求头
    headers_dict = {}
    if args.header:
        for header in args.header:
            if ':' in header:
                key, value = header.split(':', 1)
                headers_dict[key.strip()] = value.strip()
            else:
                print(f"{Colors.RED}[!] 错误: 请求头格式不正确: '{header}'。应为 'Key: Value' 格式。{Colors.RESET}")
                sys.exit(1)

    parsed_url = urlparse(args.url)
    if not parsed_url.scheme or not parsed_url.netloc:
        print(f"\n{Colors.RED}[!] 错误: 无效的URL格式。请输入完整的URL。{Colors.RESET}")
        sys.exit(1)

    check_http_methods(args.url, custom_data=args.data, custom_headers=headers_dict)