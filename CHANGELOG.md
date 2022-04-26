# 0.3.1

- fix bug where packages with blank releases would raise an error

# 0.3.0

- implement PackageObject.releases
- add util.py
- deprecate http.get_info and http.get_release_info, removal in 1.0.0
- add release date and time to CLI return
- add notifier if version has been yanked

# 0.2.0

- remove `requests` dependency in favor of stdlib's `http.client` implementation
- bump required python version down to 3.7
    - no 3.6 due to dataclasses import in `types.py`

# 0.1.2

- add --version argument, used to print current otlet version
- add `exceptions.py` and implement "custom" exceptions
- add differentiation between when no package found in API and  when package version not found

# 0.1.1

- version bump for PyPI push

# 0.1.0

- initial release