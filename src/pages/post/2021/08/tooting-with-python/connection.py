import json
import os
import sys
from dataclasses import dataclass
from typing import Any, Callable, Dict, List

import rich
from rich.pretty import pprint
from mastodon import Mastodon

# I got mine stashed in a `.envrc` file
API_BASE = os.environ.get("API_BASE")
CLIENT_KEY = os.environ.get("CLIENT_KEY")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")


def stored(func: Callable) -> Dict[str, Any]:
    def inner(*args, **kwargs):
        filename = f"{func.__name__}.json"
        rich.print(f"stored.inner for {func.__name__}")

        if os.path.exists(filename):
            with open(filename, "r") as f:
                rich.print(f"Loading data from {filename}")
                data = json.load(f)
            return data

        rich.print(f"Calling {func.__name__}")
        data = func(*args, **kwargs)

        with open(filename, "w") as f:
            rich.print(f"Writing data to {filename}")
            json.dump(data, f, indent=4, default=str)

        return data

    return inner


@dataclass
class App:
    """Provides convenience methods for querying an instance and posting toots."""

    mastodon: Mastodon

    @stored
    def instance(self) -> Dict[str, Any]:
        """Return a dictionary of information about the connected instance."""

        return self.mastodon.instance()

    def instance_summary(self) -> Dict[str, Any]:
        instance = self.instance()
        fields = ["uri", "title", "short_description"]
        data = {field: instance[field] for field in fields}
        data["contact_account"] = instance["contact_account"]["display_name"]

        return data

    @stored
    def timeline_public(self) -> List[Dict[str, Any]]:
        return self.mastodon.timeline_public()

    def timeline_summary(self) -> Dict[str, Any]:
        timeline = self.timeline_public()
        return [
            {
                "date": toot["created_at"],
                "author": toot["account"]["display_name"],
                "content": toot["content"],
            }
            for toot in timeline
        ]

    def status_post(self, status: str, visibility: str = "direct") -> Dict[str, Any]:
        """Post a toot to our connection, private unless we say otherwise."""

        return self.mastodon.status_post(status, visibility=visibility)

    @classmethod
    def connect(
        cls,
        client_key: str = CLIENT_KEY,
        api_base_url: str = API_BASE,
        client_secret: str = CLIENT_SECRET,
        access_token: str = ACCESS_TOKEN,
    ) -> "App":
        """Return an App connected to a specific Mastodon instance."""

        mastodon = Mastodon(
            client_id=client_key,
            api_base_url=api_base_url,
            client_secret=client_secret,
            access_token=access_token,
        )
        return cls(mastodon=mastodon)


if __name__ == "__main__":
    _ = rich.get_console()
    rich.reconfigure(record=True, width=80)

    app = App.connect()

    if app.mastodon.instance_health():
        rich.print("Connection instance is [green]healthy[/green]")
    else:
        rich.print("Connection instance is [red][b]not[/b] healthy![/red]")
        sys.exit(1)

    pprint(app.timeline_summary(), max_string=80)
    status_text = "Ignore me, just messing with Mastodon.py"
    toot = app.status_post(status_text)
    pprint(toot)

    rich.get_console().save_html("output.html", inline_styles=True)
