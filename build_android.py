import os
import subprocess
import argparse
import platform

archs = ["armv8", "armv7", "x86_64", "x86"]
configs = ["Debug", "Release"]

compiler = "clang"
compiler_version = "8"
cxx_stl = "libc++"
api_level = "21"
ndk_installer = "android-ndk/r20@magix/stable"

template = """[settings]
compiler=@compiler@
compiler.libcxx=@libcxx@
compiler.version=@version@
os=Android
os.api_level=@api_level@
arch=@arch@
os_build=@host@
arch_build=@host_arch@
build_type=@config@

[build_requires]
*: @ndk_installer@
"""


def host_architecture():
    return "x86_64" if platform.machine().endswith('64') else "x86"


def host_system_name():
    system_name = platform.system()
    if system_name == "Darwin":
        system_name = "Macos"
    return system_name


def prepare_template():
    host_system = host_system_name()
    template_host = template.replace("@host@", host_system) \
        .replace("@host_arch@", host_architecture()) \
        .replace("@ndk_installer@", ndk_installer) \
        .replace("@compiler@", compiler) \
        .replace("@version@", compiler_version) \
        .replace("@api_level@", api_level) \
        .replace("@libcxx@", cxx_stl)
    return template_host


def conan_command(from_source, force):
    command_list = ["conan", "create", ".", "magix/stable"]
    if not from_source:
        command_list.append("-k")
    if not force:
        command_list.append("--build=missing")
    command_list.append("-pr")
    return command_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Builds this package for Android')
    parser.add_argument("-s", "--source",
                        action="store_true", dest="source", default=False,
                        help="Retrieve source")
    parser.add_argument("-f", "--force",
                        action="store_true", dest="force", default=False,
                        help="Force rebuild")
    args = parser.parse_args()

    command = conan_command(args.source, args.force)

    temp = prepare_template()
    for config in configs:
        for arch in archs:
            profile = "%s-%s.tmp" % (arch, config)
            content = temp.replace("@arch@", arch).replace("@config@", config)
            f = open(profile, "a")
            f.write(content)
            f.close()
            cmd = command.copy()
            cmd.append(profile)
            output = subprocess.check_call(cmd)
            os.remove(profile)
