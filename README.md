# linux-env

Useful scripts, dotfiles, and other configs for carrying around with me from one Linux environment to another.

## Contents

### requirements.txt

A list of packages necessary to run the Python scripts contained herein. 

### update-julia.py

A Python script for finding the latest version of [Julia][julia], installing it in `/opt`, and symlinking `/opt/julia`
to that latest version.
Also tries to point `/usr/local/bin/julia` to `/opt/julia/bin/julia`.
Obviously needs to be run as root, though I should probably support a non-global option.

[julia]: https://julialang.org