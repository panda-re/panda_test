import fnmatch
import fnmatch
import os
import sys
import importlib.util

test_modules = {}

build_directory = os.getcwd()
data_directories = []
dry_run = False
verbose = False
build_is_bindir = False

def set_build_is_bindir(is_bindir):
    global build_is_bindir
    build_is_bindir = is_bindir

def set_build_dir(directory):
    global build_directory
    global build_is_bindir
    build_directory = directory
    plog_import_dirs = []
    if True == build_is_bindir:
        plog_import_dirs.append(os.path.join(build_directory, "..", "lib",
        "python2.7", "site-packages"))
    else:
        arch_dirs = ['i386-softmmu', 'x86_64-softmmu', 'arm-softmmu', 'ppc-softmmu']
        for ad in arch_dirs:
            plog_import_dirs.append(os.path.join(build_directory, ad))
    for pd in plog_import_dirs:
        sys.path.append(pd)

def get_build_is_bindir():
    global get_build_is_bindir
    return build_is_bindir

def get_build_dir():
    global build_directory
    return build_directory

def add_data_search_dir(d):
    global data_directories
    data_directories.append(d)

class DataAssetNotFoundError(Exception):
    def __init__(self, asset):
        super().__init__("Data asset \"%s\" failed to be resolved." % (asset))

def resolve_replay(replay):
    global data_directories
    for directory in data_directories:
        replay_path = os.path.join(directory, replay)
        snap_path = replay_path + "-rr-snp"
        nondet_path = replay_path + "-rr-nondet.log"
        if True == os.path.exists(snap_path) and True == os.path.exists(nondet_path):
            return replay_path
    raise DataAssetNotFoundError(replay)

def resolve_data_asset(asset):
    global data_directories
    for directory in data_directories:
        full_path = os.path.join(directory, asset)
        if True == os.path.exists(full_path):
            return full_path
    raise DataAssetNotFoundError(asset)

def set_dry_run(dr):
    global dry_run
    dry_run = dr

def set_verbose(v):
    global verbose
    verbose = v

def register_tests(directory):
    for testdir in os.listdir(directory):
        for test_file in os.listdir(os.path.join(directory, testdir)):
            if test_file.startswith("test_") and test_file.endswith('.py'):
                test_name = "%s.%s" % (testdir, os.path.splitext(test_file)[0])
                spec = importlib.util.spec_from_file_location(test_name,
                    os.path.join(directory, testdir, test_file))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                test_modules[test_name] = module

def run(includes=[], excludes=[]):
    for test_name, module in sorted(test_modules.items()):
        matched_includes = []
        for expr in includes:
            if fnmatch.fnmatch(test_name, expr):
                matched_includes.append(test_name)
        matched_excludes = []
        for expr in excludes:
            if fnmatch.fnmatch(test_name, expr):
                matched_excludes.append(test_name)
        if includes and test_name not in matched_includes:
            continue
        elif excludes and test_name in matched_excludes:
            continue

        if dry_run:
            print("[ DRY RUN     ]: %s" % (test_name))
            continue

        print("[ RUN         ]: %s" % (test_name))
        ok = module.run()
        module.cleanup()
        if ok:
            print("[          OK ]: %s" % (test_name))
        else:
            print("[        FAIL ]: %s" % (test_name))
