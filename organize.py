import os
import shutil
import re
_location = os.path.dirname(__file__)
trash = os.path.join(_location, "trash")
try:
    os.mkdir(trash)
except FileExistsError:
    pass

test = _location[:3]
if ("\\" in test): delim = "\\"
else: delim = "/"
class sorter:
    def __init__(self, path=None, pathto=None):
        self.path = path
        self.pathto = pathto
        self.files = os.listdir(path)
        self.match_num = len(self.files)
        self.index=0
        self.last_dir = path
        
    # def __init__(self):
    #     self.path = "C:\\Users\\caleb\\Downloads"
    #     self.pathto = "C:\\Users\\caleb\\Downloads\\Homework"
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
    # print(matches)
    def update(self):
        self.files = os.listdir(self.path)
        self.match_num = len(self.files)
        if (abs(self.index)>=self.match_num):
            self.index=0
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
    def ifin(self, string, ins):
        for word in ins:
            if (word in string):
                return True
        return False
    def move_into(self):
        file = self.full_path()
        if (os.path.isdir(file)):
            self.change_source(file)
        self.update()
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
    def get_children(self):
        return os.listdir(self.full_path())
    def full_path(self):
        return os.path.join(self.path, self.files[self.index])
    def change_source(self, new_path):
        self.last_dir = self.path
        if ("c:" in new_path.lower() or new_path.startswith(delim)):
            if (os.path.isdir(new_path)):
                self.path = f"{new_path}{delim}"
        else: 
            path = os.path.join(self.path, new_path)
            if (os.path.isdir(path)):
                self.path = f"{path}{delim}"
        

    def change_dest(self, new_dest):
        if ("c:" in new_dest.lower() or new_dest.startswith(delim)):
            if (os.path.isdir(new_dest)):
                self.pathto = new_dest
        else: 
            path = os.path.join(self.pathto, new_dest)
            if (os.path.isdir(path)):
                self.pathto = path
    def printCurrent(self):
        file=self.files[self.index]
        print(f"File: {file}")
    def getCurrent(self):
        return self.files[self.index]
    def back(self):
        self.index-=1
    def run(self, ans):
        file=os.path.join(self.path, self.files[self.index])
        if(self.ifin(ans, ["help", "Help"])):
            print("____________________\n")
            print("open: Opens file \nbreak: quits from program\nmoveto [dest]: moves file to dest if dest is within defined pathto")
            print("newfolder [name]: creates new folder with name in pathto and places file there")
            print("remove: deletes file")
            print("____________________\n")
        if ("open" in ans):
            os.startfile(file)
        elif ("moveto" in ans):
            dest = ans[7:]
            if ("c:\\" in dest.lower() or dest.startswith(delim)):
                shutil.move(file, dest)
            else:
                shutil.move(file, os.path.join(self.pathto, dest))
            self.update()
        elif ("newfolder" in ans):
            folder_name = ans[10:]
            if ("c:\\" in folder_name):
                os.makedirs(folder_name)
                shutil.move(file, folder_name)
            else:
                folder_full = os.path.join(self.pathto, folder_name)
                os.makedirs(folder_full)
                shutil.move(file, folder_full)
            self.update()
        elif ("remove" in ans):
            shutil.move(file, trash) 
            self.update()
        else: self.index+=1
        if (abs(self.index)>=self.match_num):
            self.index = 0


    

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Organizing script, loops through all files and prompts user\n for what to do")
    parser.add_argument("--source", type=str, default ="C:\\Users\\caleb\\Downloads" , help="Where the organizer will look through")
    parser.add_argument("--pathto", type=str, default="C:\\Users\\caleb\\Downloads\\Homework", help="The destination for your sorted files")

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