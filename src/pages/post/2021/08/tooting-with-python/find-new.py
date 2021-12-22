import frontmatter
import fs
import requests
import rich
from fs import open_fs
from slugify import slugify

SITE_ROOT = "~/Sites/rgb-hugo/content"
CONTENT_EXT = "*.rst.txt"

if __name__ == "__main__":
    site_fs = open_fs(SITE_ROOT)
    unannounced_content = []
    rich.print(site_fs)

    for path, info in site_fs.glob("**/*.rst.txt", exclude_dirs=["draft"]):
        dirname = fs.path.dirname(path)

        if "social.yaml" in site_fs.listdir(dirname):
            continue

        unannounced_content.append(path)

    rich.print(unannounced_content)
    unannounced_sorted = sorted(unannounced_content)
    likeliest = unannounced_sorted[-1]
    rich.print(likeliest)

    with site_fs.open(likeliest) as f:
        meta, _ = frontmatter.parse(f.read())

    rich.print(meta)
    path_parts = fs.path.parts(likeliest)
    rich.print(path_parts)
    slug = fs.path.dirname(likeliest)
    section = path_parts[1]
    rich.print(section, slug)

    if "description" in meta:
        preface = meta["description"]
    elif "summary" in meta:
        preface = meta["summary"]
    else:
        preface = f"I wrote a {section}"

    if "title" in meta:
        title = meta["title"]
    else:
        rich.print("NO TITLE?")
        title = ""

    tag_list = []
    for tag in meta["tags"]:
        posse_tag = "".join([tag_term.title() for tag_term in slugify(tag).split("-")])
        tag_list.append(posse_tag)

    tags = " ".join([f"#{tag}" for tag in tag_list])

    toot = f"""{preface}

{title}

{tags} #Blog
"""

    rich.print(toot)
    post_url = f"https://randomgeekery.org{slug}"
    rich.print(post_url)
    r = requests.head(post_url)

    if r.status_code == 200:
        rich.print("Ready to go!")
