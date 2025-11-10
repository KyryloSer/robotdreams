import tempfile
import unittest
from pathlib import Path

from lec02.utils.file_utils import get_file_name, prepare_dir, prepare_and_get_file_path


class FileUtilsTestCase(unittest.TestCase):
    def test_get_file_name_uses_dir_name_and_extension(self):
        path = "data/2023-01-01"
        assert get_file_name(path, extension="avro") == "sales_2023-01-01.avro"
        assert (
            get_file_name("data/2023-01-02/", extension="json")
            == "sales_2023-01-02.json"
        )

    def test_prepare_dir_creates_and_cleans_directory(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "target_dir"
            target.mkdir(parents=True, exist_ok=True)
            (target / "a.txt").write_text("foo")
            nested = target / "nested"
            nested.mkdir()
            (nested / "b.txt").write_text("bar")

            self.assertTrue((target / "a.txt").exists())
            self.assertTrue((nested / "b.txt").exists())

            returned = prepare_dir(str(target))

            self.assertIsInstance(returned, Path)
            self.assertEqual(returned.resolve(), target.resolve())

            self.assertTrue(target.exists())
            self.assertEqual(list(target.iterdir()), [])

    def test_prepare_and_get_file_path_returns_expected_path(self):
        with tempfile.TemporaryDirectory() as td:
            dir_path = Path(td) / "2024-01-01"
            dir_path.mkdir(parents=True, exist_ok=True)
            (dir_path / "old.txt").write_text("old")

            result_path = prepare_and_get_file_path(str(dir_path), extension="avro")

            self.assertEqual(result_path.parent.resolve(), dir_path.resolve())
            expected_name = f"sales_{dir_path.name}.avro"
            self.assertEqual(result_path.name, expected_name)

            self.assertTrue(dir_path.exists())

    def test_prepare_dir_creates_missing_directory(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "new_dir"
            self.assertFalse(target.exists())
            returned = prepare_dir(str(target))
            self.assertTrue(target.exists())
            self.assertEqual(returned.resolve(), target.resolve())
