#!/usr/bin/env python3
import cli.log
from pathlib import Path
import pygount
import logging


_log_pygount = logging.getLogger('pygount')
_log_pygount.disabled = True


class CodeSimil(cli.log.LoggingApp):

    def __init__(self, main=None, **kwargs):
        super().__init__(main=None, **kwargs)
        self.lang_files = {}
        self.process_files = 0

    def process_paths(self, paths):
        for path in paths:
            for file in path.glob('*'):
                if file.is_file():
                    self.process_file(file, path)
                elif file.is_dir() and self.params.recurse:
                    self.process_paths([file])

    def process_file(self, file, path):
        analysis = pygount.source_analysis(file, str(path), encoding='chardet')
        if analysis.code > 0:
            if analysis.language in self.lang_files:
                self.lang_files[analysis.language].append(file)
            else:
                self.lang_files[analysis.language] = []
            self.process_files += 1
            print(analysis.language, len(self.lang_files[analysis.language]), "files:", self.process_files,  end=" "*80+"\r")


    def main(self):
        paths = [Path(p) for p in self.params.paths]
        print("clasifying")
        self.process_paths(paths)
        for key in self.lang_files.keys():
            print(key, len(self.lang_files[key]))


if __name__ == "__main__":
    codesimil = CodeSimil()
    codesimil.add_param("-r", "--recurse", help="recurse on paths", action='store_const', const=True, default=False)
    codesimil.add_param("paths", help="path to codebase", nargs='+', type=str)

    codesimil.run()


