import argparse
from pathlib import Path

from rtsw.persist import manage, connect_db_from_env

parser = argparse.ArgumentParser(description="Manage the database.")
parser.add_argument(
    "--migrations-dir",
    help="Path to the migrations directory.",
    default=Path("db/migrations"),
    action="store",
    type=Path,
)

subparsers = parser.add_subparsers(
    help="Pick which action to perform on the database", dest="command"
)

forward = subparsers.add_parser("forward", help="Apply pending migrations.")
forward_g = forward.add_mutually_exclusive_group(required=True)
forward_g.add_argument("--all", help="Apply all migrations.", action="store_true")
forward_g.add_argument(
    "-n", help="Apply n up migrations from the latest", action="store", type=int
)

rollback = subparsers.add_parser("rollback", help="Rollback the last migration.")
rollback_g = rollback.add_mutually_exclusive_group(required=True)
rollback_g.add_argument("--all", help="Rollback all migrations.", action="store_true")
rollback_g.add_argument(
    "-n", help="Rollback n down migrations from the latest", action="store", type=int
)

subparsers.add_parser("list_applied", help="List applied migrations.")
subparsers.add_parser("list_pending", help="List pending migrations.")
subparsers.add_parser("list_available", help="List available migrations.")

args = parser.parse_args()

with connect_db_from_env() as conn:
    match args.command:
        case "forward":
            manage.forward(args.migrations_dir, conn, args.n)
        case "rollback":
            manage.rollback(args.migrations_dir, conn, args.n)
        case "list_applied":
            print(manage.list_applied(conn))
        case "list_available":
            available = manage.list_migrations(args.migrations_dir)
            for m in available:
                print(m.name)
        case "list_pending":
            pending = manage.list_pending(args.migrations_dir, conn)
            for m in pending:
                print(m.name)
