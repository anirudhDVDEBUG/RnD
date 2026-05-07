"""Sample diffs for demonstrating the vibe-vs-agentic code review tool."""

SAMPLES = [
    {
        "name": "Vibe-coded auth endpoint",
        "description": "AI-generated login route added in one shot, no tests, over-engineered error handling",
        "context": "production",
        "diff": """\
diff --git a/app/routes/auth.py b/app/routes/auth.py
new file mode 100644
--- /dev/null
+++ b/app/routes/auth.py
@@ -0,0 +1,62 @@
+import json
+import hashlib
+import os
+from flask import Blueprint, request, jsonify
+from app.models import db, User
+from app.utils import generate_token, send_welcome_email
+from app.helpers import validate_email_format, sanitize_input
+from app.middleware import rate_limiter
+
+auth_bp = Blueprint('auth', __name__)
+
+@auth_bp.route('/login', methods=['POST'])
+def login():
+    \"\"\"Handle user login with comprehensive error handling and validation.\"\"\"
+    try:
+        try:
+            data = request.get_json()
+        except Exception as e:
+            return jsonify({'error': 'Invalid JSON payload', 'details': str(e)}), 400
+
+        if not data:
+            return jsonify({'error': 'No data provided'}), 400
+
+        email = data.get('email', '').strip()
+        password = data.get('password', '').strip()
+
+        # Validate email format
+        if not validate_email_format(email):
+            return jsonify({'error': 'Invalid email format'}), 400
+
+        # Sanitize inputs
+        email = sanitize_input(email)
+        password = sanitize_input(password)
+
+        # Hash password for comparison
+        password_hash = hashlib.md5(password.encode()).hexdigest()
+
+        user = User.query.filter_by(email=email, password_hash=password_hash).first()
+
+        if not user:
+            return jsonify({'error': 'Invalid credentials'}), 401
+
+        # Generate authentication token
+        token = generate_token(user.id)
+
+        # Update last login timestamp
+        user.last_login = db.func.now()
+        db.session.commit()
+
+        return jsonify({
+            'token': token,
+            'user': {
+                'id': user.id,
+                'email': user.email,
+                'name': user.name,
+                'role': user.role,
+                'created_at': str(user.created_at),
+                'updated_at': str(user.updated_at),
+                'last_login': str(user.last_login),
+                'preferences': json.loads(user.preferences) if user.preferences else {}
+            }
+        }), 200
+    except Exception as e:
+        # Log the error for debugging
+        print(f"Login error: {str(e)}")
+        return jsonify({'error': 'Internal server error', 'debug': str(e)}), 500
""",
    },
    {
        "name": "Well-reviewed utility function",
        "description": "Small, focused change with tests, consistent with codebase style",
        "context": "production",
        "diff": """\
diff --git a/lib/formatting.py b/lib/formatting.py
--- a/lib/formatting.py
+++ b/lib/formatting.py
@@ -12,6 +12,15 @@ def truncate(text: str, max_len: int = 80) -> str:
     return text[:max_len - 3] + "..."


+def slugify(text: str) -> str:
+    text = text.lower().strip()
+    text = re.sub(r'[^\\w\\s-]', '', text)
+    return re.sub(r'[\\s_]+', '-', text).strip('-')
+
+
 def capitalize_words(text: str) -> str:
     return ' '.join(w.capitalize() for w in text.split())

diff --git a/tests/test_formatting.py b/tests/test_formatting.py
--- a/tests/test_formatting.py
+++ b/tests/test_formatting.py
@@ -1,5 +1,5 @@
 import pytest
-from lib.formatting import truncate, capitalize_words
+from lib.formatting import truncate, capitalize_words, slugify


@@ -18,3 +18,16 @@ def test_capitalize_words():
     assert capitalize_words("hello world") == "Hello World"
     assert capitalize_words("already Fine") == "Already Fine"
     assert capitalize_words("") == ""
+
+
+class TestSlugify:
+    def test_basic(self):
+        assert slugify("Hello World") == "hello-world"
+
+    def test_special_chars(self):
+        assert slugify("Hello, World!") == "hello-world"
+
+    def test_underscores_and_spaces(self):
+        assert slugify("my_cool  post") == "my-cool-post"
+
+    def test_empty(self):
+        assert slugify("") == ""
""",
    },
    {
        "name": "Scope-creep refactor",
        "description": "Asked to fix a typo, AI refactored the whole file and added type hints",
        "context": "production",
        "diff": """\
diff --git a/config/settings.py b/config/settings.py
--- a/config/settings.py
+++ b/config/settings.py
@@ -1,18 +1,32 @@
-# App settings
-DEBUG = True
-SECRET_KEY = "changeme"
-DB_URL = "sqlite:///app.db"
-MAX_UPLOAD = 16 * 1024 * 1024  # 16MB
-ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
-# Cahce timeout in seconds
-CACHE_TIMEOUT = 300
+\"\"\"Application configuration settings.
+
+This module contains all configuration constants for the application.
+All values can be overridden via environment variables.
+\"\"\"
+
+import os
+from typing import Final, List
+
+# Application settings
+DEBUG: Final[bool] = os.getenv("DEBUG", "true").lower() == "true"
+SECRET_KEY: Final[str] = os.getenv("SECRET_KEY", "changeme")
+DB_URL: Final[str] = os.getenv("DB_URL", "sqlite:///app.db")
+MAX_UPLOAD: Final[int] = int(os.getenv("MAX_UPLOAD", str(16 * 1024 * 1024)))
+ALLOWED_HOSTS: Final[List[str]] = os.getenv(
+    "ALLOWED_HOSTS", "localhost,127.0.0.1"
+).split(",")
+
+# Cache timeout in seconds
+CACHE_TIMEOUT: Final[int] = int(os.getenv("CACHE_TIMEOUT", "300"))
+
+# Logging configuration
+LOG_LEVEL: Final[str] = os.getenv("LOG_LEVEL", "INFO")
+LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
""",
    },
    {
        "name": "Quick prototype script",
        "description": "Throwaway data exploration script, vibe coding is fine here",
        "context": "throwaway",
        "diff": """\
diff --git a/scripts/explore_data.py b/scripts/explore_data.py
new file mode 100644
--- /dev/null
+++ b/scripts/explore_data.py
@@ -0,0 +1,25 @@
+import pandas as pd
+import matplotlib.pyplot as plt
+
+df = pd.read_csv("data/sales_2026.csv")
+print(df.head())
+print(df.describe())
+
+# Plot monthly revenue
+df['date'] = pd.to_datetime(df['date'])
+monthly = df.groupby(df['date'].dt.to_period('M'))['revenue'].sum()
+monthly.plot(kind='bar')
+plt.title("Monthly Revenue 2026")
+plt.tight_layout()
+plt.savefig("output/revenue_chart.png")
+print("saved chart")
+
+# Top products
+top = df.groupby('product')['revenue'].sum().nlargest(10)
+print("Top 10 products:")
+print(top)
+
+# Quick correlation check
+print("Correlation matrix:")
+print(df[['revenue', 'units', 'price']].corr())
""",
    },
]
