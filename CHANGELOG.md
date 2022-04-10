# 0.2.1

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