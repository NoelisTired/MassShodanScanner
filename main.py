import requests, os, sys, colorama
from colorama import Fore, Back
colorama.init(autoreset=True)

apikey = "" # Shodan API Key (Preferably a paid one)

def main():
    vulnerable = []
    safe = []
    os.system("title [NoelP Mass Shodan Vulnerability Scanner]")
    if ".txt" in sys.argv[1]:
        with open(sys.argv[1], "r") as f:
            for line in f:
                ip = line.strip()
                r = requests.get("https://api.shodan.io/shodan/host/{}?key={}".format(ip, apikey))
                if r.status_code == 429:
                    print(Fore.RED + "[-] Rate Limited")
                    input("Please press ENTER to continue")
                if r.status_code != 200:
                    continue
                try: #! Could in theory be written better but this works and i really want to sleep tonight
                    if len(r.json()['vulns']):
                        print("{}[+] {} is vulnerable with {} vulnerabilities".format(Fore.RED, ip, len(r.json()['vulns'])))
                        vulnerable.append(ip)
                    else:
                        print("{}[-] {} is not vulnerable".format(Fore.LIGHTCYAN_EX, ip))
                        safe.append(ip)
                except KeyError:
                    print("{}[-] {} is not vulnerable".format(Fore.LIGHTCYAN_EX, ip))
                    safe.append(ip)

            #! Saving vulnerable and safe IPs to files        
            x = input("Finished! Would you like to save the results? (y/n): ")
            if x.lower() == "y":
                with open("vulnerable.txt", "w") as f:
                    for ip in vulnerable:
                        f.write(f"{ip}\n")  
                with open("safe.txt", "w") as f:
                    for ip in safe:
                        f.write(f"{ip}\n")           
                print("Saved vulnerable.txt and safe.txt")
            else:
                print("Exiting...")
                exit(0)

    else:
        print("Usage: python3 main.py <ip-list.txt>")
        input()

if __name__ == "__main__":
    try:
        print("Scanning {} IPs".format(len(open(sys.argv[1], "r").readlines())))
        main()
    except IndexError:
        print("Usage: python3 main.py <ip-list.txt>")
        input()
        sys.exit()
