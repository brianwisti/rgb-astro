import json
import os
import time

import requests


def rebuild_full_feed(domain: str, token: str, target_file: str) -> None:
    endpoint = "https://webmention.io/api/mentions.jf2"
    page_size = 100
    all_entries = []
    page_index = 0

    while True:
        params = {
            "domain": domain,
            "token": token,
            "page": page_index,
            "per-page": page_size,
            "sort-dir": "up",
        }
        r = requests.get(endpoint, params=params)
        this_page = r.json()
        entries = this_page["children"]
        all_entries += entries
        page_index += 1

        entry_count = len(entries)
        print(f"Added {entry_count} entries")

        # Be a polite Internet citizen
        time.sleep(1)

        # Stop when we're done
        if entry_count < page_size:
            print("Reached end of feed")
            break

    with open(target_file, "w") as f:
        json.dump(all_entries, f, indent=4)
        print(f"Wrote {len(all_entries)} entries to {target_file}")


if __name__ == "__main__":
    domain = "randomgeekery.org"
    token = os.environ["WEBMENTION_KEY"]
    target_file = "mentions.jf2"
    rebuild_full_feed(domain, token, target_file)
