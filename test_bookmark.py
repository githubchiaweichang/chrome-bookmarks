import unittest
import bookmark


class TestMethods(unittest.TestCase):
    def test_bookmark(self):
        bookmark.main()
        with open('NEW.html', 'r', encoding='utf8') as new_file, open('TEST.html', 'r', encoding='utf8') as true_file:
            self.assertEqual(new_file.readlines(), true_file.readlines())


if __name__ == '__main__':
    unittest.main()
