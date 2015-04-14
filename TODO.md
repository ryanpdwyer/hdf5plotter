# Todo

- [ ] Make sure that adding columns to HDF5 files doesn't delete / overwrite
    data every time

# General comments
A few annoying issues.
- Nice `__repr__` function that lists groups in dataset
- Nice printing function to cycle through attributes, etc
- What happens if there are missing attributes? We should fail nicely; maybe warn when the data is loaded?
    - Write a function to check the labeling
- Transparently switch u to micro, ^ to unicode powers, etc in units labels. I think most of this code is already written
- Allow add to add a list of filenames
    - `f(['a', 'b', 'c'])` or `f('a', 'b', 'c')`?
    - Can pretty easily allow form 2 to accept a list with `*[list]`
    - What about the group argument? Just have it a named parameter at the end?
        - `f(*args, **kwargs)`
- Allow passing the file handle directly

# Command Line Tools
- [x] Switch from using show to creating a temporary pdf file, showing it, then deleting it

# Testing
- [ ] Test every function in `_util`

