#!/usr/bin/env python3

import json
import sys
import re
import os

def main():
    # make sure a file is passed, or fail
    if len(sys.argv) < 2:
        print("Error: include file you want to parse. python parse_nginx.py <file>")
        sys.exit(1)

    # take in log_file
    log_file = sys.argv[1]

    # basic error handling
    if not os.path.isfile(log_file):
        print(f"Error: {log_file} doesn't exist or is not a valid file path.")
        sys.exit(1)

    path_counts = {}       # path count dict
    total_bytes = 0        # total bytes
    success_count = 0      # 100–399
    client_error_count = 0 # 400–499
    server_error_count = 0 # 500–599

    # "request": "GET /downloads/product_1 HTTP/1.1"
    # find word(GET), then space, then capture everything until space and HTTP
    path_regex = re.compile(r'^\w+\s+([^ ]+)\s+HTTP')

    # get + parse each line
    with open(log_file, 'r') as f:
        for line in f:
            line = line.strip()

            # parse JSON
            data = json.loads(line)

            # count status code
            status = data["response"]
            if 100 <= status < 400:
                success_count += 1
            elif 400 <= status < 500:
                client_error_count += 1
            elif 500 <= status < 600:
                server_error_count += 1

            # add bytes
            total_bytes += data["bytes"]

            # path and count how many times it was requested
            match = path_regex.match(data["request"])
            if match:
                # get regex match
                path = match.group(1)
                # set to 0 if not seen before
                path_counts[path] = path_counts.get(path, 0) + 1

    # convert bytes to gigabytes
    total_gb = total_bytes / 1_000_000_000

    # summary
    print("Results:")
    print(f"  Success: {success_count}")
    print(f"  Client Error: {client_error_count}")
    print(f"  Server Error: {server_error_count}\n")

    # rounded to 2 decimal points because it's clean, can change to more. ex:(.5f)
    print(f"  Total Data Transferred (GB): {total_gb:.2f}\n")

    # print each path, count pair from the dict
    print(f"  Unique Path Requests:")
    for path, count in path_counts.items():
        print(f"  {path}: {count}")

if __name__ == "__main__":
    main()
