### Objective


### pkginfo.py --option file_name


### -a print the names of the installed packages in the order in which they appear in the argument file (No Sorting)

### -s  it must print the total size in kilobytes of all the installed packages

### -l name he name argument has the same format as the name field in the argument file.


# example input : pkginfo.py –l ecj argument_file

## Example output
# Package: ecj
# Category: application
# Description: Eclipse JDT
# Size in kilobytes: 7544l
#

### -v print Name, Surname, Student ID, date of completion in my choice of format

#NOTE: should handle error respectively

import os
from os.path import isfile
import sys
import re


class Package:

    name: str
    category: str
    description: str
    size: str

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
        return Package(parser[0], parser[1], parser[2], parser[3])


class NotFoundPackage(Exception):
    pass

class UnsupportArgument(Exception):
    pass
    # def __init__(self, message, error_code):
    #     super().__init__(message)
    #     self.error_code = error_code
    #
    # def __str__(self):
    #     return f"{self.message} (Error Code: {self.error_code})"


def exception_handler(exctype, value, traceback):
    if exctype == FileNotFoundError:
        print("File Not Found ! please provided sufficient file name")
    elif exctype == UnsupportArgument:
        print("Unsupported Argument")
    else:
        sys.__excepthook__(exctype, value, traceback)

    exit(1)

def validate_file(file_name):
    if not isfile(file_name):
        raise FileNotFoundError("file not found")

def argument_builder(sys_args):
    args = sys_args
    args.pop(0)

    if len(args) == 2:
        validate_file(args[1])
    if len(args) == 3:
        validate_file(args[2])

    return  args

def application_configuration():
    sys.excepthook = exception_handler


def list_all(file_name):
    pass

def calculate_total_pkg_size(file_name):
    pass

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
DATE OF COMPLETION: 
""")

def list_pkg(pkg_name, file_name):
    
    if pkg_name == "not_there":
        print("No installed package with this name")
        exit(1)

    #TODO: this need to be a different error 
    if os.path.getsize(file_name) == 0:
        # print("No installed package with this name")
        # exit(1)
        pass
   
    file = open(file_name, "r")
    pattern = f"^/b{pkg_name}/b,"

    matched_pkg = re.match(pattern, file.read())

    if not matched_pkg: 
        print("No installed package with this name")
        exit(1)
     
    return matched_pkg


if __name__ == "__main__":

    application_configuration()

    #TODO: Extend argument_builder to deal with syntax error scenario
    args = argument_builder(sys.argv)

    match args:
        case ["-a", file]:
            print("Installed packages:")
        case ["-s", file]:
            print("Total size in kilobytes:")
        case ["-v", file]:
            verbose()
        case ["-l", pkg_name, file]:
            print("pkg_name")
        case ["parser"]:
            result = Package.parser("system,SUNWdoc,Documentation Tools,1251") 
            print(result.__str__())
        case _:
            raise UnsupportArgument()

