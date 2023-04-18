import os
import socket
import time

# Function to get the IP address of a domain using a DNS lookup
def get_ip(domain):
    return socket.gethostbyname(domain)

# Function to update the IP address at a specific line number in the specified file
def update_ip_in_file(ip, file_path, line_number, domain):
    # Open the file in read mode and read its content into a list of lines
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Format the new IP address line
    ip_line = f"    - \"{ip}\" # {domain}\n"
    # Replace the specified line with the new IP address line
    lines[line_number - 1] = ip_line

    # Open the file in write mode and write the updated content
    with open(file_path, 'w') as file:
        file.writelines(lines)

# Function to reload the CrowdSec configuration
def reload_crowdsec():
    os.system('systemctl reload crowdsec')

# Main function
def main():
    # Domain names to look up
    domain1 = <DOMAIN1>
    domain2 = <DOMAIN2>
    # Path to the configuration file
    config_file = <CONFIG_FILE>
    # Line numbers to insert the IP addresses
    line_number1 = <LINE1>
    line_number2 = <LINE2>
    # Time interval (in seconds) to check for IP changes
    check_interval = 3600

    # Get the current IP addresses for both domains
    current_ip1 = get_ip(domain1)
    current_ip2 = get_ip(domain2)

    # Update the configuration file with the current IP addresses
    update_ip_in_file(current_ip1, config_file, line_number1, domain1)
    update_ip_in_file(current_ip2, config_file, line_number2, domain2)
    # Reload the CrowdSec configuration
    reload_crowdsec()

    # Continuously check for IP changes
    while True:
        # Get the current IP addresses for both domains
        new_ip1 = get_ip(domain1)
        new_ip2 = get_ip(domain2)

        ip_changed = False

        # Check if the IP address for domain1 has changed
        if new_ip1 != current_ip1:
            print(f"IP for {domain1} changed from {current_ip1} to {new_ip1}")
            current_ip1 = new_ip1
            # Update the configuration file with the new IP address
            update_ip_in_file(current_ip1, config_file, line_number1)
            ip_changed = True
        else:
            print(f"IP for {domain1} remains the same: {current_ip1}")

        # Check if the IP address for domain2 has changed
        if new_ip2 != current_ip2:
            print(f"IP for {domain2} changed from {current_ip2} to {new_ip2}")
            current_ip2 = new_ip2
            # Update the configuration file with the new IP address
            update_ip_in_file(current_ip2, config_file, line_number2)
            ip_changed = True
        else:
            print(f"IP for {domain2} remains the same: {current_ip2}")

        # If one or both IP addresses have been modified, reload the CrowdSec configuration
        if ip_changed:
            reload_crowdsec()

        # Wait for the specified time interval before checking again
        time.sleep(check_interval)

# Entry point of the script
if __name__ == "__main__":
    main()
