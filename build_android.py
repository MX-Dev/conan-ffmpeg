import os
import subprocess
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Builds this package for Android')
    parser.add_argument("-s", "--source",
                        action="store_true", dest="source", default=False,
                        help="Retrieve source")
    parser.add_argument("-f", "--force",
                        action="store_true", dest="force", default=False,
                        help="Force rebuild")
    args = parser.parse_args()
    profile_dir = os.path.join(os.getcwd(), "profiles")
    profile_ext = ".profile"
    for file in os.listdir(profile_dir):
        if file.endswith(profile_ext):
            profile_path = os.path.join(profile_dir, file)
            command = ["conan", "create", ".", "magix/stable", "-pr", profile_path]
            if not args.source:
                command.append("-k")
            if not args.force:
                command.append("--build=missing")
            output = subprocess.check_call(command)
