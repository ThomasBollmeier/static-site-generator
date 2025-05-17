def copy_dir(src, dst):
    """
    Copy a directory from src to dst.
    """
    import os
    import shutil

    if not os.path.exists(src):
        raise FileNotFoundError(f"Source directory {src} does not exist.")

    if os.path.exists(dst):
        shutil.rmtree(dst)

    shutil.copytree(src, dst)
    print(f"Copied {src} to {dst}")