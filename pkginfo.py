import os
from os.path import isfile
import sys
import re

class Package:

    name: str
    category: str
    description: str
    size: int

    def __init__(self, name , cat, des, size):
        self.name = name
        self.category = cat
        self.description = des
        self.size = size

    def __str__(self) -> str:
        return f""" 
Package: {self.name}
Category: {self.category}
Description: {self.description}
Size in kilobytes: {self.size}
        """

    @staticmethod
    def parser(package_string: str):
        parser = package_string.split(',')
        return Package(parser[1], parser[0], parser[2], int(parser[3]))

class ArgumentCallBackException(Exception):
    pass

class NotFoundPackage(Exception):
    pass

class UnsupportArgument(Exception):
    pass

def exception_handler(exctype, value, traceback):
    if exctype == FileNotFoundError:
        print("File Not Found ! please provided sufficient file name")
    elif exctype == UnsupportArgument:
        print("Unsupported Argument")
    elif exctype == ArgumentCallBackException:
        print("Insufficient call back, please provide a function for each argument")
    else:
        sys.__excepthook__(exctype, value, traceback)

    exit(1)

def validate_file(file_name):
    if not isfile(file_name):
        raise FileNotFoundError("file not found")

def argument_builder(sys_args, arguments):
    sys_args.pop(0)

    result = {}

    for arg in arguments:

        if arg["option"] != sys_args[0]:
            continue

        result["option_name"] = arg["option_name"]

        arg_len = DEFAULT_ARG_LEN

        if arg["option_argument"]:
            arg_len += 1

        if(len(sys_args) < arg_len):
            print("Missing an argument")
            exit(1)

        if(len(sys_args) > arg_len):
            raise UnsupportArgument()

        result["option_argument"] = sys_args[1]

        if arg["file"]:
            file = sys_args[-1]
            validate_file(file)
            result["file"] = file

    if not result:
        raise UnsupportArgument()

    return result

def application_configuration():
    sys.excepthook = exception_handler

def list_all(file_name):
    result = ""

    if(os.path.getsize(file_name) == 0):
        print("No packages installed")
        exit(1)

    with open(file_name, "r") as file:
        for line in file:
            pkg = Package.parser(line)
            result += pkg.name + "\n"

    print("Installed packages:")
    print(result)


def calculate_total_pkg_size(file_name):
    total_pkg_size = 0

    if(os.path.getsize(file_name) == 0):
        print(f"Total size in kilobytes: {total_pkg_size}")
        exit(0)

    with open(file_name, "r") as file:
        for line in file:
            pkg = Package.parser(line)
            total_pkg_size += pkg.size

    print(f"Total size in kilobytes: {total_pkg_size}")

def verbose():
    print(r"""
Please use this option with fullscreen thank you
.___________.    ___       __            .__   __.   _______  __    __  ____    ____  _______ .__   __. 
|           |   /   \     |  |           |  \ |  |  /  _____||  |  |  | \   \  /   / |   ____||  \ |  | 
`---|  |----`  /  ^  \    |  |           |   \|  | |  |  __  |  |  |  |  \   \/   /  |  |__   |   \|  | 
    |  |      /  /_\  \   |  |           |  . `  | |  | |_ | |  |  |  |   \_    _/   |   __|  |  . `  | 
    |  |     /  _____  \  |  |     __    |  |\   | |  |__| | |  `--'  |     |  |     |  |____ |  |\   | 
    |__|    /__/     \__\ |__|    (__)   |__| \__|  \______|  \______/      |__|     |_______||__| \__| 
                                                                                                        
 _____  _____    ___  __  _____  ___________    ___ 
/ __  \|  ___|  /   |/  ||  _  ||___  /  _  |  /   |
`' / /'|___ \  / /| |`| || |/' |   / /| |_| | / /| |
  / /      \ \/ /_| | | ||  /| |  / / \____ |/ /_| |
./ /___/\__/ /\___  |_| |\ |_/ /./ /  .___/ /\___  |
\_____/\____/     |_/\___/\___/ \_/   \____/     |_/
                                                    

DINH NHAT TAI NGUYEN - 25410794
DATE OF COMPLETION: 16/Oct/2024
""")

def list_pkg_with_name(pkg_name, file_name):

    #TODO: this need to be a different error 
    if os.path.getsize(file_name) == 0:
        print("No installed package with this name")
        exit(1)

    pattern = re.compile(f"^[a-z_.]+,.*{pkg_name}.*,[-/a-zA-Z0-9.+_ ]+,[0-9]+$", re.IGNORECASE)
    print(pattern)
    matched_pkg = None

    with open(file_name, "r") as file:
        for item in file:
            matched_pkg = pattern.match(item)

    if not matched_pkg: 
        print("No installed package with this name")
        exit(1)

    print(Package.parser(matched_pkg.string))

if __name__ == "__main__":

    application_configuration()

    #TODO: Extend argument_builder to deal with syntax error scenario
    # args = argument_builder(sys.argv)
    DEFAULT_ARG_LEN = 2

    arguments = [{"option": "-l", "option_name":"list-pkg-with-name","option_argument": True, "file": True},
                 {"option": "-a", "option_name":"list-all","option_argument": False, "file": True},
                 {"option": "-v", "option_name":"verbose","option_argument": False, "file": True},
                 {"option": "-s", "option_name":"size","option_argument": False, "file": True}]

    arg = argument_builder(sys.argv, arguments)

    if arg["option_name"] == "list-pkg-with-name":
        list_pkg_with_name(arg["option_argument"], arg["file"])
    elif arg["option_name"] == "list-all":
        list_all(arg["file"])
    elif arg["option_name"] == "verbose":
        verbose()
    elif arg["option_name"] == "size":
        calculate_total_pkg_size(arg["file"])
    else:
        raise UnsupportArgument()

