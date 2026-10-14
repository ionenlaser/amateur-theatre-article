#!/usr/bin/env python3
"""Upload the .wiki files in a folder to the Amateur Theatre Wiki.

The page title is the file name without `.wiki`, with underscores as spaces
(`Kellertheater_Hamburg.wiki` -> "Kellertheater Hamburg"). Existing pages are
skipped unless --overwrite is given.

Usage:
    python3 upload_articles.py [--overwrite] [--summary TEXT] [FOLDER]   # default: articles

Logs in with a normal wiki account (no bot password). The username and password
are read from WIKI_USER / WIKI_PASSWORD, or asked for interactively.
"""

import argparse
import getpass
import http.cookiejar
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://amateur-theatre-wiki.gwi.uni-muenchen.de/api.php"
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar())
)
opener.addheaders = [("User-Agent", "amateur-theatre-article-uploader/1.0")]


def api(post=False, **params):
    params["format"] = "json"
    data = urllib.parse.urlencode(params).encode()
    if post:
        resp = opener.open(API, data)
    else:
        resp = opener.open(API + "?" + data.decode())
    return json.load(resp)


def token(kind):
    return api(action="query", meta="tokens", type=kind)["query"]["tokens"][
        kind + "token"
    ]


def login(user, password):
    r = api(
        post=True,
        action="clientlogin",
        username=user,
        password=password,
        loginreturnurl="https://amateur-theatre-wiki.gwi.uni-muenchen.de/",
        logintoken=token("login"),
    )
    status = r.get("clientlogin", {}).get("status")
    if status != "PASS":
        sys.exit(f"Login failed: {r.get('clientlogin', r)}")


def main():
    parser = argparse.ArgumentParser(
        description="Upload .wiki files to the Amateur Theatre Wiki."
    )
    parser.add_argument("folder", nargs="?", default="articles")
    parser.add_argument(
        "--overwrite", action="store_true", help="replace pages that already exist"
    )
    parser.add_argument("--summary", default="Create article (AI-generated draft)")
    args = parser.parse_args()

    files = sorted(Path(args.folder).glob("*.wiki"))
    if not files:
        sys.exit(f"No .wiki files in {args.folder}")

    user = os.environ.get("WIKI_USER") or input("Wiki username: ")
    password = os.environ.get("WIKI_PASSWORD") or getpass.getpass("Wiki password: ")
    login(user, password)
    csrf = token("csrf")

    for f in files:
        title = f.stem.replace("_", " ")
        params = {
            "action": "edit",
            "title": title,
            "text": f.read_text(encoding="utf-8"),
            "summary": args.summary,
            "token": csrf,
        }
        if not args.overwrite:
            params["createonly"] = 1
        r = api(post=True, **params)
        if "error" in r:
            print(f"SKIP  {title}: {r['error'].get('code')} - {r['error'].get('info')}")
        else:
            print(f"OK    {title} ({r['edit'].get('result')})")


if __name__ == "__main__":
    main()
