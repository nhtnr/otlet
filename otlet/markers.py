import os
import sys
import platform
from .packaging.version import parse

# 'implementation_version' impl as per PEP 508
def format_full_version(info):
    version = "{0.major}.{0.minor}.{0.micro}".format(info)
    kind = info.releaselevel
    if kind != "final":
        version += kind[0] + str(info.serial)
    return version


if hasattr(sys, "implementation"):
    IMPL_VER = format_full_version(sys.implementation.version)
else:
    IMPL_VER = "0"

DEPENDENCY_ENVIRONMENT_MARKERS = {
    "os_name": os.name,
    "sys_platform": sys.platform,
    "platform_machine": platform.machine(),
    "platform_python_implementation": platform.python_implementation(),
    "platform_release": platform.release(),
    "platform_system": platform.system(),
    "platform_version": platform.version(),
    "python_version": parse(".".join(platform.python_version_tuple()[:2])),
    "python_full_version": parse(platform.python_version()),
    "implementation_name": sys.implementation.name,
    "implementation_version": parse(IMPL_VER),
}
