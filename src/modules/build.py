# build.py
"""
For building CoreBench as a redistributable archive.

author: T. de R-R
license: Apache-2.0
date: 07.01.26
"""
# modules/build.py

import zipfile, os

def zip_release(output_zip: str = "build.zip"):
    filenames = ["src", "corebench.bat", "corebench.sh", "requirements.txt"]
    deletions = ["apikey.txt", "output.png"]

    with zipfile.ZipFile(output_zip, "w", compression=zipfile.ZIP_DEFLATED) as zipf:
        for p in filenames:
            if os.path.isdir(p):
                # Walk through the directory and add files
                for root, _, files in os.walk(p):
                    for f in files:
                        full_path = os.path.join(root, f)
                        # Makes archive path relative
                        arcname = os.path.relpath(full_path, start=os.path.dirname(p))
                        zipf.write(full_path, arcname)
            else:
                zipf.write(p, arcname=os.path.basename(p))

    for delete in deletions:
        if os.path.isfile(delete):
            os.remove(delete)