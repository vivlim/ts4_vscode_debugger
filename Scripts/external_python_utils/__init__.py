# SPDX-SnippetCopyrightText: 2025 viviridian
# SPDX-License-Identifier: MIT OR Apache-2.0

import typing


class WantedPackage:
    def __init__(self, name, version):
        self.name = name
        self.version = version
    
    def to_pip_arg(self):
        return f'{self.name}=={self.version}'

class PackageDir:
    def __init__(self, name, logger, provided_external_python_path):
        self.name = name
        self.logger = logger
        self.external_python_path = self.get_external_python_path(provided_external_python_path)

        import os,tempfile
        packages_path = os.path.join(tempfile.gettempdir(), 'ts4_python_packages', 'vscode_debug');
        os.makedirs(packages_path, exist_ok=True)
        self.packages_path = packages_path
        logger(f'using package path: {packages_path}')
    
    def get_external_python_path(self, provided):
        import os
        if provided:
            if os.path.exists(provided):
                self.logger(f'using provided python at {provided}')
                return provided
            else:
                self.logger(f'the python path {provided} was not found')

        # try windows appdata user install before doing anything more extreme
        pp = os.path.join(os.getenv('APPDATA'), 'Local', 'Programs', 'Python', 'Python37', 'python.exe')
        # pp = None # uncomment this to test the registry stuff
        if pp and os.path.exists(pp):
            self.logger(f'found python at {pp}')
            return pp
        
        # registry time. unfortunately winreg isn't available in ts4 so as a fallback, we'll try powershell
        
        def powershell(script):
            import subprocess
            args = ['powershell', '-c', script]
            result = subprocess.run(args=args, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                return None
            return result.stdout.strip()

        # keys that may contain a python path - https://stackoverflow.com/a/648552
        for reg_path in [
            'HKLM:\\Software\\Python\\PythonCore\\3.7\\InstallPath',
            'HKCU:\\Software\\Python\\PythonCore\\3.7\\InstallPath',
            'HKLM:\\Software\\Wow6432Node\\Python\\PythonCore\\3.7\\InstallPath',
        ]:
            pp = powershell(f'Get-ItemPropertyValue "{reg_path}" "ExecutablePath"')
            if pp and os.path.exists(pp):
                self.logger(f'found python at {pp} (via powershell + registry)')
                return pp
        
        raise Exception(f"Couldn't find a python 3.7 install. Please install 3.7.9 if you don't have it, or edit the script to hardcode it.")

    def ensure_in_search_path(self):
        import sys
        if not self.packages_path in sys.path:
            sys.path.append(self.packages_path)
            self.logger(f'added {self.packages_path} to search path (sys.path)')

    def pip_packages(self, packages: typing.List[WantedPackage]):
        import os
        pip_path = os.path.join(os.path.dirname(self.external_python_path), "Scripts", "pip.exe")
        if not os.path.exists(pip_path):
            raise Exception(f"Expected pip at {pip_path}, but it wasn't there.")
        
        def pip_install(package: WantedPackage):
            import subprocess
            args = [pip_path, 'install', '-t', self.packages_path, package.to_pip_arg()]
            result = subprocess.run(args=args, shell=True, capture_output=True, text=True)
            self.logger(f'stdout: {result.stdout}')
            self.logger(f'stderr: {result.stderr}')
            if result.returncode != 0:
                raise Exception(f"exit code was {result.returncode}")
            #.decode("utf-8").strip()

        for package in packages:
            ppath = os.path.join(self.packages_path, package.name)
            if os.path.exists(ppath):
                self.logger(f'already installed: {package.name} {package.version}')
            else:
                self.logger(f'installing {package.name} {package.version}...')
                try:
                    pip_install(package)
                    if os.path.exists(ppath):
                        self.logger(f'package successfully installed: {package.name} {package.version}')

                except Exception as e:
                    self.logger(f'failed to install: {package.name} {package.version}')
                    raise e

    def call_python_exe(self, args):
        import subprocess
        args = [self.external_python_path] + args
        return subprocess.check_output(args=args, shell=True).decode("utf-8").strip()

    def from_external_python_import(self, name):
        import os
        ppath = os.path.join(self.packages_path, name)
        if os.path.exists(ppath):
            self.logger(f'already copied: {name}')
            return

        source_package_path = self.call_python_exe(['-c', f'import {name}; print({name}.__path__[0])'])

        self.logger(f"found {name} at {source_package_path}")
        if not os.path.exists(source_package_path):
            raise Exception(f"unexpected: {source_package_path} doesn't exist")
        print(f'going to copy {source_package_path} -> {ppath}')
        import shutil
        shutil.copytree(source_package_path, ppath)
        print(f'done copying {name}')

if __name__ == "__main__":
    def logger(l):
        print(l)

    pd = PackageDir("test_package_dir", logger, None)
    pd.pip_packages([WantedPackage('absolutely-nothing', '1.0.0')])
