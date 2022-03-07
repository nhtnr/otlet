<div align="center">
    <img src=".github/otlet.png" alt="otlet readme image"><br>
    CLI tool and wrapper for the PyPI JSON Web API.
</div>

# Installing

Otlet supports Python 3.7 and above, but at least Python 3.8 is recommended.

The simplest method is installing otlet from PyPI using pip:  
  
```pip install otlet```

It can also be installed from source using the [Poetry dependency management system](https://python-poetry.org/):  
  
```
# from root project directory

# build wheel from source and install
poetry build
cd dist && pip install ./path-to-otlet-wheel.whl

# install directly with pyproject.toml and masonry (poetry build API)
pip install .
```