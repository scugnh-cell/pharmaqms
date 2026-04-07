"""
Data migration tool: TiDB Cloud -> local SQLite
Run this ONCE during build to generate pharma_qms.db with production data.

Usage:
  pip install pymysql sqlalchemy
  set DATABASE_URL=mysql+pymysql://user:pass@host:port/db?ssl_verify_cert=true
  python migrate_data.py
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from app import create_app, db
from app.change_management.model import ChangeRequest, ActionItem


def migrate():
    source_url = os.environ.get("DATABASE_URL")
    if not source_url:
        print("ERROR: Set DATABASE_URL env var to point to the source database.")
        print("Example: set DATABASE_URL=mysql+pymysql://user:pass@host:port/dbname")
        sys.exit(1)

    # Connect to source
    source_engine = create_engine(source_url)
    print(f"Connected to source: {source_url.split('@')[1] if '@' in source_url else source_url}")

    # Read source data
    with Session(source_engine) as session:
        changes_raw = session.execute(text("SELECT * FROM change_request")).mappings().all()
        actions_raw = session.execute(text("SELECT * FROM change_action_item")).mappings().all()

    print(f"Read {len(changes_raw)} changes, {len(actions_raw)} action items from source.")

    # Write to local SQLite via Flask app
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        for row in changes_raw:
            change = ChangeRequest(**{k: v for k, v in row.items() if hasattr(ChangeRequest, k)})
            db.session.add(change)

        db.session.flush()

        for row in actions_raw:
            item = ActionItem(**{k: v for k, v in row.items() if hasattr(ActionItem, k)})
            db.session.add(item)

        db.session.commit()

    target_path = os.path.join(os.path.dirname(__file__), "..", "data", "pharma_qms.db")
    print(f"Migration complete. SQLite database at: {os.path.abspath(target_path)}")
    print(f"  {len(changes_raw)} change requests")
    print(f"  {len(actions_raw)} action items")


if __name__ == "__main__":
    migrate()
