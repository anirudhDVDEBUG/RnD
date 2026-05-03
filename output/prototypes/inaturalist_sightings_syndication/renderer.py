"""Render sightings to HTML pages and Atom feed."""

import os
from jinja2 import Environment, BaseLoader

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Wildlife Sightings</title>
  <link rel="alternate" type="application/atom+xml" href="feed.xml" title="Sightings Feed">
  <style>
    body { font-family: system-ui, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }
    .sighting { border-bottom: 1px solid #eee; padding: 1.5rem 0; }
    .sighting h2 { font-size: 1.2rem; margin: 0 0 0.5rem; }
    .sighting-photos { display: flex; gap: 0.5rem; flex-wrap: wrap; }
    .sighting-photos figure { margin: 0; }
    .sighting-photos img { width: 150px; height: 150px; object-fit: cover; border-radius: 4px; }
    figcaption { font-size: 0.8rem; color: #666; text-align: center; }
    .meta { font-size: 0.85rem; color: #555; margin-top: 0.5rem; }
    .pagination { margin-top: 2rem; display: flex; gap: 1rem; }
    a { color: #2563eb; }
  </style>
</head>
<body>
  <h1>Wildlife Sightings</h1>
  <p>{{ total_sightings }} sightings, {{ total_species }} species observed.</p>
  {% for s in sightings %}
  <article class="sighting">
    <h2>{{ s.species | join(", ") }}</h2>
    <div class="sighting-photos">
      {% for photo in s.photos %}
      <figure>
        <img src="{{ photo.url }}" alt="{{ photo.label }}" loading="lazy">
        <figcaption>{{ photo.label }}</figcaption>
      </figure>
      {% endfor %}
    </div>
    <p class="meta">
      <time datetime="{{ s.date }}">{{ s.date }}</time> &mdash; {{ s.place }}
      {% for url in s.source_urls %}<a href="{{ url }}">[iNat]</a> {% endfor %}
    </p>
  </article>
  {% endfor %}
  <div class="pagination">
    {% if pages %}
    Pages: {% for p in pages %}<a href="page{{ p }}.html">{{ p }}</a> {% endfor %}
    {% endif %}
  </div>
</body>
</html>
"""

PAGE_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Sightings - Page {{ page_num }}</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 800px; margin: 2rem auto; padding: 0 1rem; }
    .sighting { border-bottom: 1px solid #eee; padding: 1.5rem 0; }
    .sighting h2 { font-size: 1.2rem; margin: 0 0 0.5rem; }
    .sighting-photos { display: flex; gap: 0.5rem; flex-wrap: wrap; }
    .sighting-photos figure { margin: 0; }
    .sighting-photos img { width: 150px; height: 150px; object-fit: cover; border-radius: 4px; }
    figcaption { font-size: 0.8rem; color: #666; text-align: center; }
    .meta { font-size: 0.85rem; color: #555; margin-top: 0.5rem; }
    .pagination { margin-top: 2rem; display: flex; gap: 1rem; }
    a { color: #2563eb; }
  </style>
</head>
<body>
  <h1>Sightings - Page {{ page_num }}</h1>
  <p><a href="index.html">&larr; Back to all sightings</a></p>
  {% for s in sightings %}
  <article class="sighting">
    <h2>{{ s.species | join(", ") }}</h2>
    <div class="sighting-photos">
      {% for photo in s.photos %}
      <figure>
        <img src="{{ photo.url }}" alt="{{ photo.label }}" loading="lazy">
        <figcaption>{{ photo.label }}</figcaption>
      </figure>
      {% endfor %}
    </div>
    <p class="meta">
      <time datetime="{{ s.date }}">{{ s.date }}</time> &mdash; {{ s.place }}
      {% for url in s.source_urls %}<a href="{{ url }}">[iNat]</a> {% endfor %}
    </p>
  </article>
  {% endfor %}
  <div class="pagination">
    {% if prev_page %}<a href="page{{ prev_page }}.html">&larr; Previous</a>{% endif %}
    {% if next_page %}<a href="page{{ next_page }}.html">Next &rarr;</a>{% endif %}
  </div>
</body>
</html>
"""

ATOM_TEMPLATE = """\
<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>Wildlife Sightings</title>
  <link href="feed.xml" rel="self"/>
  <updated>{{ updated }}</updated>
  <id>urn:sightings:feed</id>
  {% for s in sightings %}
  <entry>
    <title>{{ s.species | join(", ") }}</title>
    <id>urn:sighting:{{ s.date }}:{{ loop.index }}</id>
    <updated>{{ s.time_start or s.date }}T00:00:00Z</updated>
    <content type="html"><![CDATA[
      <p>{{ s.place }}</p>
      {% for photo in s.photos %}<img src="{{ photo.url }}" alt="{{ photo.label }}"/>{% endfor %}
    ]]></content>
    {% for url in s.source_urls %}<link href="{{ url }}"/>{% endfor %}
  </entry>
  {% endfor %}
</feed>
"""


def render_all(sightings, output_dir="output", per_page=3):
    """Render sightings to HTML index, paginated pages, and Atom feed."""
    os.makedirs(output_dir, exist_ok=True)
    env = Environment(loader=BaseLoader())

    total_species = len(set(sp for s in sightings for sp in s["species"]))

    # Index page (shows all)
    tpl = env.from_string(INDEX_TEMPLATE)
    num_pages = (len(sightings) + per_page - 1) // per_page
    pages = list(range(1, num_pages + 1))
    html = tpl.render(sightings=sightings, total_sightings=len(sightings), total_species=total_species, pages=pages)
    with open(os.path.join(output_dir, "index.html"), "w") as f:
        f.write(html)
    print(f"Generating {output_dir}/index.html ...")

    # Paginated pages
    page_tpl = env.from_string(PAGE_TEMPLATE)
    for i in range(num_pages):
        page_sightings = sightings[i * per_page:(i + 1) * per_page]
        html = page_tpl.render(
            sightings=page_sightings,
            page_num=i + 1,
            prev_page=i if i > 0 else None,
            next_page=i + 2 if i + 1 < num_pages else None,
        )
        filename = f"page{i + 1}.html"
        with open(os.path.join(output_dir, filename), "w") as f:
            f.write(html)
        print(f"Generating {output_dir}/{filename} (sightings {i * per_page + 1}-{min((i + 1) * per_page, len(sightings))})...")

    # Atom feed
    atom_tpl = env.from_string(ATOM_TEMPLATE)
    updated = sightings[0]["time_start"] if sightings else "2026-01-01T00:00:00Z"
    if not updated or "T" not in updated:
        updated = (sightings[0]["date"] if sightings else "2026-01-01") + "T00:00:00Z"
    xml = atom_tpl.render(sightings=sightings, updated=updated)
    with open(os.path.join(output_dir, "feed.xml"), "w") as f:
        f.write(xml)
    print(f"Generating {output_dir}/feed.xml (Atom feed)...")

    return {"pages": num_pages, "total_species": total_species}
