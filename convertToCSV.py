import re
import csv

def main():
    # Read information from the file
    with open("latest_sorted_all_domains.httpx.txt", "r") as file:
        lines = file.readlines()

    # Extract domain and status codes using regex
    results = []
    for line in lines:
        match = re.match(r'^(https?://\S+)\s+\[(\d+(?:,\d+)*)\](?:\s+\[(https?://\S+)\])?$', line)
        #print(match)
        if match:
            domain = match.group(1)
            status_codes = match.group(2).split(',')
            final_url = match.group(3) if match.group(3) else ""

            result_line = [domain] + status_codes
            if final_url:
                result_line.append(final_url)
            results.append(result_line)

            # Sort results based on the first status code
            results.sort(key=lambda x: int(x[1]))  # Assuming the first status code is always present

            # Write sorted results to a CSV file
            with open("latest_sorted_all_domains.httpx.txt.csv", "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow(["Domain"] + ["Status Code"] * len(status_codes) + ["Final URL"])
                csv_writer.writerows(results)

    print("Sorted output saved to latest_sorted_all_domains.httpx.txt.csv")

#latest_sorted_all_domains.httpx.txt
if __name__ == "__main__":
    main()