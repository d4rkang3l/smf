#!/usr/bin/env python

import sys
import os
import logging
import logging.handlers
import subprocess
import argparse
import tempfile
import os.path
import json

fmt_string='%(levelname)s:%(asctime)s %(filename)s:%(lineno)d] %(message)s'
logging.basicConfig(format=fmt_string)
formatter = logging.Formatter(fmt_string)
for h in logging.getLogger().handlers: h.setFormatter(formatter)
logger = logging.getLogger('it.test')
logger.setLevel(logging.DEBUG)

def generate_options():
    parser = argparse.ArgumentParser(description='run smf integration tests')
    parser.add_argument('--binary', type=str,
                        help='binary program to run')
    parser.add_argument('--directory', type=str,
                        help='source directory of binary. needed for metadata')
    parser.add_argument('--test_type', type=str, default="unit",
                        help='either integration or unit. ie: --test_type unit')
    return parser



def get_git_root():
    ret = str(subprocess.check_output("git rev-parse --show-toplevel",
                                      shell=True))
    if ret is None:
        log.error("Cannot get the git root")
        sys.exit(1)
    return "".join(ret.split())

def test_environ():
    e = os.environ
    git_root = get_git_root()
    e["GIT_ROOT"] = git_root
    ld_path = ""
    if e.has_key("LD_LIBRARY_PATH"):
        ld_path = e["LD_LIBRARY_PATH"]
    libs = "{}/src/third_party/lib:{}/src/third_party/lib64:{}".format(
        git_root,git_root, ld_path)
    e["LD_LIBRARY_PATH"]=libs
    e["GLOG_logtostderr"]='1'
    e["GLOG_v"]='1'
    e["GLOG_vmodule"]=''
    e["GLOG_logbufsecs"]='0'
    e["GLOG_log_dir"]='.'
    e["GTEST_COLOR"]='no'
    e["GTEST_SHUFFLE"]='1'
    e["GTEST_BREAK_ON_FAILURE"]='1'
    e["GTEST_REPEAT"]='1'
    return e


def execute(cmd, environ):
    logger.info("Executing test: %s" % cmd)
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             # buffer one line at a time
                             bufsize=1,
                             shell=True,
                             universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        sys.stdout.write(stdout_line)
    popen.stdout.close()
    return_code = popen.wait()
    if return_code and return_code != 0:
        raise subprocess.CalledProcessError(return_code, cmd)

def load_test_config(directory):
    test_cfg = directory + "/test.json"
    if os.path.isfile(test_cfg) is not True:
        return None
    json_data = open(test_cfg).read()
    return json.loads(json_data)


def exec_test(binary, source_dir):
    test_env = test_environ()
    cfg = load_test_config(source_dir)
    if cfg is None:
        return execute(binary, test_env)
    if cfg.has_key("tmp_home"):
        dirpath = tempfile.mkdtemp()
        logger.info("Executing test in tmp dir %s" % dirpath)
        os.chdir(dirpath)
        test_env["HOME"]=dirpath
    cmd = binary
    if cfg.has_key("args"):
        cmd = ' '.join([cmd] + cfg["args"])
    return execute(cmd, test_env)

def main():
    parser = generate_options()
    options, program_options = parser.parse_known_args()

    if not options.binary:
        parser.print_help()
        raise Exception("Missing binary")
    if not options.directory:
        parser.print_help()
        raise Exception("Missing source directory")
    if not options.test_type:
        if (options.test_type is not "unit" or
            options.test_type is not "integration"):
            parser.print_help()
            raise Exception("Missing test_type ")

    exec_test(options.binary, options.directory)

if __name__ == '__main__':
    main()