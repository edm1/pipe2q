#!/usr/bin/env python2
#
# Reads commands from the standard in and submits them to the queue using qsub
#

import subprocess
import time
import sys
import argparse
from tempfile import NamedTemporaryFile

def main():

    # Parse args
    args = parse_arguments()
    # Parse walltime
    wt = parse_walltime(args.wt)

    # If there is something in the standard input, isatty() will be False
    if not sys.stdin.isatty():
        # For each line in stdin, submit job
        for line in sys.stdin:
            cmd = line.rstrip()
            qsub(cmd, procs=args.procs, wt=wt, name=args.n, istest=args.testq)
    else:
        sys.exit("Standard input is required. For usage see: pipe2q -h")

    return 0

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

def qsub(cmd, nodes=1, procs=1, wt="00:00:10:00", name=None, istest=True):
    """ Submit a command to the cluster.
    """

    # Open a tempory file and write contents
    with NamedTemporaryFile(delete=False) as tf:

        print tf.name

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

        # Add the command
        tf.write("\n{0}\n".format(cmd))

        # Submit
        subprocess.call("qsub {0}".format(tf.name), shell=True)
        # Sleep
        time.sleep(1)

    return 0

if __name__ == "__main__":
    main()
