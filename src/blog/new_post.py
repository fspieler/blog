from datetime import date
import sys

def main():
    title = sys.argv[-1]
    title_url = title.replace(" ", "-").replace("_", "-").replace("'", "").lower()
    with open(f"content/{title_url}.md", "w", encoding="utf-8") as f:
        f.write("type:blog\n")
        f.write(f"title:{title}\n")
        f.write("subtitle:\n")
        f.write("description:\n")
        f.write(f"date:{date.today()}\n")
        f.write("order:0\n")
        f.write("tags:\n")
