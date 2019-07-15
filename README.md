# code-simil

Find similarity between files of a source code base.

Uses TF-IDF algorithm with n-grams.

## Usage

    usage: main [-h] [-l LOGFILE] [-q] [-s] [-v] [-r] [-f FACTOR]
                paths [paths ...]
    
    positional arguments:
      paths                 path to codebase
    
    optional arguments:
      -h, --help            show this help message and exit
      -l LOGFILE, --logfile LOGFILE
                            log to file (default: log to stdout)
      -q, --quiet           decrease the verbosity
      -s, --silent          only log warnings
      -v, --verbose         raise the verbosity
      -r, --recurse         recurse on paths
      -f FACTOR, --factor FACTOR
                            similarity factor
                            
                            
                            
## License

See LICENSE file for details

(c) 2019 Eduardo Díaz Cortés