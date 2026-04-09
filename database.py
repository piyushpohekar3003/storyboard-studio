import sqlite3
import os
from config import DB_PATH


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_slug TEXT NOT NULL,
            topic TEXT NOT NULL,
            research_input TEXT,
            research_images TEXT,
            source_url TEXT,
            generated_script TEXT,
            edited_script TEXT,
            generated_storyboard TEXT,
            status TEXT DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Add column if upgrading from old schema
    try:
        conn.execute("ALTER TABLE projects ADD COLUMN research_images TEXT")
    except Exception:
        pass
    conn.commit()
    conn.close()


def save_project(channel_slug, topic, research_input, source_url=None, research_images=None):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO projects (channel_slug, topic, research_input, source_url, research_images) VALUES (?, ?, ?, ?, ?)",
        (channel_slug, topic, research_input, source_url, research_images),
    )
    conn.commit()
    project_id = cur.lastrowid
    conn.close()
    return project_id


def update_project(project_id, **kwargs):
    conn = get_db()
    sets = ", ".join(f"{k} = ?" for k in kwargs)
    vals = list(kwargs.values()) + [project_id]
    conn.execute(f"UPDATE projects SET {sets}, updated_at = CURRENT_TIMESTAMP WHERE id = ?", vals)
    conn.commit()
    conn.close()


def get_project(project_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def list_projects(channel_slug=None):
    conn = get_db()
    if channel_slug:
        rows = conn.execute(
            "SELECT * FROM projects WHERE channel_slug = ? ORDER BY created_at DESC", (channel_slug,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
