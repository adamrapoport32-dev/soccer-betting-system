
import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API_URL = "https://api.football-data.org/v4/competitions/PL/matches"


def main():
    token = os.environ.get("FOOTBALL_DATA_TOKEN")

    if not token:
        raise SystemExit(
            "Missing FOOTBALL_DATA_TOKEN GitHub Actions secret"
        )

    request = urllib.request.Request(
        API_URL,
        headers={
            "X-Auth-Token": token,
            "Accept": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(
            request, timeout=30
        ) as response:
            data = json.load(response)
    except urllib.error.HTTPError as error:
        raise SystemExit(
            f"Football API returned HTTP {error.code}"
        ) from None

    matches = data.get("matches")

    if not isinstance(matches, list):
        raise SystemExit("Invalid Premier League API response")

    output = {
        "competition": "Premier League",
        "source": "football-data.org",
        "retrieved_at_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "match_count": len(matches),
        "matches": matches,
        "research_only": True,
    }

    destination = Path("artifacts/epl/latest.json")
    destination.parent.mkdir(
        parents=True, exist_ok=True
    )

    destination.write_text(
        json.dumps(output, indent=2),
        encoding="utf-8",
    )

    print(
        f"Successfully retrieved {len(matches)} EPL matches"
    )


if __name__ == "__main__":
    main()
