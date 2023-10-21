try:
    import requests
except ImportError:
    print("Please install the requests module.")
    exit()
import json
#from pprint import pprint

url = "https://raw.githubusercontent.com/MaximumADHD/Roblox-Client-Tracker/roblox/API-Dump.json"
r = requests.get(url)
data = r.json()

Version = data["Version"]
Classes = data["Classes"]
Enums = data["Enums"]

def render(creator):
    file = creator.FileStart.format(Version=Version)
    
    ### ENUMS ###
    file += creator.Section.format(Name="Enums")
    file += creator.EnumSection
    for i in Enums:
        Name = i["Name"]
        Data = i["Items"]
        
        file += creator.EnumCore.format(Name=Name)
        for item in Data:
            line = creator.EnumItem.format(Name=item["Name"], Value=item["Value"])
            if creator.EnumVerify(creator, item["Name"], item["Value"]) != None:
                line = creator.EnumVerify(creator, item["Name"], item["Value"])
            file += line
        file += creator.EnumCoreEnd.format(Name=Name)
        
    file += creator.EnumEnd.format(Name="Enums")
    
    ### CLASSES ###
    file += creator.Section.format(Name="Classes")
    file += creator.ClassSection
    classCache = []
    
    for Class in Classes:
        for classitem in Class['Members']:
            Name = classitem["Name"]
            
            if Name in classCache:
                continue
            else:
                classCache.append(Name)
                
            file += creator.ClassCore.format(Name=Name)
            for name, val in enumerate(classitem):
                if isinstance(val, dict):
                    file += creator.ClassCore.format(Name=name)
                    for subname, subval in val:
                        line = creator.ClassProperty.format(Name=subname, Value=subval)
                        file += line
                else:
                    line = creator.ClassProperty.format(Name=val, Value=name)
                    file += line
            file += creator.ClassCoreEnd.format(Name=Name)
    file += creator.ClassEnd.format(Name="Classes")
    

    return file

class Creator: # Python Example
    Section = """\n#### {Name} ####\n"""
    FileStart = """# Auto-Generated by RCC Bindings Engine\n# Dump Version: {Version}\n\n"""
    
    ### ENUMS ###
    EnumSection = """Enum = {\n"""
    EnumCore = """\t"{Name}": {{\n"""
    EnumItem = """\t\t"{Name}": {Value},\n"""
    EnumCoreEnd = """\t}},\n"""
    EnumEnd = """}}"""
    
    def EnumVerify(self, Name, Value):
        """ Verifies that the Enum is valid, if not fix and return the fixed Enum. """
        pass
    
    ### CLASSES ###
    ClassSection = """"""
    ClassCore = """type {Name} = {{\n"""
    ClassProperty = """\t{Name} = {Value}\n"""
    ClassCoreEnd = """}}\n"""
    ClassEnd = """"""
    
def main():
    file = render(Creator)
    print(file)
        
if __name__ == "__main__":
    main()