class HauntedMansion(dict):
   
    def __init__(self, **kwargs):
        for key, val in kwargs.items(): 
            setattr(self, key, val)
            
    def __getattribute__(self, name):
        if(name[:len("spooky_")] == "spooky_"):
            spooky_name = name[len("spooky_"):]
            return object.__getattribute__(self, spooky_name)
        elif name[2:] == "__" and name[:len(name) - 3] == "__":
            return object.__getattribute__(self, name)
        else:
            return "Booooo, only ghosts here!"   