import requests
from datetime import datetime

# 1. 定义你的规则列表 URLs
list_urls = [
    "https://ghfast.top/raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt",
    "https://ruleset.skk.moe/Internal/reject-adguardhome.txt",
    "https://adrules.top/dns.txt"
]

all_rules = set() # 使用 set 自动去重

# 2. 循环获取和处理
for url in list_urls:
    try:
        response = requests.get(url)
        response.raise_for_status() # 如果请求失败则抛出异常

        lines = response.text.splitlines() 

        for line in lines:
            line = line.strip() 
            # 过滤掉注释、空行和无效规则
            if line and not line.startswith('#') and not line.startswith('!'):
                all_rules.add(line)
        
        print(f"成功处理: {url}")

    except requests.RequestException as e:
        print(f"处理失败: {url} - {e}")

sorted_rules = sorted(all_rules, key=lambda x: (not x.startswith('||'), x))

with open("adguard_mixed_list.txt", "w") as f:
    f.write("! tittle: AdGuard mixed list\n")
    f.write(f"! build time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"! total: {len(all_rules)}\n")
    f.write("! source:\n")
    for url in list_urls:
        f.write(f"! {url}\n")
    f.write("\n")
    for rule in sorted_rules:
        f.write(rule + "$dnsrewrite=NOERROR;;\n")

print(f"\n 整合完毕！总共 {len(all_rules)} 条规则已保存至 adguard_mixed_list.txt")