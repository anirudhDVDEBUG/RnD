---
name: datasette_jump_menu_plugin
description: |
  Build custom Datasette plugin hooks using the jump_items_sql() API to add searchable items to Datasette's "Jump to..." menu.
  TRIGGER: when user wants to create a Datasette plugin, customize the Jump to menu, add searchable navigation items to Datasette, or extend Datasette 1.0a30+ with jump_items_sql.
---

# Datasette Jump Menu Plugin Development

Create plugins that extend Datasette's "Jump to..." quick-navigation menu (activated with `/` key) by registering custom searchable items via the `jump_items_sql()` plugin hook.

## When to use

- "Add custom items to Datasette's Jump to menu"
- "Create a Datasette plugin with jump_items_sql"
- "Make my Datasette tables searchable from the Jump menu"
- "Extend Datasette navigation with a plugin hook"
- "Build a Datasette plugin for quick search/navigation"

## How to use

1. **Create the plugin structure:**
   ```
   datasette-my-jump-items/
   +-- pyproject.toml
   +-- datasette_my_jump_items.py
   ```

2. **Implement the `jump_items_sql()` hook** in your plugin module:
   ```python
   from datasette import hookimpl

   @hookimpl
   def jump_items_sql(datasette, actor, request):
       # Return a list of (sql, database, params) tuples
       # Each SQL query should return rows with: label, url, description (optional)
       return [
           (
               "SELECT label, url, description FROM my_custom_items WHERE label LIKE :q",
               "my_database",
               {},
           )
       ]
   ```

3. **SQL query requirements:**
   - Must return columns: `label` (displayed text), `url` (navigation target)
   - Optional column: `description` (shown below label)
   - Use `:q` parameter for the user's search query (will be `%search_term%`)

4. **Register as a Datasette plugin** in `pyproject.toml`:
   ```toml
   [project]
   name = "datasette-my-jump-items"
   version = "0.1.0"
   [project.entry-points.datasette]
   my_jump_items = "datasette_my_jump_items"
   ```

5. **Install and test:**
   ```bash
   cd datasette-my-jump-items
   pip install -e .
   datasette serve mydata.db
   # Press / on any page to open the Jump to menu
   ```

## Key details

- The Jump to menu is triggered by pressing `/` anywhere in the Datasette UI
- Items from all registered plugins are merged and filtered as the user types
- The hook receives `datasette`, `actor`, and `request` for context-aware results
- Available in Datasette 1.0a30+

## References

- Release announcement: https://simonwillison.net/2026/May/24/datasette/#atom-everything
- Plugin hook docs: https://docs.datasette.io/en/latest/plugin_hooks.html#jump-items-sql-datasette-actor-request
- Live demo: https://latest.datasette.io/
