import logging
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import psycopg as pg

log = logging.getLogger(__name__)


@dataclass
class Migration:
    index: int
    name: str
    up: Path
    down: Path


def up(migration: Migration, conn: pg.Connection):
    log.info("Applying up migration %s", migration.name)
    conn.execute(migration.up.read_text())  # type: ignore
    conn.execute("INSERT INTO _migrations (name) VALUES (%s)", (migration.name,))


def down(migration: Migration, conn: pg.Connection):
    log.info("Applying down migration %s", migration.name)
    conn.execute(migration.down.read_text())  # type: ignore
    conn.execute("DELETE FROM _migrations WHERE name = %s", (migration.name,))


def _prep(conn: pg.Connection):
    conn.execute("CREATE TABLE IF NOT EXISTS _migrations (name TEXT PRIMARY KEY)")
    conn.commit()


def list_pending(migrations_dir: Path, conn: pg.Connection) -> list[Migration]:
    _prep(conn)
    available = list_migrations(migrations_dir)
    applied = list_applied(conn)
    return [m for m in available if m.name not in applied]


def forward(migrations_dir: Path, conn: pg.Connection, n=None):
    _prep(conn)
    for m in list_pending(migrations_dir, conn):
        up(m, conn)

    conn.commit()


def rollback(migrations_dir: Path, conn: pg.Connection, n=None):
    _prep(conn)
    applied_names = list_applied(conn)
    available = list_migrations(migrations_dir)
    applied = [m for m in available if m.name in applied_names]
    applied.sort(key=lambda m: m.index, reverse=True)
    for m in applied:
        down(m, conn)

    conn.commit()


def list_migrations(migrations_dir: Path) -> list[Migration]:
    files = [f for f in migrations_dir.iterdir() if f.is_file() and f.suffix == ".sql"]

    migrations_by_name = defaultdict(list)
    for f in files:
        name = f.name.removesuffix(".down.sql").removesuffix(".up.sql")
        migrations_by_name[name].append(f)

    migrations = []

    for name, files in migrations_by_name.items():
        if len(files) != 2:
            raise ValueError(f"Migration {name} has {len(files)} files (requires 2)")

        up = next(f for f in files if f.name.endswith(".up.sql"))
        down = next(f for f in files if f.name.endswith(".down.sql"))
        index = int(name.split("_")[0])
        migrations.append(Migration(index, name, up, down))

    return migrations


def list_applied(conn: pg.Connection) -> list[str]:
    return [r[0] for r in conn.execute("SELECT name FROM _migrations").fetchall()]
