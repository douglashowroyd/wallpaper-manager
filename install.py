
#ask for main path with warnings and all
#sort folder
#run random wallpaper once and record resulting image in txt file
#place wallpaper_manager file as exe in startup folder (google this)


#    To run on setup in general: (This just puts a bat file in startup folder saying run this script)
#    import getpass
#    USER_NAME = getpass.getuser()


#    def add_to_startup(file_path=""):
#        if file_path == "":
#            file_path = os.path.dirname(os.path.realpath(__file__))
#        bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
#        with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
#            bat_file.write(r'start "" %s' % file_path)
        
        
        
        
#        or set through start manager 
#        https://www.sevenforums.com/tutorials/67503-task-create-run-program-startup-log.html
        
        
        
#        need extra col in df to say if in new or old, then take weights in wm not as 1 but as weights from df over files in new
        
        
#Use installer to do this, need an exe file to run during installation to create spec file and run random wallpaper once         


import ctypes
import os
import Folder_Sorter as fs
import Wallpaper_Manager as wm


main_path = input("Where is your wallpaper folder?:",).replace("\\","\\\\")
#Add checks in here os.isdir

warning = ' '

print('Warning: this program will greatly modify the given folder.')
warning = input('If you would like to keep a copy please do so now. When ready to run the program please type: ready. If you would like to exit the program type: cancel',)

while warning != 'ready':
    if warning == 'cancel':
        print('Cancelling...')
        sys.exit()
    print('Command not recognised, please enter either ready or cancel\n')
    print('Warning: this program will greatly modify the given folder.')
    warning = input('If you would like to keep a copy please do so now then type: ready. If you would like to exit the program type: cancel',)


os.chdir(main_path)


# Sort the folder
fs.Move_Into_Temp()
fs.Temp_To_New()
fs.DataFrame_Populate()
fs.Check_Errors_Folder(main_path)

#Add functionality to dataframe_populate



open('specs.txt', 'a').close()

with open('specs.txt', 'r') as file:
    # read a list of lines into data
    specs = file.readlines()

#save path to folder, current wallpaper and number of different wallpapers seen
main_path = main_path.replace("\\\\","\\")
specs.append(main_path+'\n')

specs.append('\n')

specs.append(str(0)+'\n')


# and write everything back
with open('specs.txt', 'w') as file:
    file.writelines(specs)

    


    
#Just have to put run file in right place
    
    
    
    

# run random wallpaper once
wm.Random_Wallpaper()





