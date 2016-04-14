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
```

For this to work `~/bin` will have to be in your `$PATH`. If its not, you can add it to your `~/.bashrc` file:

```
# Make backup
cp ~/.bashrc ~/.bashrc.backup
# Add ~/bin to $PATH
echo export PATH=$HOME/bin:$PATH >> ~/.bashrc
hash
```


## Usage
The help file can be view with
