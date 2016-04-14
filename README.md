# pipe2q
Script to pipe commands to the PBS queue

## Installation

You can either clone the git repository or copy the pipe2q.py script into your home directory. For example, to clone the repository in a folder called 'programs' then add a link in your local bin, you could:

```
# Make programs directory if it doesn't exist, then change to directory
mkdir -p ~/programs
cd ~/programs
# Clone the repository
git clone https://github.com/edm1/pipe2q.git

# Make ~/bin directory if it doesn't exist, then change to directory
mkdir -p ~/bin
cd ~/bin
# Add symbolic link to pipe2q
ln -s ~/programs/pipe2q/pipe2q.py pipe2q
hash
```

For this to work, `~/bin` will have to be in your `$PATH`. If its not, you can add it to your `~/.bashrc` file:

```
# Make backup
cp ~/.bashrc ~/.bashrc.backup
# Add ~/bin to $PATH
echo export PATH=$HOME/bin:$PATH >> ~/.bashrc
source ~/.bashrc
```


## Usage

```
$ pipe2q --help
usage: pipe2q [options] < commands.txt
usage: cat commands.txt | pipe2q [options]

Pipe jobs to the queue

optional arguments:
 -h, --help          show this help message and exit
 --wt <dd:hh:mm:ss>  Specify amount of walltime. E.g. 10:00 (is 10 min),
                     10:00:00 (is 10 hours), 10:00:00:00 (is 10 days).
 --procs <int>       Number of processors (default: 1)
 --n <str>           Name of job. Prefix n-* will be added.
 --testq             Add commands to the test queue.

```

pipe2q takes the stdin as input. In the simplest case, you could have a file containing a list of commands (e.g. commands.txt) and submit each job separately to the queue:

```
# Submit each job separately to 1 processor for 1 hour
cat commands.txt | pipe2q --wt 00:01:00:00 --procs 1
# Or
pipe2q --wt 00:01:00:00 --procs 1 < commands.txt
```

However, its useful for building and submitting complex commands to the queue on the fly. Eg:

```
# For each bed file
for bedfile in *.bed.gz; do

    # Create output name
    outfile=output/$(basename $bedfile)

    # Unzip
    # Find overlaps with regulatory elements
    # Sort the BED file
    # Gzip and save result
    # N.B. the whole command must inside "" and echo'ed
    echo "zcat $bedfile | bedtools intersect -wa -A regulatory_elements.bed.gz -B - | sort-bed | gzip -c > $outfile"

# Pipe the echoed commands to pipe2q
done | pipe2q --wt 00:01:00:00 --procs 1
```
