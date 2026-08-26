#!/usr/bin/env python3
"""
Environment check.

Run this BEFORE the first class:

    python doctor.py        (Windows)
    python3 doctor.py       (Mac, if not in a virtual environment yet)

Every line should say PASS. If any line says FAIL, the fix is printed at the
bottom. If you cannot resolve it, email me the full output of this script --
not a screenshot, the actual text.
"""

import os
import platform
import sys
from pathlib import Path

import logging
logging.getLogger("google_genai.models").setLevel(logging.ERROR)

FAILURES = []
WARNINGS = []
HERE = Path(__file__).resolve().parent


def check(name, ok, fix):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if not ok:
        FAILURES.append((name, fix))
    return ok


def warn(name, ok, note):
    if not ok:
        print(f"  WARN  {name}")
        WARNINGS.append((name, note))
    else:
        print(f"  PASS  {name}")
    return ok


print("\n" + "=" * 62)
print("  AI Agents -- environment check")
print("=" * 62)

# ---------------------------------------------------------------- system
print("\nSystem")
print(f"  Python      {platform.python_version()}")
print(f"  Interpreter {sys.executable}")
print(f"  Platform    {platform.system()} {platform.machine()}")
print(f"  Folder      {HERE}")

# ------------------------------------------------------------- python
print("\nPython")
v = sys.version_info
check(
    "Python 3.10 or newer",
    v >= (3, 10),
    "Install Python 3.12 from python.org. On Windows, TICK 'Add Python to PATH'\n"
    "     during installation, then close and reopen your terminal.",
)

warn(
    "Python 3.12 (recommended version)",
    (v.major, v.minor) == (3, 12),
    f"You are on {platform.python_version()}. The course is tested on 3.12.\n"
    "     Newer versions sometimes lack prebuilt packages and fail to install.\n"
    "     This is only a problem if the package checks below fail.",
)

check(
    "Running inside a virtual environment",
    sys.prefix != sys.base_prefix,
    "Create and activate one:\n"
    "       Mac:      python3 -m venv .venv && source .venv/bin/activate\n"
    "       Windows:  python -m venv .venv\n"
    "                 .venv\\Scripts\\activate\n"
    "     If Windows blocks activation, run this once in PowerShell:\n"
    "       Set-ExecutionPolicy -Scope CurrentUser RemoteSigned",
)

# ------------------------------------------------------------- location
print("\nLocation")
cloud_markers = ("onedrive", "dropbox", "google drive", "icloud", "cloudstorage")
in_cloud = any(m in str(HERE).lower() for m in cloud_markers)
check(
    "Project folder is not inside a cloud-synced folder",
    not in_cloud,
    "Your project is inside OneDrive/Dropbox/iCloud. Sync interferes with\n"
    "     virtual environments and causes strange install errors.\n"
    "     Move the whole folder somewhere local (e.g. Documents or Desktop)\n"
    "     and recreate the virtual environment there.",
)

# ------------------------------------------------------------- packages
print("\nPackages")
try:
    from google import genai  # noqa: F401

    ok_genai = True
except ImportError:
    ok_genai = False
check(
    "google-genai installed",
    ok_genai,
    "pip install --upgrade pip\n"
    "     pip install google-genai python-dotenv\n"
    "     If a package fails to BUILD (mentions maturin, cargo, or Rust), try:\n"
    "       pip install 'cryptography<43'\n"
    "     then run the install again.",
)

try:
    from dotenv import load_dotenv

    ok_dotenv = True
except ImportError:
    ok_dotenv = False
check(
    "python-dotenv installed",
    ok_dotenv,
    "pip install python-dotenv",
)

# ------------------------------------------------------------- api key
print("\nAPI key")
env_path = None
if ok_dotenv:
    for folder in (HERE, *HERE.parents[:2]):
        candidate = folder / ".env"
        if candidate.exists():
            env_path = candidate
            break
    if env_path:
        load_dotenv(env_path)

check(
    ".env file found",
    env_path is not None,
    "Create a file named exactly '.env' in this folder containing one line:\n"
    "       GEMINI_API_KEY=your-key-here\n"
    "     Get a key at https://aistudio.google.com -> Get API key.\n"
    "     Create it in VS Code, NOT Notepad -- Notepad saves it as '.env.txt'.",
)

key = os.environ.get("GEMINI_API_KEY", "")
if env_path:
    check(
        "GEMINI_API_KEY is set",
        bool(key),
        f"{env_path} has no usable GEMINI_API_KEY line. It must be exactly:\n"
        "       GEMINI_API_KEY=AIza...\n"
        "     No quotes, and no spaces around the = sign.",
    )
else:
    print("  SKIP  GEMINI_API_KEY is set  (no .env file to read)")

# ------------------------------------------------------------- gitignore
print("\nSafety")
gi_text = ""
for folder in (HERE, *HERE.parents[:2]):
    gi = folder / ".gitignore"
    if gi.exists():
        gi_text += gi.read_text()
check(
    ".env is listed in .gitignore",
    ".env" in gi_text,
    "Create a .gitignore file containing these lines:\n"
    "       .env\n"
    "       .venv/\n"
    "       __pycache__/\n"
    "     Never commit your API key. Anyone who finds it can spend your quota.",
)

# ------------------------------------------------------------- live call
print("\nLive API call")
if FAILURES:
    print("  SKIP  (fix the problems above first)")
else:
    try:
        MODEL = "gemini-3.6-flash"
        try:
            from config import MODEL  # noqa: F811
        except Exception:
            pass

        from google import genai
        from google.genai import errors

        client = genai.Client()
        try:
            resp = client.models.generate_content(
                model=MODEL, contents="Reply with exactly the word: ok"
            )
            got = (resp.text or "").strip().lower()
            check(
                f"Called {MODEL} successfully",
                "ok" in got,
                f"The model replied unexpectedly: {got!r}",
            )
            u = resp.usage_metadata
            print(
                f"        tokens in={u.prompt_token_count} "
                f"total={u.total_token_count}"
            )
        except errors.ClientError as e:
            if getattr(e, "code", None) == 429 or "429" in str(e):
                print("  PASS  Your key works (hit the rate limit, which is normal)")
                print("        Free tier allows 5 requests per minute per model.")
            elif "not found" in str(e).lower():
                check(
                    f"Called {MODEL} successfully",
                    False,
                    f"The model '{MODEL}' is not available to you.\n"
                    "     Run this to see what you CAN use:\n"
                    "       python -c \"from google import genai; "
                    "c=genai.Client();\\\n"
                    "         [print(m.name) for m in c.models.list()]\"\n"
                    "     Then tell me which models you see.",
                )
            else:
                check(f"Called {MODEL} successfully", False, str(e))
    except Exception as e:
        check("Live API call", False, f"{type(e).__name__}: {e}")

# ------------------------------------------------------------- summary
print("\n" + "=" * 62)
if FAILURES:
    print(f"  {len(FAILURES)} problem(s) to fix:\n")
    for name, fix in FAILURES:
        print(f"  * {name}")
        print(f"     -> {fix}\n")
    print("  Fix these, then run this script again.")
    print("=" * 62 + "\n")
    sys.exit(1)

if WARNINGS:
    print("  Notes:\n")
    for name, note in WARNINGS:
        print(f"  * {name}")
        print(f"     -> {note}\n")

print("  All checks passed. You are ready for Week 1.")
print("=" * 62 + "\n")
