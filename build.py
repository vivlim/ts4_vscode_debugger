# simplified build
# based on June Hanabi's template https://github.com/junebug12851/Sims4ScriptingBPProj and, transitively, andrew's tutorial https://sims4studio.com/thread/15145/started-python-scripting
# but cut down to just the bare essentials needed to compile the scripts & produce a .ts4script archive.

import fnmatch, logging, os, shutil
import typing
import build_tools.import_crawler;
import build_tools.compile;
from pathlib import Path
from zipfile import PyZipFile, ZIP_DEFLATED

entry_filename = 'inspector_gadget.py'

dirs_to_not_allow_emptying = ['Scripts', '']

def get_dir(name: str) -> Path :
    d = Path(__file__).parent.joinpath(name)
    d.mkdir(parents= True, exist_ok= True)
    return d

def open_zip(file_path) -> PyZipFile:
    zip = PyZipFile(file_path, mode='w', compression=ZIP_DEFLATED, allowZip64=True, optimize=2)
    return zip

def collect_wanted_sources(source: Path):
    crawler = build_tools.import_crawler.ImportCrawler(source)
    crawler.start_crawl(source.joinpath(entry_filename))
    return crawler.get_visited_relative_paths()

def stage_wanted_files(source: Path):
    # Create stage and make sure it is empty
    stage = get_dir('stage')
    shutil.rmtree(stage)
    stage.mkdir(parents=True, exist_ok=True)

    wanted_files = []
    wanted_files.extend(collect_wanted_sources(source))
    
    for f in wanted_files:
        print(f'staging {f}')
        f_source = source.joinpath(f)
        f_stage = stage.joinpath(f)
        f_stage.parent.mkdir(parents= True, exist_ok= True)
        if source in f_source.parents and stage in f_stage.parents:
            shutil.copyfile(f_source, f_stage)
        else:
            raise Exception(f'Path is unexpectedly outside of a dir: {f_source} or {f_stage}')
    
    return stage
        
def get_short_commit():
    try:
        import subprocess
        out = subprocess.check_output(['git', 'rev-parse', '--short=6', 'HEAD'])
        short_hash = out.decode('utf-8').strip()
        if '\n' in short_hash:
            return 'err'
        return short_hash
    except:
        return 'unknownversion'


if __name__ == '__main__':
    stage = stage_wanted_files(get_dir('Scripts'))
    workdir = get_dir('workdir')
    shutil.rmtree(workdir)
    workdir = get_dir('workdir')

    build_tools.compile.compile_scripts_with_python(stage, workdir, '**/*.py', '3.7')

    outdir = get_dir('out')
    zip_path = outdir.joinpath(f'viviridian_inspector_gadget-{get_short_commit()}.ts4script')

    # final check to make sure nothing unwanted snuck into stage
    unwanted_globs = ['generated_build_script.*']
    any_unwanted_files_staged = False
    for ug in unwanted_globs:
        for uf in stage.glob(ug):
            any_unwanted_files_staged = True
            print(f'Unwanted file is staged: {uf}')
    if any_unwanted_files_staged:
        raise Exception('Unwanted files were staged during build, see above messages')
    
    # stage prebuilt dependencies

    with open_zip(zip_path) as zf:
        for f in stage.glob('**/*'):
            if f.is_file():
                rel_path = f.relative_to(stage)
                zf.write(f, rel_path)
