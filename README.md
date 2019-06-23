# NAME

**fsholetree** - Tool to generate file tree with empty files based on
real file tree.

# SYNOPSIS

* fsholetree -h
* fsholetree /path/to/directory /path/to/result.squashfs
* fsholetree -l DEBUG -T /tmp /path/to/directory
  /path/to/result.squashfs -- -comp xz

# DESCRIPTION

**fsholetree** is like **cp --archive** or **rsync --archive**, but
without keeping actual contents of files and with mountable SquashFS
image as a result.

Written in Python, supports both Python 2 & 3. No dependencies except of
Python itself.

## Installation and usage

Easiest way:

```bash
git clone https://github.com/im-0/fsholetree
cd fsholetree

python -m fsholetree.cli -h
python -m fsholetree.cli /path/to/directory /path/to/result.squashfs
```

If you really want to install or package this: use `python.py` like with
any regular python project.

# BUGS

See issues on GitHub: <https://github.com/im-0/fsholetree/issues>.

# AUTHOR

**fsholetree** was written by Ivan Mironov \<mironov.ivan@gmail.com>
