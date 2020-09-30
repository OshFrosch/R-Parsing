class AstInterface:
    def __init__(self, df):
        self.ast = df

    def get_df(self):
        return self.ast

    def is_root_leave(self, node_id):
        return self.get_parent(node_id) == 0

    def is_terminal(self, node_id):
        return self.ast['terminal'][f'{node_id}'] == 1

    def token(self, node_id):
        return self.ast['token'][f'{node_id}']

    def text(self, node_id):
        return self.ast['text'][f'{node_id}']

    def get_parent(self, node_id):
        return self.ast['parent'][f'{node_id}']

    def get_children(self, node_id):
        children = []
        for i in self.ast.index:
            if self.get_parent(i) == node_id:
                children.append(i)
        return children

    def get_path(self, node_start, node_end):
        end_to_root = [node_end]
        node = node_end
        while not node == 0:
            node = self.get_parent(node)
            end_to_root.append(node)
        root_to_end = end_to_root[::-1]
        start_to_mutual = []
        node = node_start
        while not (node in root_to_end):
            start_to_mutual.append(node)
            node = self.get_parent(node)
        mutual_root = node
        mutual_to_end = root_to_end[root_to_end.index(mutual_root):]
        return start_to_mutual + mutual_to_end
