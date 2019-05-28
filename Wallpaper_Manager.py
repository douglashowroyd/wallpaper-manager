'''To Do:
This will go in main program folder as exe. (need to find where specs.txt has to sit to be useable)

Need to set this to run on startup.

Need to add machine learning stuff in ML file then call func here.

Need to check it works again
'''
    

import ctypes
import os
import numpy as np
import tkinter as tk
import pandas as pd




# This picks a random picture in your specified folder + New, makes it the current wallpaper then 
#      moves it to the used folder
def Random_Wallpaper():
    with open('specs.txt', 'r') as file:
        specs = file.readlines()
    specs = [line[:-1] for line in specs]
    main_path = specs[0]
    old_wallpaper = specs[1]
    specs[2] = int(specs[2])
    
    # Load possible wallpapers and weights 
    df = pd.read_csv("wallpaper_data.csv")
    wallpapers = df.loc[df['New or Used'] == 0]
    wallpapers_list = wallpapers.loc[:, 'Names']
    weights = wallpapers.loc[:,'Weight']

    # Pick one with a suitable weight
    new_random_wallpaper = np.random.choice(wallpapers_list, 1, p=weights / sum(weights))
    new_wallpaper_path = os.path.join(main_path,'New',new_random_wallpaper[0])
    
    # Change Wallpaper
    ctypes.windll.user32.SystemParametersInfoW(20, 0, new_wallpaper_path, 3)

    # Update data for that wallpaper
    df.loc[df['Names'] == old_wallpaper, 'Rejected'] += 1
    df.loc[df['Names'] == new_random_wallpaper[0], 'New or Used'] = 1

    # Move wallpaper to Used folder and check if New folder is empty
    Move_Wallpaper(new_random_wallpaper[0])
    Check_empty_folder()
    
    # Save current wallpaper to text file for future reference and add 1 to count      
    specs[0] = specs[0] + '\n'
    specs[1] = new_random_wallpaper[0] + '\n'
    specs[2] += 1
    specs[2] = str(specs[2]) + '\n'
    
    with open('specs.txt', 'w') as file:
        file.writelines( specs )
        
    df.to_csv("wallpaper_data.csv")
    
    
    
    
# This just moves the file from the New folder to the Used folder
def Move_Wallpaper(wallpaper):
    old_name=os.path.join("New",wallpaper)
    new_name=os.path.join("Used",wallpaper)
    os.rename(old_name,new_name)

    
    
# This checks if the New folder is empty and if so moves all the used images back into the New folder and updates data
def Check_empty_folder():
    if len(os.listdir('New')) == 0:
        os.rename('New', 'New(1)')
        os.rename('Used', 'New')
        os.rename('New(1)', 'Used')
        df.loc[:, 'New or Used'] = 0
        
        
        
# This just updates the current wallpapers kept count
def Keep_Wallpaper():
    df = pd.read_csv("wallpaper_data.csv")
    with open('specs.txt', 'r') as file:
        specs = file.readlines()
    df.loc[df['Names'] == specs[1][:-1], 'Kept'] += 1
    df.to_csv("wallpaper_data.csv")
       
    
    
class Change_Wallpaper(tk.Frame):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_widgets()
        self.pack()

    def configure_gui(self):
        self.master.title("Wallpaper Picker")
        self.master.geometry("300x75")
        self.master.resizable(True, True)
        
    def create_widgets(self):
        self.message= tk.Label(self, text="Are you happy with  this wallpaper?")
        self.message.pack(side="top", fill="x")
        
        self.yes= tk.Button(self, text="Yes", command=self.keep)
        self.yes.pack(side="left")
        
        self.space=tk.Label(self)
        self.space.pack(side="left")
        
        self.no= tk.Button(self, text="No",command=self.change)
        self.no.pack(side="right")        
        
    def change(self):
        Random_Wallpaper()
        
    def keep(self):
        Keep_Wallpaper()
        root.destroy
        
        
        
if __name__ == '__main__':
    # Need to change this so user path is one from specs file and use chdir
    with open('specs.txt', 'r') as file:
        specs = file.readlines()
    specs = [line[:-1] for line in specs]
    main_path = specs[0]
    os.chdir(main_path)
    
    root = tk.Tk()
    change_wallpaper = Change_Wallpaper(root)
    root.mainloop()
    
    
    # Need to do ML stuff here
    if specs[2]%100 == 0:
        i=1 #do ML every 100 times