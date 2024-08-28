import sqlite3

def init_db():
    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            mode TEXT NOT NULL,
            duration TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(origin, destination, mode)
        )
    ''')
    conn.commit()
    conn.close()

def add_search(origin, destination, mode, duration):
    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    try:
        c.execute('''
            INSERT OR IGNORE INTO history (origin, destination, mode, duration)
            VALUES (?, ?, ?, ?)
        ''', (origin, destination, mode, duration))
        
        c.execute('''
            DELETE FROM history
            WHERE id NOT IN (
                SELECT id FROM history
                ORDER BY timestamp DESC
                LIMIT 5
            )
        ''')
        conn.commit()
    except Exception as e:
        print(f"Error adding search: {e}")
    finally:
        conn.close()

def recent_searches(limit=5):
    conn = sqlite3.connect('search_history.db')
    c = conn.cursor()
    c.execute('SELECT origin, destination, mode, duration FROM history ORDER BY timestamp DESC LIMIT ?', (limit,))
    results = c.fetchall()
    conn.close()
    return results