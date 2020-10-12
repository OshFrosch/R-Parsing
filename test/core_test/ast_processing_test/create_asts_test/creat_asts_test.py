import src.core.ast_processing.create_asts.create_ast as ca
import pandas as pd
import unittest


class MainFileTest(unittest.TestCase):
    def setUp(self) -> None:
        self.path_a = '../../../test_data/acer/aaa.R'
        self.path_b = '../../../test_data/acer/mixture.R'
        self.ast_columns = ['line1', 'col1', 'line2', 'col2', 'id', 'parent', 'token', 'terminal', 'text']
        self.df_a = ca.get_ast_from_file(self.path_a)
        self.df_b = ca.get_ast_from_file(self.path_b)

    def test_create_ast(self):
        self.assertEqual(type(self.df_a) is pd.DataFrame, True)
        self.assertEqual(type(self.df_b) is pd.DataFrame, True)
        self.assertListEqual(list(self.df_a.columns), self.ast_columns)
        self.assertListEqual(list(self.df_b.columns), self.ast_columns)

    def tearDown(self) -> None:
        self.path_a = ''
        self.path_a = ''
        self.ast_columns = []


if __name__ == '__main__':
    unittest.main()
