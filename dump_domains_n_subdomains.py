import subprocess
import json
from dotenv import load_dotenv
import os

load_dotenv()
health_check_webhook = os.getenv("health_check_webhook")

def healthcheck(message):
    command = f'curl -X POST -H "Content-type: application/json" --data \'{{"text":"{message}"}}\' "{health_check_webhook}" --silent'
    output = subprocess.check_output(command, shell=True).decode().strip()
    output.strip()
    return

def debugg(function_name):
    subprocess.check_output(f"echo {function_name} Passed!",shell=True, universal_newlines=True)
    return

def aws_command_working():
    #healthcheck("Running aws_command_working")
    command = "aws route53 list-hosted-zones | notify --silent"
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def get_route53_hosted_zones():
    cmd = "aws route53 list-hosted-zones"

    output = subprocess.check_output(cmd.split()).decode("utf-8")
    data = json.loads(output)

    hosted_zones = data["HostedZones"]
    debugg("get_route53_hosted_zones")
    return hosted_zones

def extract_subdomains(domain_name, record_sets):
    subdomains = []
    for record_set in record_sets:
        name = record_set["Name"]
        if name.endswith(domain_name):
            subdomain = name[: -len(domain_name)].rstrip(".")
            if subdomain:
                subdomains.append(subdomain)
    return subdomains

def remove_trailing_dots(input_file, output_file):
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            cleaned_line = line.rstrip('.\n')
            f_out.write(cleaned_line + '\n')
    print("Trailing dots have been removed from domains_with_dot.txt and output saved to all_domains.txt")

def main():
    #healthcheck("Debug-1.1")
    hosted_zones = get_route53_hosted_zones()
    domains = []
    input_file = 'domains_with_dot.txt'
    output_file = 'all_domains.txt'
    
    for hosted_zone in hosted_zones:
        domain_name = hosted_zone["Name"]

        record_sets_cmd = "aws route53 list-resource-record-sets --hosted-zone-id {}".format(hosted_zone['Id'])
        record_sets_output = subprocess.check_output(record_sets_cmd.split()).decode("utf-8")
        record_sets_data = json.loads(record_sets_output)
        record_sets = record_sets_data["ResourceRecordSets"]
        subdomains = extract_subdomains(domain_name, record_sets)
        domains.append(domain_name)
        domains.extend([subdomain + "." + domain_name for subdomain in subdomains])

    with open("domains_with_dot.txt", "w") as file:
        for domain in domains:
            file.write(domain + "\n")
    remove_trailing_dots(input_file, output_file)
    subprocess.check_output("sort -u all_domains.txt -o sorted_all_domains.txt", shell=True, universal_newlines=True)
    print("Domains and subdomains saved to domains_with_dot.txt")

if __name__ == "__main__":
    main()
