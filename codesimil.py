#!/usr/bin/env python3
import cli.log
import sys
from pathlib import Path
import pygount
import logging
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import traceback

_log_pygount = logging.getLogger('pygount')
_log_pygount.disabled = True


class CodeSimil(cli.log.LoggingApp):

    def __init__(self, main=None, **kwargs):
        super().__init__(main=None, **kwargs)
        self.lang_files = {}
        self.analysis = {}
        self.process_files = 0

    def process_paths(self, paths):
        for path in paths:
            for file in path.glob('*'):
                if file.is_file():
                    self.process_file(file, path)
                elif file.is_dir() and self.params.recurse:
                    self.process_paths([file])


    def process_file(self, file, path):
        try:
            analysis = pygount.source_analysis(file, str(path), encoding='chardet')
            if analysis is not None and analysis.code > 0 and analysis.language is not None:
                self.analysis[file] = analysis
                if analysis.language in self.lang_files:
                    self.lang_files[analysis.language].append(file)
                else:
                    self.lang_files[analysis.language] = [file]
                self.process_files += 1
                print(analysis.language, len(self.lang_files[analysis.language]), "processed files:", self.process_files,  end=" "*80+"\r")

        except:
            self.log.warning("couldn't process file {}".format(file))
            pass

    def process_langs(self):
        print("processing languages\n\n")
        for lang in self.lang_files.keys():
            self.process_lang(lang)

    def process_lang(self, lang):
        try:
            print('process lang', lang, end='\r')
            files = self.lang_files[lang]
            if len(files) <= 1:
                return

            print("processing lang", lang, len(files), 'files...')
            vectorizer = TfidfVectorizer(input="filename", decode_error='ignore',
                                         lowercase=False, analyzer='word',
                                         token_pattern=r'\".*\"|\'\.*\'|\w+|\d+|\S+',
                                         ngram_range=(1, 4))

            tfidf = vectorizer.fit_transform(self.lang_files[lang])
            similarity_matrix = (tfidf * tfidf.T).A
            (n, m) = similarity_matrix.shape
            simils = {}
            for i in range(n):
                simils[files[i]] = list()
                for j in range(i+1, n):
                    if i != j and similarity_matrix[(i, j)] >= self.params.factor:
                        simils[files[i]].append((str(files[j]), similarity_matrix[(i,j)]))

            for k in simils.keys():
                if len(simils[k]) > 0:
                    print(k, '=>')
                    for (f,s) in simils[k]:
                        print('\t', f, '\t', s)
                    print('\n')
            print('\n')
        except:
            self.log.warning("couldn't proces lang {}".format(lang))
            pass

    def similar_size(self, file1, file2):
        a1 = self.analysis[file1]
        a2 = self.analysis[file2]
        mc = max(a1.code, a2.code)
        delta = abs(a1.code - a2.code)
        f = delta / mc if mc > 0 else 0
        return f > 0.5


    def main(self):
        paths = [Path(p) for p in self.params.paths]
        print("clasifying")
        self.process_paths(paths)
        self.process_langs()




if __name__ == "__main__":
    codesimil = CodeSimil()
    codesimil.add_param("-r", "--recurse", help="recurse on paths", action='store_const', const=True, default=False)
    codesimil.add_param("-f", "--factor", help="similarity factor", type=float, default=0.6)
    codesimil.add_param("paths", help="path to codebase", nargs='+', type=str)

    codesimil.run()


