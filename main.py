import requests
from datetime import datetime
import re
def get_adguard_mixed_list():
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
        f.write(f"! homepage: https://github.com/baiyi115/Ad-list")
        f.write(f"! License: https://github.com/baiyi115/Ad-list/blob/main/LICENSE")
        f.write("\n")
        for rule in sorted_rules:
            f.write(rule + "\n")

    print(f"\n 共 {len(all_rules)} 条规则已保存至 adguard_mixed_list.txt")

def extract_domains(file_path):
    domains = []
    keywords = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line or re.search(r'^[!@#]|[*$~]', line):
                continue
            match = re.search(r"\|\|([a-zA-Z0-9.-]+)\^", line)
            if match:
                domains.append(match.group(1))
    return sorted(domains)

def mosdns_rules(domains):
    with open("mosdns_mixed_list.txt", "w") as f:
        f.write("# tittle: mosdns_mixed_list\n")
        f.write(f"# build time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"# total: {len(domains)}\n")
        f.write(f"# homepage: https://github.com/baiyi115/Ad-list\n")
        f.write(f"# License: https://github.com/baiyi115/Ad-list/blob/main/LICENSE\n")
        for domain in domains:
            f.write("domain:" + domain + "\n")
        print(f"\n 共 {len(domains)} 条规则已保存至 mosdns_mixed_list")

if __name__ == "__main__":
    get_adguard_mixed_list()
    domains=extract_domains("adguard_mixed_list.txt")
    mosdns_rules(domains)