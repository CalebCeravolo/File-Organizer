import os
import shutil
import re
# Creates a trash folder at the location of this file
_location = os.path.expanduser("~")
trash = os.path.join(_location, "Trash")
try:
    os.mkdir(trash)
except FileExistsError:
    pass

test = _location[:3]
if ("\\" in test): delim = "\\"
else: delim = "/"

# Class for making a sorter to look through files. Initializes over the files and can be changed to a different set of files
class sorter:
    def __init__(self, path=None, pathto=None):
        self.path = path
        self.pathto = pathto
        self.files = os.listdir(path)
        self.match_num = len(self.files)
        self.index=0
        self.last_dir = path

    # Used for regex searching, returns all matches of the given regex pattern
    def regex(self, pattern):
        pat = re.compile(pattern)
        matches = []
        for file in self.files:
            result = pat.fullmatch(file)
            try:
                matches.append(result.group(0))
            except:
                pass
        return matches
    
    # Refreshes file databank, good to initialize once the target directory files have changed
    def update(self):
        self.files = os.listdir(self.path)
        if len(self.files)==0:
            self.move_back()
            self.files = os.listdir(self.path)
        self.match_num = len(self.files)
        if (abs(self.index)>=self.match_num):
            self.index=0
    
    # Returns 2*{number} of surrounding files to the current, aka {number} of files on each side up to the ends of the folder. 
    def surrounding_files(self, number):
        list = ""
        if (self.match_num):
            for i in range(self.index-min(number, int(self.match_num/2)),self.index+min(number, int(self.match_num/2)+1)):
                if (i>=self.match_num):
                    i-=self.match_num
                elif (i<=self.match_num*-1):
                    i+=self.match_num
                if (i==self.index):
                    list = f"{list}\n{self.files[i]} (current)"
                else: list = f"{list}\n{self.files[i]}"
            return list
    
    # Local helper function
    def ifin(self, string, ins):
        for word in ins:
            if (word in string):
                return True
        return False

    # Sets the source directory to the current file
    def move_into(self):
        file = self.full_path()
        if (os.path.isdir(file)):
            self.change_source(file)
        self.update()

    # Moves back a directory. Aka c:\Users\bob\Downloads would become c:\Users\bob
    def move_back(self):
        index=0
        if (self.path.endswith(delim)):
            self.path = self.path[:-1]
        for i, char in enumerate(self.path):
            if (char==delim): index = i
        last = self.path[index+1:]
        self.path=self.path[0:index+1]
        self.update()
        self.index=self.files.index(last)
    
    # Returns all the files in the current directory
    def get_children(self):
        return os.listdir(self.full_path())
    
    # Returns full path of the current file
    def full_path(self):
        return os.path.join(self.path, self.files[self.index])
    
    # Changes the source directory to the given new_path. new_path can be relative or full
    def change_source(self, new_path):
        self.last_dir = self.path
        if ("c:" in new_path.lower() or new_path.startswith(delim)):
            if (os.path.isdir(new_path)):
                self.path = f"{new_path}{delim}"
        else: 
            path = os.path.join(self.path, new_path)
            if (os.path.isdir(path)):
                self.path = f"{path}{delim}"
        
    # Changes the target directory to the given new_dest. new_dest can be relative or full
    def change_dest(self, new_dest):
        if ("c:" in new_dest.lower() or new_dest.startswith(delim)):
            if (os.path.isdir(new_dest)):
                self.pathto = new_dest
        else: 
            path = os.path.join(self.pathto, new_dest)
            if (os.path.isdir(path)):
                self.pathto = path

    # Prints current file to the terminal. Useful for debugging
    def printCurrent(self):
        file=self.files[self.index]
        print(f"File: {file}")

    # Returns current file name
    def getCurrent(self):
        return self.files[self.index]
    
    # Goes back an index
    def back(self):
        self.index-=1

    # Main function for operations on files
    def run(self, ans):
        file=os.path.join(self.path, self.files[self.index])
        if(self.ifin(ans, ["help", "Help"])):
            print("""____________________
open: Opens file
break: quits from program
moveto [dest]: moves file to dest if dest is within defined pathto")
newfolder [name]: creates new folder with name in pathto and places file there")
remove: deletes file
____________________""")
        if ("open" in ans):
            os.startfile(file)
        elif ("moveto" in ans):
            dest = ans[7:]
            if ("c:\\" in dest.lower() or dest.startswith(delim)):
                shutil.move(file, dest)
            else:
                shutil.move(file, os.path.join(self.pathto, dest))
        elif ("newfolder" in ans):
            folder_name = ans[10:]
            if ("c:\\" in folder_name):
                os.makedirs(folder_name)
                shutil.move(file, folder_name)
            else:
                folder_full = os.path.join(self.pathto, folder_name)
                os.makedirs(folder_full)
                shutil.move(file, folder_full)
        elif ("remove" in ans):
            shutil.move(file, trash) 
        else: self.index+=1
        if (abs(self.index)>=self.match_num):
            self.index = 0


    
# This can be used to run the organizer as command line input. Takes in arguments for the source and destination files
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Organizing script, loops through all files and prompts user for what to do")
    parser.add_argument("--source", type=str, default =_location , help="Where the organizer will look through")
    parser.add_argument("--pathto", type=str, default=_location, help="The destination for your sorted files")

    args = parser.parse_args()
    org = sorter(args.source, args.pathto)

    org.printCurrent()
    ans = input("What to do? ")
    org.run(ans)
    while ("break" not in ans):
        org.printCurrent()
        ans = input("What to do? ")
        org.run(ans)
    # for file in files:
    #     result = re.fullmatch(r".*[.]pdf", file)
    #     try:
    #         matches.append(result.group(0))
    #     except:
    #         pass
    # print(matches)
    # classes = ["371", "400", "233", "271"]



    # for file in files:
    #     result = re.search(r"\d{3}", file)
    #     try:
    #         dest = result.group(0)
    #         if(ifin(dest, classes)):
    #             shutil.move(file, os.path.join("Homework", dest))
    #             print(f"Moving {file} to {dest}")
    #     except:
    #         pass