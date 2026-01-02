import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from database.save_result import test_connect, test_table_exists


def test_database():
    test_connect()
    test_table_exists()
