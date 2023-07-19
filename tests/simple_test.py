import unittest


class SimpleTest(unittest.TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_main(self):
        return "ok"


if __name__ == "__main__":
    unittest.main()
