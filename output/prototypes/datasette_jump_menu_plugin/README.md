# Datasette Jump Menu Plugin

Build custom Datasette plugins that add searchable items to the "Jump to..." quick-navigation menu (press `/` anywhere in the UI). This prototype demonstrates a working plugin using the new `jump_items_sql()` hook from Datasette 1.0a30.

**Headline result:** Type `/` in Datasette, start typing, and instantly navigate to any custom item your plugin registers -- tables, saved queries, bookmarks, anything with a label and URL.

- [HOW_TO_USE.md](HOW_TO_USE.md) -- install, configure, first 60 seconds
- [TECH_DETAILS.md](TECH_DETAILS.md) -- architecture, limitations, relevance
