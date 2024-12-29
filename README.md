# 📂 ManDir

Manage-Directory [File management library]

## Usage

Warpping a Folder with Queue for files and folder inside, creating put and get actions with a overflow imit.

## How to Install

### Using PIP

To install the package using pip,

```bash
pip install "git+https://github.com/MrTechyWorker/ManDir.git"
```

### Using Setuptools
To install the package using setuptools,

```python
from setuptools import setup, find_packages

setup(
    name="foo",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "ManDir @ git+https://github.com/MrTechyWorker/ManDir.git"
    ] 
)
```

### Using `pyproject.toml`
To install the package using toml,

```toml

[project]
dependencies = [
    "ManDir @ git+https://github.com/MrTechyWorker/ManDir.git"
]
```
