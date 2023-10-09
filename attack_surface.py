import subprocess
import os
from dotenv import load_dotenv
import convertToCSV
import dump_domains_n_subdomains

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

load_dotenv()
health_check_webhook = os.getenv("health_check_webhook")

def healthcheck(message):
    command = f'curl -X POST -H "Content-type: application/json" --data \'{{"text":"{message}"}}\' "{health_check_webhook}" --silent'
    output = subprocess.check_output(command, shell=True).decode().strip()
    output.strip()
    return

def prob_sub_domains_slack():
    subprocess.check_output("echo 'Below New Domain have been Found' | notify --silent ; cat sorted_all_domains.txt | anew latest_all_domains.txt | notify --silent", shell=True, universal_newlines=True)
    command = "echo 'Running httpx if there are any newly domains identified' | notify --silent ; cat sorted_all_domains.txt | anew temp1.txt | httpx -sc -nc -fr --silent | notify --silent | anew latest_sorted_all_domains.httpx.txt"
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def change_in_previous_URLs():
    command = "echo 'Checking if anything changed in previous collections' | notify --silent ; cat sorted_all_domains.txt | anew temp2.txt | httpx -sc -cl -location -title -nc -fr --silent | notify --silent | anew verbose_all_domains.httpx.txt"
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
       # print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    healthcheck("attack_surface_script is healthy! -----------> prod")
    
    healthcheck("Fetching all domains and subdomains from route53")
    print("Running dump_domains_n_subdomains.main function")
    dump_domains_n_subdomains.main()

    healthcheck("Checking newly found domain with httpx")
    print("Running prob_sub_domains_slack function")
    prob_sub_domains_slack()

    healthcheck("Checking if anything changed in exisiting list")
    print("Running prob_sub_domains_slack function")
    change_in_previous_URLs()

    healthcheck("Converting into csv file.")
    print("Running convert_to_csv function")
    convertToCSV.main()
    healthcheck("attack_surface_script finished successfully on prod")