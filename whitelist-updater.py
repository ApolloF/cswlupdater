import socket
import time
import sys
import os
import json

# Function to get the IP address for a domain
def get_ip(domain):
    return socket.gethostbyname(domain)

# Function to update the IP address in the specified file and line number
def update_ip_in_file(ip, file_path, line_number):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    ip_line = f"    - \"{ip}\"\n"
    lines[line_number - 1] = ip_line

    with open(file_path, 'w') as file:
        file.writelines(lines)

# Function to get user input and store them in a JSON configuration file
def setup(config_file):
    num_domains = int(input("Enter the number of domains: "))
    domains = [input(f"Enter domain {i + 1}: ") for i in range(num_domains)]
    line_numbers = [int(input(f"Enter the line number for domain {i + 1} IP: ")) for i in range(num_domains)]
    config_file_path = input("Enter the path to the config file: ")
    check_interval = int(input("Enter the check interval in seconds: "))

    config = {
        'domains': domains,
        'line_numbers': line_numbers,
        'config_file': config_file_path,
        'check_interval': check_interval
    }

    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

# Function to load the settings from a JSON configuration file
def load_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)

    return config['domains'], config['line_numbers'], config['config_file'], config['check_interval']

# Main function
def main():
    config_file = 'update_whitelist_ips_config.json'

    # Check if the script is run with the 'setup' argument
    if len(sys.argv) > 1 and sys.argv[1] == "setup":
        setup(config_file)
        return

    # Load the settings from the configuration file
    domains, line_numbers, config_file_path, check_interval = load_config(config_file)

    previous_ips = [None] * len(domains)

    # Continuously check for IP changes and update the file
    while True:
        for i, domain in enumerate(domains):
            current_ip = get_ip(domain)

            # If the IP has changed, update the file and reload crowdsec
            if current_ip != previous_ips[i]:
                print(f"Updating IP for {domain}...")
                update_ip_in_file(current_ip, config_file_path, line_numbers[i])
                previous_ips[i] = current_ip
                if os.system("systemctl reload crowdsec") == 0:
                    print(f"Successfully updated IP for {domain} and reloaded crowdsec.")
                else:
                    print(f"Error reloading crowdsec after updating IP for {domain}.")
            else:
                print(f"IP for {domain} hasn't changed.")

        time.sleep(check_interval)

if __name__ == "__main__":
    main()