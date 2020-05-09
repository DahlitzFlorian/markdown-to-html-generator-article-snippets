import os

from datetime import datetime
from email.utils import formatdate, format_datetime  # for RFC2822 formatting
from pathlib import Path

import jinja2
import markdown

import blog

ROOT = Path(__file__).parent.parent.parent
POSTS_DIR = ROOT / "app" / "posts"
TEMPLATE_DIR = ROOT / "app" / "templates"
BLOG_TEMPLATE_FILE = TEMPLATE_DIR / "shared" / "layout.html"
INDEX_TEMPLATE_FILE = TEMPLATE_DIR / "shared" / "index.html"
BASE_URL = os.environ.get("DOMAIN", "http://0.0.0.0:5000/")


def generate_entries():
    posts = POSTS_DIR.glob("*.md")

    extensions = ["extra", "smarty", "meta"]
    loader = jinja2.FileSystemLoader(searchpath="./")
    env = jinja2.Environment(loader=loader, autoescape=True)

    all_posts = []
    for post in posts:
        print("rendering {0}".format(post))

        url = Path("posts") / f"{post.stem}"
        url_html = f"{url}.html"
        target_file = TEMPLATE_DIR / url_html

        _md = markdown.Markdown(extensions=extensions, output_format="html5")

        with open(post) as post_f:
            content = post_f.read()
            estimated_reading_time = blog.estimate_reading_time(content)
            html = _md.convert(content)
            doc = env.get_template(str(BLOG_TEMPLATE_FILE)).render(
                content=html,
                baseurl=BASE_URL,
                estimated_reading_time=estimated_reading_time,
                url=url,
                **_md.Meta,
            )

        with open(target_file, "w") as post_html_f:
            post_html_f.write(doc)

        post_date = datetime.strptime(_md.Meta["published"][0], "%B %d, %Y")
        post_dict = dict(
            **_md.Meta,
            date=post_date,
            rfc2822_date=format_datetime(post_date),
            rel_link=f"/{url}",
            link="{0}{1}".format(BASE_URL, url),
        )

        all_posts.append(post_dict)

    # Order blog posts by date published
    all_posts.sort(key=lambda item: item["date"], reverse=True)

    with open(TEMPLATE_DIR / "index.html", "w") as index_f:
        index_f.write(
            env.get_template(str(INDEX_TEMPLATE_FILE)).render(
                posts=all_posts, template_path=str(BLOG_TEMPLATE_FILE)
            )
        )


if __name__ == "__main__":
    generate_entries()
