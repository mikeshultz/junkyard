""" Generate a random MAC address

Example MAC: 12:34:56:78:90:ab

Usage
-----
python random_mac.py
python random_mac.py --prefix ab:cd:ef
"""
import os
import re
import typer
from typing import Generator, Optional

app = typer.Typer()


def format_mac(hexstr: str) -> str:
    norm = hexstr.replace(":", "")
    return ":".join([norm[i : i + 2] for i in range(0, 12, 2)])


@app.command()
def main(prefix: Optional[str] = ""):
    if prefix and not re.match(
        r"([0-9a-fA-F]{2}):?([0-9a-fA-F]{2}):?([0-9a-fA-F]{2})", prefix
    ):
        raise ValueError("Invalid prefix.  Expected 3 hex bytes like 1d:ea:d0")

    randb = os.urandom(4 if prefix else 8).hex()
    mac = format_mac(prefix + randb)

    print(f"Randomized MAC: {mac}")


if __name__ == "__main__":
    app()
