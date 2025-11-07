import os
import shutil
import re
# Creates a trash folder at the location of this file
_location = os.getcwd()
test = _location[:3]
if ("\\" in test): delim = "\\"
else: delim = "/"

def rewrite(file, content):
    with open(file, "w") as f:
        f.write(content)
# Class for making a sorter to look through files. Initializes over the files and can be changed to a different set of files
class sorter:
    def __init__(self, path=None, pathto=None, files=None, trash=None):
        self.path = path
        self.pathto = pathto
        if (files!=None):
            self.files = files
        else:
            self.files = os.listdir(path)
        self.match_num = len(self.files)
        self.index=0
        self.last_dir = path
        self.trash=trash
        if (self.trash==None):
            self.trash = os.path.join(_location, "Trash")
            try:
                os.mkdir(self.trash)
            except FileExistsError:
                pass
        
    def search(self, pattern, recurse):
        if ("--avoid" in pattern):
            ind = pattern.find("--avoid")
            ind2=ind+len("--avoid")+1
            npattern = pattern[ind2:]
            pattern=pattern[:ind-1]
            npat=re.compile(npattern)
        else: npat = None
        pat = re.compile(pattern)
        matches = []
        for file in self.files:
            if (npat==None or not npat.fullmatch(file)):
                if (not delim in file):
                    file = os.path.join(self.path, file)
                if (os.path.isfile(file)):
                    try:
                        with open(file, "r") as f:
                            content = f.read()
                            if (pat.search(content)):
                                matches.append(file)
                    except: pass
                elif (os.path.isdir(file) and recurse):
                    self.__search(pat, matches, file, npat)
        return matches
    def __search(self, pat, matches, dir,npat):
        try:
            files = os.listdir(dir)
        except PermissionError:
            return False
        else:
            for file in files:
                if (npat==None or not npat.fullmatch(file)):
                    if (not delim in file):
                        file = os.path.join(dir, file)
                    if (os.path.isfile(file)):
                        try:
                            with open(file, "r") as f:
                                content = f.read()
                                if (pat.search(content)):
                                    matches.append(file)
                        except: pass
                    elif (os.path.isdir(file)):
                        self.__search(pat, matches, file)
    # Used for regex searching, returns all matches of the given regex pattern
    def regex(self, pattern, recurse):
        if ("--avoid" in pattern):
            ind = pattern.find("--avoid")
            ind2=ind+len("--avoid")+1
            npattern = pattern[ind2:]
            pattern=pattern[:ind-1]
            npat=re.compile(npattern)
        else: npat = None
        pat = re.compile(pattern)
        
        matches = []
        for file in self.files:
            if ((npat==None) or (not npat.fullmatch(file))):
                # if (delim in file):
                #     rev_file = file[::-1]
                #     ind1 = rev_file.find(delim)
                #     file_search = file[-1*ind1:]
                # else: file_search=file
                if (recurse):
                    if (self.path==None):
                        full = file
                    else:
                        full = os.path.join(self.path,file)
                    
                    if (os.path.isdir(full)):
                        self.__regex(pat, npat, full, matches)
                if(pat.fullmatch(file)):
                    if (self.path!=None):
                        name = os.path.join(self.path, file)
                    else: name = file
                    matches.append(name)
        return matches
    def __regex(self, pat, npat, dir, matches):
        try:
            files = os.listdir(dir)
        except PermissionError:
            return False
        else:
            for file in files:
                if ((npat==None) or (not npat.fullmatch(file))):
                    # if (delim in file):
                    #     rev_file = file[::-1]
                    #     ind1 = rev_file.find(delim)
                    #     file_search = file[:-1*ind1]
                    # else: file_search=file
                    full = os.path.join(dir,file)
                    if (os.path.isdir(full)):
                        self.__regex(pat, npat, full, matches)
                    
                    if(pat.fullmatch(file)):
                        if (self.path!=None):
                            name = os.path.join(dir, file)
                        else: name = file
                        matches.append(name)

    # Refreshes file databank, should be ran once the target directory files have changed
    def update(self):
        if (self.path==None):
            for file in self.files:
                if (not (os.path.isfile(file) or os.path.isdir(file))):
                    self.files.remove(file)
            if len(self.files)==0:
                self.files.append("No more files")
            self.match_num = len(self.files)
            if (abs(self.index)>=self.match_num):
                self.index=0
        else:
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
    
    def find(self, pattern, recurse):
        if ("--avoid" in pattern):
            ind = pattern.find("--avoid")
            ind2=ind+len("--avoid")+1
            npattern = pattern[ind2:]
            pattern=pattern[:ind-1]
            npat=re.compile(npattern)
        else: npat = None
        pat = re.compile(pattern)
        for file in self.files:
            if ((npat==None) or (not npat.fullmatch(file))):
                if (recurse):
                    if (self.path==None):
                        full = file
                    else:
                        full = os.path.join(self.path,file)
                    if (os.path.isdir(full)):
                        if (self.__find(pat, npat, full)):
                            break
                if (pat.fullmatch(file)):
                    match = file
                    self.index=self.files.index(match)
                    break
    def __find(self, pat, npat,full_path):
        try:
            files = os.listdir(full_path)
        except PermissionError:
            return False
        else:
            for file in files:
                if ((npat==None) or (not npat.fullmatch(file))):
                    full = os.path.join(full_path,file)
                    if (os.path.isdir(full)):
                        if(self.__find(pat, npat, full)):
                            return True
                    if (pat.fullmatch(file)):
                        match = file
                        self.change_source(full_path)
                        self.update()
                        self.index=self.files.index(match)
                        return True
            return False
    def save_current(self, content):
        rewrite(self.full_path(), content[:-1])
    def new_file(self, name):
        j=1
        ts=name[::-1]
        ind = ts.find(".")
        ext=".txt"
        if (ind!=-1):
            ext = name[-1*ind-1:]
            name=name[:-1*ind-1]
        if (len(name)==0):
            name="New"
        if (not self.path==None):   
            name = os.path.join(self.path, name)
        else:
            name = os.path.join(self.pathto, name)

        if (os.path.isfile(f"{name}{ext}")):
            while (os.path.isfile(f"{name}({j}){ext}")):
                j+=1
            name = f"{name}({j})"
        name = f"{name}{ext}"
        # if (not("c:" in name.lower() or name.startswith(delim))):
        #     if (os.path==None):
        #         name = os.path.join(self.pathto,name)
        #     else: 
        #         name = os.path.join(self.path,name)
        open(name, "x")
        if (self.path==None):
            self.files.insert(self.index, name)
            self.update()
        else:
            self.update()
            ind = (name[::-1]).index(delim)
            self.index=self.files.index(name[-1*ind:])
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
        path = self.full_path()
        if (os.path.isdir(path)):
            return os.listdir(path)
        else: return []
    
    # Returns full path of the current file
    def full_path(self):
        if (self.path==None): return self.files[self.index]
        else: return os.path.join(self.path, self.files[self.index])
    
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
    def change_trash(self, trash_dest):
        if ("c:" in trash_dest.lower() or trash_dest.startswith(delim)):
            if (not os.path.isdir(trash_dest)):
                os.makedirs(trash_dest)
            
        else: 
            trash_dest = os.path.join(_location, trash_dest)
            if (not os.path.isdir(trash_dest)):
                os.makedirs(trash_dest)
        files = os.listdir(self.trash)
        for file in files:
            file = os.path.join(self.trash, file)
            shutil.move(file, trash_dest)
        os.remove(self.trash)
        self.trash = trash_dest
    # Prints current file to the terminal. Useful for debugging
    def printCurrent(self):
        file=self.files[self.index]
        print(f"File: {file}")

    # Returns current file name
    def getCurrent(self):
        return self.files[self.index]
    def open(self):
        file=self.full_path()
        if os.path.isdir(file) or os.path.isfile(file):
            os.startfile(file)
    def moveto(self, dest):
        file=self.full_path()
        if (not ("c:\\" in dest.lower() or dest.startswith(delim))):
            dest=os.path.join(self.pathto, dest)
        if (not os.path.isdir(dest)):
            if ("." not in dest and not os.path.isdir(file)):
                rev = file[::-1]
                ind = rev.find(".")
                ext = file[-1*ind-1:]
                dest = f"{dest}{ext}"
        shutil.move(file, dest)

    def newfolder(self, folder_name):
        file=self.full_path()
        if ("c:\\" in folder_name):
            os.makedirs(folder_name)
            shutil.move(file, folder_name)
        else:
            folder_full = os.path.join(self.pathto, folder_name)
            os.makedirs(folder_full)
            shutil.move(file, folder_full)
    def delete(self):
        file=self.full_path()
        shutil.move(file, self.trash) 
    # Goes back an index
    def back(self):
        self.index-=1
        # if (abs(self.index)>=self.match_num):
        #     self.index = 0
    def next(self):
        self.index+=1
        # if (abs(self.index)>=self.match_num):
        #     self.index = 0
    # Main function for operations on files
    if __name__=="__main__":
        def run(self, ans):
            if (self.path!=None):
                file=os.path.join(self.path, self.files[self.index])
            else: file = self.files[self.index]
            if(self.ifin(ans, ["help", "Help"])):
                print("""____________________
    open: Opens file
    break: quits from program
    moveto [dest]: moves file to dest if dest is within defined pathto")
    newfolder [name]: creates new folder with name in pathto and places file there")
    remove: deletes file
    ____________________""")
            if ("open" in ans):
                self.open()
            elif ("moveto" in ans):
                dest = ans[7:]
                self.moveto(dest)
            elif ("newfolder" in ans):
                folder_name = ans[10:]
                self.newfolder(folder_name)
            elif ("remove" in ans):
                shutil.move(file, self.trash) 
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