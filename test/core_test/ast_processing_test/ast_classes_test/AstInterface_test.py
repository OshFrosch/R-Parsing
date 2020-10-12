from src.core.ast_processing.ast_classes.AstInterface import AstInterface
from src.core.ast_processing.create_asts.create_ast import get_ast_from_file
import pandas as pd
import unittest


class MainFileTest(unittest.TestCase):
    def setUp(self) -> None:
        self.path = '../../../test_data/acer/mixture.R'
        self.ast = get_ast_from_file(self.path)
        self.ast_interface = AstInterface(self.ast)
        self.childs_of_root = [107, 361, 676, 906, 1210, 1503, 1599, 1755, 1917]
        self.root_leave = 107

    def test_get_children(self):
        self.assertEqual(len(self.ast_interface.childrens) == 0, True)
        self.assertListEqual(self.ast_interface.get_children(0), self.childs_of_root)
        self.assertEqual(len(self.ast_interface.childrens) > 0, True)

    def test_get_parent(self):
        self.assertEqual(self.ast_interface.get_parent(self.root_leave) == 0, True)

    def test_is_root_leave(self):
        self.assertEqual(self.ast_interface.is_root_leave(self.root_leave), True)
        self.assertEqual(self.ast_interface.is_root_leave(223), False)

    def test_get_df(self):
        df = self.ast_interface.get_df()
        self.assertEqual(df, self.ast)
        self.assertEqual(type(df), pd.DataFrame)

    def test_get_path(self):
        path = self.ast_interface.get_path(self.root_leave, 906)
        self.assertEqual(type(path) is list, True)
        self.assertEqual(len(path) == 3, True)
        self.assertEqual(path[0] == self.root_leave, True)
        self.assertEqual(path[-1] == 906, True)
        self.assertEqual(0 in path, True)


if __name__ == '__main__':
    unittest.main()
