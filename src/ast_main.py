from tqdm import tqdm
from src.core.ast_processing.creation.create_ast import get_ast_from_file
from src.core.ast_processing.ast_classes.AstTransformer import AstTransformer
from src.core.util.file_management import create_folder_if_necessary
import os


def main():

    dataset = '../res/r_small'
    target = '../res/r_small_ast'

    create_folder_if_necessary(target)

    all_dir = os.listdir(dataset)
    already_done = os.listdir(target)

    progress_bar = tqdm(total=len(all_dir), desc="creating AST's")

    for subdir, dirs, files in os.walk(dataset):
        progress_bar.update(n=1)

        if '.DS_Store' in files:
            continue

        repository = subdir.split('/')[-1]
        path = f'{target}/{repository}'
        if repository in already_done:
            continue
        create_folder_if_necessary(path)

        for file in files:
            try:
                ast = get_ast_from_file(os.path.join(subdir, file))
            except Exception:
                continue

            AstTransformerObject = AstTransformer(ast)
            if len(AstTransformerObject.get_function_nodes()) == 0:
                # ToDO im zweiten Durchgang
                continue
            else:
                ast_dic_list = AstTransformerObject.function_ast_dic_list()
                for function_dic in ast_dic_list:
                    function_name = function_dic['name']
                    function_ast = function_dic['ast_processing']
                    json_file = f'{function_name}.json'
                    try:
                        function_ast.to_json(f'{path}/{json_file}')
                    except Exception:
                        continue


if __name__ == '__main__':
    main()

