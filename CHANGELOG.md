# 1.0.0

- stable release
- split CLI into seperate package, 'otlet-cli'

### What's new?
<hr width=300 style="margin-left: 0;">

### ```api.PackageBase```
- base class for PackageObject and PackageInfoObject

### ```api.PackageDependencyObject```
- subclass of "api.PackageObject"
- represents a dependency for a given package

### ```markers.DEPENDENCY_ENVIRONMENT_MARKERS```
- holds respective values for each environment marker for the current system as per PEP 508

### What's changed?
<hr width=300 style="margin-left: 0;">

### ```api.PackageObject```
- converted from dataclass to callable object
- added ```dependencies``` and ```dependency_count``` properties
- added ```populate_dependencies()``` method
  - used to populate every dependency contained in a ```PackageObject``` instance
- accepts ***2*** new ```**kwargs```:
  - ```disregard_extras``` and ```disregard_markers```
  - see [PackageInfoObject](#packageinfoobject) for more on these

### ```api.PackageInfoObject```
- converted from dataclass to callable object
- accepts ***2*** new ```**kwargs```:
  - ```disregard_extras``` and ```disregard_markers```
    - boolean values used to tell the dependency parser whether or not to
    care about extras/markers when parsing a given package's dependencies.

## ```api.PackageVulnerabilitiesObject```
- ```fixed_in``` property now contains ```List[Version]``` instead of ```List[str]```

### ```packaging.version.Version```
- added ```fits_constraints()``` method
    - checks to see if a particular version fits within certain version constraints
    - i.e. 'Version("1.0.0").fits_constraints('(>=0.9.0, <1.1.0)')' will evaluate to 'True'

### What's gone?
<hr width=300 style="margin-left: 0;">

- ```api.get_release_full()```
- ```api.get_release_info()```
- ```api.get_package()```
- ```api.get_package_info()```
- ```api.download_dist()```
- ```exceptions.HashDigestMatchError```

<!-- The great CHANGELOG.md styling schism. -->

# 0.6.0

- [API] remove DeprecationWarning from otlet.packaging.version.LegacyVersion
        - since this is an indexing program, we need to retain LegacyVersion for properly searching/displaying package versions that do not conform to the PEP 440 standard
- [API] add otlet.packaging.version.etc for extra version-related operations
- [API] rename 'otlet.api.get_full()' to 'otlet.api.get_package()'
- [API] merge 'otlet.api.get_release_full()' functionality into 'otlet.api.get_package()'
- [API] deprecate 'otlet.api.get_release_full()', removal in 1.0.0
- [API] add function 'otlet.api.download_dist' for downloading package distribution files 
- [CLI] remove -gt and -lt
- [CLI] convert '--releases' to subcommand 'otlet releases':
        - add '--before-date' ('-bd'), '--after-date' ('-ad'), '--before-version' ('-bv'), and '--after-version' ('-av')
- [CLI] move CLI to dedicated submodule directory
        - move printers into dedicated module (otlet.cli.util)
        - seperate argparser into dedicated module (otlet.cli.options)
- [CLI] spice up version command
- [CLI] split up package positional argument into:
        - package
                - single argument positional for package name (i.e. 'otlet')
        - package_version
                - single argument OPTIONAL positional for package version (i.e. '0.6.0')
- [CLI] add subcommand 'otlet download':
        - download package distributions from the PyPI CDN

# 0.5.1

- [API] add packaging.version submodule into project (located at: 'otlet/packaging/version')
- [API] docs changes

# 0.5.0

- [CLI] add some color and bold text to warning/note labels
- [CLI] add items to CLI output
        - Documentation URL
        - Homepage URL
        - Maintainer
- [CLI] add --urls option
        - returns list of relevant URLs for given package
- [CLI] add extra info to --releases 
- [CLI] add '-lt' and '-gt' options for use with --releases
- [API] change PackageObject.info.version from `str` to `Union[packaging.version.Version, packaging.version.LegacyVersion]`
- [API] change PackageObject.releases from `Dict[str, URLReleaseObject]` to `Dict[Union[packaging.version.Version, packaging.version.LegacyVersion], URLReleaseObject]`
- [API] docs changes

# 0.4.0

- [API] add PackageVulnerabilitiesObject
- [CLI] add vulnerability warning if any are present for a given release
- [CLI] add --vulnerabilities option
        - returns paginated list of vulnerabilities, if any, for a given release
- [CLI] add --releases option
        - returns list of all available release versions
- [API] add documentation
- [API/CLI] rename modules
        - otlet.http -> otlet.api
        - otlet.otlet -> otlet.cli
- [API] fix Optional class params to store NoneType if blank str


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
