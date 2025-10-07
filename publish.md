# 🧱 Manual Publish (Local)

If you prefer to manually build and publish to **PyPI** instead of using GitHub Actions, this repo includes a helper script: [`scripts/publish.py`](scripts/publish.py).

---

## 🔧 1. Make sure your `.pypirc` is configured

Your `~/.pypirc` should be configured for **real PyPI** with an API token.

### **Configuration File**

````ini
[distutils]
index-servers =
    pypi

[pypi]
repository = [https://upload.pypi.org/legacy/](https://upload.pypi.org/legacy/)
username = __token__
password = pypi-<your_api_token>

Secure the File
Secure your configuration file to ensure only the owner can read or write to it:

chmod 600 ~/.pypirc

Here is the complete Markdown file, ready for you to copy and paste into your IDE:

Markdown

# 🧱 Manual Publish (Local)

If you prefer to manually build and publish to **PyPI** instead of using GitHub Actions, this repo includes a helper script: [`scripts/publish.py`](scripts/publish.py).

---

## 🔧 1. Make sure your `.pypirc` is configured

Your `~/.pypirc` should be configured for **real PyPI** with an API token.

### **Configuration File**

```ini
[distutils]
index-servers =
    pypi

[pypi]
repository = [https://upload.pypi.org/legacy/](https://upload.pypi.org/legacy/)
username = __token__
password = pypi-<your_api_token>
Secure the File
Secure your configuration file to ensure only the owner can read or write to it:

Bash

chmod 600 ~/.pypirc
🚀 2. Run the Publish Script
From the root directory of your repository, simply execute the publish script:

Bash

python scripts/publish.py
What the Script Does
This script automates the full publishing workflow:

Cleans previous build artifacts (i.e., dist/, build/, and *.egg-info).

Builds the wheel (.whl) and source distribution (.tar.gz).

Runs integrity checks on the built files using twine check.

Uploads the distributions to PyPI using the credentials in your ~/.pypirc.

Testing the Publish
If you'd like to test your package on TestPyPI first, you can manually edit the upload command inside scripts/publish.py to target the test repository:

Bash

twine upload --repository testpypi dist/*
🧪 Example Output
A successful publish run will display output similar to this:

Go

Cleaning old builds...
Building package...
Checking distribution files...
Uploading distributions to [https://upload.pypi.org/legacy/](https://upload.pypi.org/legacy/)
Upload complete! ✅
✅ Pro Tip: Alias for Quick Publishing
You can create a shell alias for quick, one-command publishing:

Bash

alias publish="python scripts/publish.py"
Then, you can simply run:

Bash

publish
from anywhere in your project to automatically rebuild and publish.
````
