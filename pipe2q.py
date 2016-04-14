#!/usr/bin/env python2
#
# Reads commands from the standard in and submits them to the queue using qsub
#

import subprocess
import time
import sys
import argparse
from tempfile import NamedTemporaryFile
import os

def main():

    # Parse args
    args = parse_arguments()
    # Parse walltime
    wt = parse_walltime(args.wt)

    # Run commands using qsub
    for cmds in chunks(list(yield_commands()), args.batch):
        qsub(cmds, procs=args.procs, wt=wt, name=args.n, istest=args.testq)

    return 0

def yield_commands():
    """ Parse commands from the stdin and yield one at a time
    """
    # isatty() will be False if stdin not empty
    if not sys.stdin.isatty():
        for line in sys.stdin:
            yield line.rstrip()
    else:
        # Return warning if stdin empty
        sys.exit("ERROR: Standard input is required. For usage see: pipe2q -h")

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i+n]

def parse_walltime(wt_arg):
    """ Converts walltimes to format dd:hh:mm:ss.
    """
    # Clean the wt
    parts = wt_arg.split(":")
    wt_clean = ["{0:02d}".format(int(value)) for value in parts]
    # Pad with 00
    wt_clean = ["00"] * (4 - len(wt_clean)) + wt_clean
    # Join and return
    return ":".join(wt_clean)

def parse_arguments():
    """ Parses command line arguments.
    """
    # Create top level parser.
    parser = argparse.ArgumentParser(
        prog="pipe2q",
        description="Pipe jobs to the queue",
        usage="%(prog)s [options] < commands.txt\nusage: cat commands.txt | %(prog)s [options]")

    # Add options
    parser.add_argument('--wt', metavar="<dd:hh:mm:ss>",
        help=('Specify amount of walltime. E.g. 10:00 (is 10 min), 10:00:00 (is'
              ' 10 hours), 10:00:00:00 (is 10 days).'),
        required=True,
        type=str)
    parser.add_argument('--procs', metavar="<int>",
        help=('Number of processors (default: 1)'),
        required=False,
        default=1,
        type=int)
    parser.add_argument('--batch', metavar="<int>",
        help=('Group commands into batches of this size. (default: 1)'),
        required=False,
        default=1,
        type=int)
    parser.add_argument('--n', metavar="<str>",
        help=('Name of job. Prefix n-* will be added.'),
        required=False,
        type=str)
    parser.add_argument('--testq',
        help=('Add commands to the test queue.'),
        action='store_true')

    # Parse the arguments
    args = parser.parse_args()

    # Parse the arguments
    return args

def qsub(cmd_list, nodes=1, procs=1, wt="00:00:10:00", name=None, istest=True):
    """ Submit a command to the cluster.
    """

    # Open a tempory file and write contents
    tf = NamedTemporaryFile(delete=False)

    # Write shebang
    tf.write("#!/bin/sh\n")
    # Nodes and proc
    tf.write("#PBS -l nodes={0}:ppn={1}\n".format(nodes, procs))
    # Walltime
    tf.write("#PBS -l walltime={0}\n".format(wt))
    # Name
    if name:
        tf.write("#PBS -N n-{0}\n".format(name))
    # If test add to testq
    if istest:
        tf.write("#PBS -q testq\n")

    # Change to working dir
    tf.write("\nif [ ! -z ${PBS_O_WORKDIR+x} ]; then\ncd $PBS_O_WORKDIR\nfi\n")

    # Add commands
    tf.write("\n{0}\n".format("\n".join(cmd_list)))

    # Close tempfile
    tf.close()
    # Submit
    subprocess.call("qsub {0}".format(tf.name), shell=True)
    # Sleep
    time.sleep(1)
    # Remove temp file
    # print tf.name
    os.remove(tf.name)

    return 0

if __name__ == "__main__":
    main()
