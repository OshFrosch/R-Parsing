from src.core.ast_processing.ast_classes.AstInterface import AstInterface


class AstTransformer(AstInterface):
    def __init__(self, df):
        super().__init__(df)

    def is_root_function(self, node_id):
        is_function = super().token(node_id) == 'FUNCTION'
        is_root = False
        if is_function:
            try:
                is_root = super().get_parent(super().get_parent(
                            super().get_parent(node_id))) == 0
            except Exception:
                is_root = False

        return is_function and is_root

    def get_function_root(self, node_id):
        return super().get_parent(super(AstTransformer, self).get_parent(node_id))

    def get_function_nodes(self):
        function_nodes = []
        for j in self.ast.index:
            j = int(j)
            if self.is_root_function(j):
                function_nodes.append(self.get_function_root(j))
        return function_nodes

    def get_function_name(self, function_root_id):
        function_name = 'function_name_not_found'
        children = super().get_children(function_root_id)
        for child in children:
            if super().token(child) == 'expr':
                grand_children = super().get_children(child)
                if len(grand_children) == 1:
                    return super().text(grand_children[0])
        return function_name

    def function_ast_dic_list(self):
        ast_list = []
        f = self.get_function_nodes()
        for function_node in f:
            function_name = self.get_function_name(function_node)
            # here index values and position_values are used
            start = self.ast.index.get_loc(f'{function_node}')
            end = start
            root_node = False
            while not root_node:
                end += 1
                end_id = self.ast.index.values[end]
                root_node = super().is_root_leave(end_id) or not end < self.length - 1
            # slicing the ast_processing for the function
            ast_dic = {'ast_processing': self.ast[start:end],
                       'name': function_name}
            ast_list.append(ast_dic)

        return ast_list
