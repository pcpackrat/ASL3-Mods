#!/usr/bin/python3

import requests
import subprocess
import argparse
import time
import sys

def load_list(file_path):
    """Loads a list of node IDs from a text file."""
    try:
        with open(file_path, 'r') as file:
            # Read each line, strip any surrounding whitespace, and add to the set
            return {line.strip() for line in file}
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return set()

def fetch_data(url):
    """Fetches data from the given URL and returns the JSON response."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data from {url}, Status Code: {response.status_code}")
        return None

def run_command(node_id):
    """Runs the system command with the given node ID."""
    command = f"asterisk -rx 'rpt fun {args.initial_node_id} *1{node_id}'"
    if not args.quiet:
        print(f"Running command: {command}")
    subprocess.run(command, shell=True)

def main():
    global args
    parser = argparse.ArgumentParser(description='Fetch and process node data.')
    parser.add_argument('initial_node_id', type=str, help='Initial Node ID to fetch data for')
    parser.add_argument('--quiet', action='store_true', help='Suppress output')
    parser.add_argument('--whitelist', type=str, help='Path to the whitelist file')
    parser.add_argument('--ignorelist', type=str, help='Path to the ignore list file')
    parser.add_argument('--loop', type=int, help='Loop the script with the specified interval in seconds.')
    args = parser.parse_args()

    # Enforce minimum loop interval of 10 seconds
    if args.loop and args.loop < 10:
        print("Error: Loop interval must be at least 10 seconds.")
        sys.exit(1)

    # Load the whitelist and ignore list from the file if provided, otherwise default to an empty set
    whitelisted_nodes = load_list(args.whitelist) if args.whitelist else set()
    ignored_nodes = load_list(args.ignorelist) if args.ignorelist else set()

    base_url = "https://stats.allstarlink.org/api/stats/"
    initial_url = base_url + args.initial_node_id

    while True:
        # Fetch data for the initial node
        if args.initial_node_id in ignored_nodes:
            if not args.quiet:
                print(f"Initial node {args.initial_node_id} is in the ignore list, skipping.")
            break

        initial_data = fetch_data(initial_url)

        if initial_data:
            # Extract links
            links = initial_data.get('stats', {}).get('data', {}).get('links', [])

            if links:
                if not args.quiet:
                    print(f"Node IDs connected to {args.initial_node_id}: {links}")

                # Flag to track if command has been run
                command_run = False

                # Fetch and process data for each linked node
                for node_id in links:
                    # Skip nodes in the ignore list
                    if str(node_id) in ignored_nodes:
                        if not args.quiet:
                            print(f"Node {node_id} is in the ignore list, skipping.")
                        continue

                    node_url = base_url + str(node_id)
                    node_data = fetch_data(node_url)

                    if node_data:
                        if not args.quiet:
                            print(f"\nData for Node ID {node_id}:")
                        # Extract and print links for the current node
                        links_for_current = node_data.get('stats', {}).get('data', {}).get('links', [])

                        if links_for_current:
                            if not args.quiet:
                                print(f"Linked Nodes for Node ID {node_id}")
                            for linked_node_id in links_for_current:
                                if not args.quiet:
                                    print(f"  Node ID: {linked_node_id}")
                                # Run the command if linked_node_id is not the initial node ID and not in the whitelist
                                if linked_node_id != args.initial_node_id and linked_node_id not in whitelisted_nodes:
                                    if not command_run:
                                        run_command(node_id)
                                        command_run = True
                        else:
                            if not args.quiet:
                                print(f"No linked nodes found for Node ID {node_id}")
                    else:
                        if not args.quiet:
                            print(f"Failed to retrieve data for Node ID {node_id}")
            else:
                if not args.quiet:
                    print("No links found for the initial node.")
        else:
            if not args.quiet:
                print("Failed to retrieve data for the initial node.")

        if args.loop:
            time.sleep(args.loop)
        else:
            break

if __name__ == "__main__":
    main()
