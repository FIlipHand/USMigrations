import os


def get_project_root() -> str:
    """Returns the root directory of the current project."""
    # get the current working directory
    cwd = os.getcwd()

    # loop through parent directories until a known file or directory is found
    while True:
        # check for a known file or directory at the current path
        if os.path.exists(os.path.join(cwd, 'README.md')):
            return cwd
        # move up one directory
        cwd = os.path.dirname(cwd)
        # check if the root directory has been reached
        if cwd == os.path.dirname(cwd):
            raise Exception("Project root directory not found.")
