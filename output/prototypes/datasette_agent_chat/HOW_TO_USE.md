# How to Use

## Option A: Run the offline demo (no keys needed)

```bash
cd datasette_agent_chat
bash run.sh
```

This creates a sample SQLite database and runs simulated agent-chat queries against it, showing the NL -> SQL -> results flow that datasette-agent provides in the browser.

## Option B: Run datasette-agent live in your browser

### 1. Install

```bash
pip install "datasette>=1.0a30" "datasette-agent>=0.1a4"
```

### 2. Create or use an existing database

```bash
# use the included sample
python3 create_sample_db.py

# or point at any .db file you already have
```

### 3. Launch Datasette

```bash
datasette serve demo.db
```

Open `http://127.0.0.1:8001` in your browser.

### 4. Use the agent chat

1. Press `/` to open the **Jump to** menu.
2. Below the search box you'll see **"Start a new agent chat"**.
3. Type a natural-language question (e.g. "What are the top 5 products by revenue?").
4. The agent generates SQL, runs it, and displays the answer inline.

## Using as a Claude Code Skill

### Install the skill

```bash
mkdir -p ~/.claude/skills/datasette_agent_chat
cp SKILL.md ~/.claude/skills/datasette_agent_chat/SKILL.md
```

### Trigger phrases

- "Set up datasette-agent for my Datasette instance"
- "Add an agent chat interface to Datasette"
- "I want to query my Datasette database using natural language"
- "Configure the Jump menu agent chat in Datasette"
- "Install datasette-agent and enable the chat plugin"

## First 60 seconds

```
$ bash run.sh

=== datasette-agent Chat Demo ===

Created sample database: demo.db
  - products: 15 rows
  - orders:   15 rows

----------------------------------------------------------------
  User:  How many products do we have?
  Agent: Count all products
  SQL:   SELECT count(*) AS product_count FROM products

  product_count
  -------------
  15

----------------------------------------------------------------
  User:  Show me the most expensive products
  Agent: Top 5 most expensive products
  SQL:   SELECT name, category, price FROM products ORDER BY price DESC LIMIT 5

  name                    | category    | price
  ------------------------+-------------+------
  Ergonomic Chair         | Furniture   | 649.99
  Standing Desk           | Furniture   | 499.99
  Noise-Cancel Headphones | Electronics | 199.99
  Mechanical Keyboard     | Electronics | 89.99
  Monitor Arm             | Furniture   | 79.99

... (more queries follow)
```
