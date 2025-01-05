
import unittest
import os
import time
from pickledb import load

class TestPickleDBEnhanced(unittest.TestCase):

    def setUp(self):
        self.db_file = "test_db.json"
        self.db = load(self.db_file, auto_dump=True, enable_ttl=True)

    def tearDown(self):
        if os.path.exists(self.db_file):
            os.remove(self.db_file)
        if os.path.exists(f"{self.db_file}.gz"):
            os.remove(f"{self.db_file}.gz")

    # Enhanced List Features
    def test_lsort(self):
        self.db.lcreate("test_list")
        self.db.ladd("test_list", 3)
        self.db.ladd("test_list", 1)
        self.db.ladd("test_list", 2)
        self.assertEqual(self.db.lsort("test_list"), [1, 2, 3])
        self.assertEqual(self.db.lsort("test_list", reverse=True), [3, 2, 1])

    def test_lremove(self):
        self.db.lcreate("test_list")
        self.db.ladd("test_list", "item1")
        self.db.ladd("test_list", "item2")
        self.assertTrue(self.db.lremove("test_list", "item1"))
        self.assertEqual(self.db.lgetall("test_list"), ["item2"])
        self.assertFalse(self.db.lremove("test_list", "nonexistent"))

    def test_lgetrange(self):
        self.db.lcreate("test_list")
        self.db.ladd("test_list", "a")
        self.db.ladd("test_list", "b")
        self.db.ladd("test_list", "c")
        self.assertEqual(self.db.lgetrange("test_list", 0, 2), ["a", "b"])

    def test_llen(self):
        self.db.lcreate("test_list")
        self.db.ladd("test_list", "a")
        self.db.ladd("test_list", "b")
        self.assertEqual(self.db.llen("test_list"), 2)

    # Enhanced Dictionary Features
    def test_dremove(self):
        self.db.dcreate("test_dict")
        self.db.dadd("test_dict", "key1", "value1")
        self.assertTrue(self.db.dremove("test_dict", "key1"))
        self.assertFalse(self.db.dremove("test_dict", "key2"))

    def test_dmerge(self):
        self.db.dcreate("test_dict")
        self.db.dadd("test_dict", "key1", "value1")
        self.db.dmerge("test_dict", {"key2": "value2", "key3": "value3"})
        self.assertEqual(self.db.dgetall("test_dict"), {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        })

    def test_dkeys(self):
        self.db.dcreate("test_dict")
        self.db.dadd("test_dict", "key1", "value1")
        self.db.dadd("test_dict", "key2", "value2")
        self.assertEqual(set(self.db.dkeys("test_dict")), {"key1", "key2"})

    def test_dvalues(self):
        self.db.dcreate("test_dict")
        self.db.dadd("test_dict", "key1", "value1")
        self.db.dadd("test_dict", "key2", "value2")
        self.assertEqual(set(self.db.dvalues("test_dict")), {"value1", "value2"})

    # Additional Tests
    def test_persistence(self):
        self.db.set("key1", "value1")
        del self.db
        db = load(self.db_file, auto_dump=True)
        self.assertEqual(db.get("key1"), "value1")

    def test_invalid_ladd(self):
        with self.assertRaises(TypeError):
            self.db.ladd("nonexistent_list", "item")

    def test_invalid_dadd(self):
        with self.assertRaises(TypeError):
            self.db.dadd("nonexistent_dict", "key", "value")

    def test_compress(self):
        self.db.set("key1", "value1")
        self.assertTrue(self.db.compress())
        self.assertTrue(os.path.exists(f"{self.db_file}.gz"))

    def test_ttl_expiry(self):
        self.db.set("key1", "value1", ttl=1)
        time.sleep(2)
        self.assertIsNone(self.db.get("key1"))

    def test_clear(self):
        self.db.set("key1", "value1")
        self.db.set("key2", "value2")
        self.db.clear()
        self.assertEqual(len(self.db.getall()), 0)

    def test_deldb(self):
        self.db.set("key1", "value1")
        self.db.deldb()
        self.assertFalse(os.path.exists(self.db_file))

if __name__ == "__main__":
    unittest.main()
