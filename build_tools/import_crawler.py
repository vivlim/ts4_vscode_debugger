import fnmatch, logging, os, shutil
from pathlib import Path
import typing

class ImportCrawler:
    def __init__(self, root_dir: Path):
        self.visited_files: typing.List[Path] = []
        self.files_to_visit: typing.List[Path] = []
        self.root_dir = root_dir

    def start_crawl(self, root_file):
        import sys
        original_path = sys.path
        try:
            self.files_to_visit.append(root_file)
            self._do_crawl_inner()
        finally:
            sys.path = original_path
    def get_visited_relative_paths(self):
        for p in self.visited_files:
            yield p.relative_to(self.root_dir)

    
    def _do_crawl_inner(self):
        import importlib,sys
        while len(self.files_to_visit) > 0:
            f = self.files_to_visit.pop()

            if f in self.visited_files:
                # don't visit it twice
                continue
            
            print(f'list imports referenced by {f}')
            original_path = sys.path
            import_count = 0
            eligible_import_count = 0
            for imp in get_file_imports(f):
                import_count += 1
                try:
                    # add current dir to search path
                    sys.path.insert(0, str(f.parent.absolute()))

                    # try a relative import, see how it goes
                    #current = str(f.parent.absolute())
                    module = _import_module_rec(imp)
                    
                    module_path = Path(module.__file__)
                    #print(f'import {imp} -> {module}')
                    if self.root_dir in module_path.parents:
                        print(f'discovered {module_path}')
                        self.files_to_visit.append(module_path)
                        eligible_import_count += 1

                except Exception as e:
                    if 'vivlib' in imp:
                        import traceback
                        tb = traceback.format_exc()
                        print(f'couldn\'t import {imp}: {tb}')
                    pass
            print(f'file {f} contained {import_count} imports, {eligible_import_count} were eligible')
            print()
            sys.path = original_path
            self.visited_files.append(f)

def _import_module_rec(mod_name):
    import importlib,sys,pathlib
    if '.' in mod_name:
        orig_path = sys.path
        try:
            parts = mod_name.split('.')
            leaf_part = parts.pop()
            parent_mod = _import_module_rec('.'.join(parts))
            sys.path.append(str(pathlib.Path(parent_mod.__file__).parent.absolute()))
            return importlib.import_module(mod_name, package=parent_mod)
        finally:
            sys.path = orig_path
    return importlib.import_module(mod_name)



def get_file_imports(path):
    import ast
    with open(path) as fh:        
        root = ast.parse(fh.read(), path)

    for node in ast.walk(root):
        if isinstance(node, ast.Import):
            for n in node.names:
                yield n.name
        elif isinstance(node, ast.ImportFrom):  
            yield node.module
        else:
            continue

        #for n in node.names:
            #yield n.name
        #yield node.names[0].name
        # last = None

        # for n in node.names:
        #     last = n
        # if last:
        #     yield last
            #yield n.name #ast.Import(module, n.name.split('.'), n.asname)

if __name__ == '__main__':
    scripts_dir = Path(__file__).parent.parent.joinpath('Scripts')
    crawler = ImportCrawler(scripts_dir)
    crawler.start_crawl(scripts_dir.joinpath('dev_server.py'))
    print([str(x) for x in crawler.get_visited_relative_paths()])
    #jfor imp in get_imports(get_dir('Scripts').joinpath('dev_server.py')):
    #    print(imp)