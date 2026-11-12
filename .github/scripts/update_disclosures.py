#!/usr/bin/env python3
"""Render the disclosures block of README.md from 0w30.uk (the single source of truth).

Fetches /disclosures.json and /stats.json, rebuilds only the text between
<!-- DISCLOSURES:START --> and <!-- DISCLOSURES:END -->, and prints a diff.
Any fetch or validation error exits non-zero before README.md is touched.

Usage: update_disclosures.py [--base https://0w30.uk] [--readme README.md] [--self-test]
"""
import argparse
import difflib
import json
import sys
import urllib.parse
import urllib.request

START = "<!-- DISCLOSURES:START -->"
END = "<!-- DISCLOSURES:END -->"
SEVERITY_COLOURS = {"critical": "red", "high": "orange", "medium": "yellow", "low": "lightgrey"}
STATUS_COLOURS = {"fixed": "brightgreen", "published": "blue", "pending": "lightgrey"}
FOCUS_BADGE = "![Focus](https://img.shields.io/badge/focus-self--hosted_web_apps-informational?style=flat-square)"
FOOTER = (
    "<sub>More reports are in coordinated disclosure right now. They show up here once a fix is out. "
    "Thanks to every maintainer who took the time to look into a report and ship a fix. 💚</sub>\n\n"
    "🏡 More on how I work and what I hold to: **[0w30.uk/research ↗](https://0w30.uk/research)**"
)


def fetch_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": "nik-kl-readme-updater"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def md(text):
    """Escape text for a markdown table cell."""
    text = " ".join(str(text).split())
    for char in "\\`*_[]<>|":
        text = text.replace(char, "\\" + char)
    return text


def badge_text(text):
    """shields.io static badge text: '-' -> '--', '_' -> '__', space -> '_', rest URL-encoded."""
    text = " ".join(str(text).split()).replace("-", "--").replace("_", "__").replace(" ", "_")
    return urllib.parse.quote(text, safe="_-.")


def https(url, field):
    url = str(url or "")
    if not url.startswith("https://") or any(c in url for c in " ()<>\"'"):
        raise ValueError(f"{field}: only plain https:// links are allowed, got {url!r}")
    return url


def tone(value, colours, field):
    word = str(value).strip().split()[0].lower() if str(value).strip() else ""
    if word not in colours:
        raise ValueError(f"{field}: unknown value {value!r} (expected one of {sorted(colours)})")
    return word, colours[word]


def render(rows, stats):
    if not isinstance(rows, list) or not rows:
        raise ValueError("disclosures.json: expected a non-empty list")
    if not isinstance(stats.get("reported"), int):
        raise ValueError("stats.json: 'reported' must be an integer")
    lines = [
        f"![Reported](https://img.shields.io/badge/{badge_text('coordinated disclosures')}-{stats['reported']}-blueviolet?style=flat-square)",
        f"![Public](https://img.shields.io/badge/{badge_text('public / fixed')}-{len(rows)}-brightgreen?style=flat-square)",
        FOCUS_BADGE,
        "",
        "| Project | Vulnerability | Severity | Status | Reference |",
        "| :-- | :-- | :-: | :-: | :-- |",
    ]
    for i, row in enumerate(rows, 1):
        where = f"disclosures.json row {i}"
        for key in ("project", "repo", "issue", "cwe", "severity", "status", "link"):
            if not str(row.get(key, "")).strip():
                raise ValueError(f"{where}: missing '{key}'")
        _, sev_colour = tone(row["severity"], SEVERITY_COLOURS, f"{where} severity")
        status_word, status_colour = tone(row["status"], STATUS_COLOURS, f"{where} status")
        label = row.get("link_label") or "Advisory"
        lines.append(
            "| "
            + " | ".join([
                f"[{md(row['project'])}]({https(row['repo'], where + ' repo')})",
                f"{md(row['issue'])} <sub>{md(row['cwe'])}</sub>",
                f"![{md(row['severity'])}](https://img.shields.io/badge/{badge_text(row['severity'])}-{sev_colour}?style=flat-square)",
                f"![{status_word}](https://img.shields.io/badge/{badge_text(row['status'])}-{status_colour}?style=flat-square)",
                f"[{md(label)} ↗]({https(row['link'], where + ' link')})",
            ])
            + " |"
        )
    return "\n".join(lines) + "\n\n" + FOOTER


def replace_block(readme, block):
    if readme.count(START) != 1 or readme.count(END) != 1 or readme.index(START) > readme.index(END):
        raise ValueError("README.md: expected exactly one START marker followed by one END marker")
    head, rest = readme.split(START)
    _, tail = rest.split(END)
    return f"{head}{START}\n{block}\n{END}{tail}"


def self_test():
    assert badge_text("High 7.8") == "High_7.8"
    assert badge_text("self-hosted web_apps") == "self--hosted_web__apps"
    assert badge_text("public / fixed") == "public_%2F_fixed"
    assert md("a|b [x]") == "a\\|b \\[x\\]"
    for bad in ("javascript:alert(1)", "http://x", "https://x/(y)"):
        try:
            https(bad, "t")
        except ValueError:
            pass
        else:
            raise AssertionError(bad)
    row = {"project": "P", "repo": "https://r", "issue": "i", "cwe": "CWE-1", "severity": "Low", "status": "pending", "link": "https://l"}
    assert "lightgrey" in render([row], {"reported": 1})
    for broken in ([], [dict(row, severity="Spicy")], [dict(row, link="")]):
        try:
            render(broken, {"reported": 1})
        except ValueError:
            pass
        else:
            raise AssertionError(broken)
    doc = f"a\n{START}\nold\n{END}\nb"
    assert replace_block(doc, "new") == f"a\n{START}\nnew\n{END}\nb"
    print("self-test ok")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base", default="https://0w30.uk", help="site to read the JSON files from")
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()

    base = args.base.rstrip("/")
    rows = fetch_json(f"{base}/disclosures.json")
    stats = fetch_json(f"{base}/stats.json")
    block = render(rows, stats)

    with open(args.readme, encoding="utf-8") as handle:
        old = handle.read()
    new = replace_block(old, block)
    if new == old:
        print("README.md is up to date.")
        return
    diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(), "README.md", "README.md (new)", lineterm=""))
    print("\n".join(diff))
    print(f"\n{sum(l.startswith('+') and not l.startswith('+++') for l in diff)} lines added, "
          f"{sum(l.startswith('-') and not l.startswith('---') for l in diff)} removed.")
    with open(args.readme, "w", encoding="utf-8") as handle:
        handle.write(new)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:  # fail loudly, README untouched
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
