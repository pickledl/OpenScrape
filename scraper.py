import requests
import time
import os
from colorama import Fore, Style, init

init()

# ==== CONFIGURATION ====
start_user_id = 53646466       # Starting user ID - counts up from this id
item_id = 140823690        # Item ID to check for
delay_seconds = 0.3        # Delay between requests to avoid rate limiting
# ========================

# Output file in same folder as script
output_file = os.path.join(os.path.dirname(__file__), "ids.txt")
output_file2 = os.path.join(os.path.dirname(__file__), "users.txt")

user_id = start_user_id
print("\n--------------------------------------")
print("             OpenScrape\n")
print("https://github.com/pickledl/OpenScrape    ")
print("--------------------------------------\n\n")


def check(item_id2):
    url = f"https://inventory.roblox.com/v1/users/{user_id}/items/accessories/{item_id2}"
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        if response.status_code == 400:
            print(Fore.LIGHTBLACK_EX + f"[!] Failed for ID {user_id} - HTTP {response.status_code} (User Terminated)")
            return False
        elif response.status_code == 429:
            print(Fore.LIGHTBLACK_EX + f"[!] Failed for ID {user_id} - HTTP {response.status_code} (Rate Limit Exceeded)")
            time.sleep(5)
            return check(item_id2)
        else:
            print(Fore.RED + f"Error {response.status_code}")
    else:
        data = response.json()

        # Item Check
        if any(item.get("id") == item_id2 for item in data.get("data", [])):
            return True
        else:
            return False
    
def id2user(uid):
    url = f"https://users.roblox.com/v1/users/{uid}"
    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        if response.status_code == 400:
            print(Fore.LIGHTBLACK_EX + f"[!] Failed for ID {user_id} - HTTP {response.status_code} (User Terminated)")
            return False
        elif response.status_code == 429:
            print(Fore.LIGHTBLACK_EX + f"[!] Failed for ID {user_id} - HTTP {response.status_code} (Rate Limit Exceeded)")
            time.sleep(5)
            return id2user(uid)
        else:
            print("Error {response.status_code}")
    else:
        data = response.json()
        return(data.get("name", []))
            
# Console Pizzazz
while True:
    try:
        if check(item_id)==True:
            print(Fore.WHITE + f"[✓] Found item {item_id} for user {user_id} [✓]")
            time.sleep(delay_seconds)
            if check(102611803)==True:
                print(Fore.LIGHTYELLOW_EX + f"[!] User {user_id} is Verified (Hat) [!]")
            else:
                time.sleep(delay_seconds)
                if check(1567446)==True:
                    print(Fore.LIGHTYELLOW_EX + f"[!] User {user_id} is Verified (Sign) [!]")
                else:
                    print(Fore.LIGHTGREEN_EX + f"[✓] User {user_id} is Unverified [✓]")
                    with open(output_file, "a") as f:
                        f.write(f"{user_id}\n")
                    with open(output_file2, "a") as f:
                        f.write(f"{id2user(user_id)}\n")
                    print(Fore.LIGHTCYAN_EX + f"[✓] Successfully Saved [✓]")
        user_id += 1
        time.sleep(delay_seconds)
    except Exception as e:
        print(f"[ERROR] {e}")
        user_id += 1
        time.sleep(delay_seconds)