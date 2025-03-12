from shared_imports import os, time, subprocess
import varalyze_cli

def api_key_set():
    api_keys = ["ABUSEIPDB_API_KEY", "IPQUALITY_API_KEY", "URLSCAN_API_KEY", "VIRUSTOTAL_API_KEY"]
    for key in api_keys:
        value = os.getenv(key)
        if value is None:
            set_key = input(f"{key} not set. Please enter your API key or 'skip' if you don't wish to set this tool up: ")
            if set_key == 'skip':
                continue
            os.environ[key] = set_key
            subprocess.run(["setx", key, set_key], check=True)
        else:
            print(f"{key} - Already been set.")

def main():
    print("\033[1m" + "\n►►►►►►►►► Welcome to the API key setter ◄◄◄◄◄◄◄◄◄\n" + "\033[0m")
    api_key_set()
    print("\nReturning to main menu...")
    time.sleep(4)
    varalyze_cli.main()

if __name__ == "__main__":
    main()