from src.core.ast_processing.ast_classes.AstTransformer import AstTransformer
from src.core.ast_processing.create_asts.create_ast import get_ast_from_file
import pandas as pd
import unittest


class MainFileCase(unittest.TestCase):
    def setUp(self) -> None:
        self.path = '../../../test_data/acer/mixture.R'
        self.ast = get_ast_from_file(self.path)
        self.ast_transformer = AstTransformer(self.ast)
        self.function_node = 122
        self.function_root = 361
        self.function_name = 'pmixsurv'
        self.function_nodes = self.ast_transformer.get_function_nodes()
        pd.set_option("display.max_rows", None, "display.max_columns", None)
        # print(self.ast)

    def test_is_root_function(self):
        self.assertEqual(self.ast_transformer.is_root_function(self.function_node), True)
        self.assertEqual(self.ast_transformer.token(self.function_node) == 'FUNCTION', True)
        self.assertEqual(self.ast_transformer.is_root_function(375), True)
        self.assertEqual(self.ast_transformer.is_root_function(121), False)

    def test_get_function_root(self):
        self.assertEqual(self.ast_transformer.get_function_root(self.function_node), self.function_root)

    def test_get_function_nodes(self):
        function_nodes = self.ast_transformer.get_function_nodes()
        self.assertEqual(type(function_nodes) is list, True)
        self.assertEqual(len(function_nodes) > 0, True)
        self.assertEqual(self.function_root in function_nodes, True)

    def test_get_function_name(self):
        function_name = self.ast_transformer.get_function_name(self.function_root)
        self.assertEqual(type(function_name) is str, True)
        self.assertEqual(len(function_name) > 0, True)
        self.assertEqual(function_name, self.function_name)

    def test_function_ast_dic_list(self):
        ast_dicts = self.ast_transformer.function_ast_dic_list()
        self.assertEqual(type(ast_dicts) is list, True)
        self.assertEqual(type(ast_dicts[0]) is dict, True)
        self.assertEqual(len(ast_dicts) == len(self.function_nodes), True)
        function_ast = ast_dicts[0]['ast_processing']
        self.assertEqual(type(function_ast) is pd.DataFrame, True)
        self.assertEqual(function_ast['id'][0] == self.function_root, True)
        self.assertEqual(function_ast['parent'][0] == 0, True)
        self.assertEqual(function_ast['token'][f'{self.function_node}'], 'FUNCTION')
        # check if the df is complete and key error free
        for child in list(function_ast['parent']):
            if child > 0:
                self.assertEqual(child in list(function_ast['id']), True)


if __name__ == '__main__':
    unittest.main()
