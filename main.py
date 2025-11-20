import requests
from datetime import datetime

list_urls = [
    "https://ghfast.top/raw.githubusercontent.com/TG-Twilight/AWAvenue-Ads-Rule/main/AWAvenue-Ads-Rule.txt",
    "https://ruleset.skk.moe/Internal/reject-adguardhome.txt",
    "https://adrules.top/dns.txt"
]

all_rules = set()

for url in list_urls:
    try:
        response = requests.get(url)
        response.raise_for_status() 

        lines = response.text.splitlines() 

        for line in lines:
            line = line.strip() 
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
        f.write(rule + "\n")

print(f"\n 共 {len(all_rules)} 条规则已保存至 adguard_mixed_list.txt")
