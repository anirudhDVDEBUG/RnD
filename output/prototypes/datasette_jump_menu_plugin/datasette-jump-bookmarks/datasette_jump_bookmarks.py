"""Datasette plugin: adds bookmarks to the Jump to... menu."""
from datasette import hookimpl


@hookimpl
def jump_items_sql(datasette, actor, request):
    """Return SQL queries whose results appear in the Jump menu."""
    return [
        (
            "SELECT label, url, description FROM bookmarks WHERE label LIKE :q",
            "sample",
            {},
        )
    ]
