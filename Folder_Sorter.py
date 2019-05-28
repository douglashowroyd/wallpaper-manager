'''
Need to run this on first set up. Or another file calling this one.

Can't assume cd'ed into wallpaper folder either
'''




import os
import pandas as pd
import shutil




def Move_Into_Temp():
    '''Makes an empty temp folder, 
            moves the old temp folder to a new one if such a folder exists 
            then moves all folders into temp folder'''
    folder_dir = os.listdir()
    if 'Temp' in folder_dir:
        new_temp='Temp'
        count = 0
        while new_temp in folder_dir:
            count += 1
            new_temp = 'Temp-%d' % (count,) 
        os.mkdir(new_temp)
        folder_dir.append(new_temp)
        folder_dir.remove('Temp')
        for file in os.listdir('Temp'):
            shutil.move(os.path.join('Temp',file),os.path.join(new_temp,file))
            print('Moving %s from Temp folder to' % (file,), new_temp)
    else:
        os.mkdir('Temp')
    
    # move all files in path to temp folder
    for file in folder_dir:
        shutil.move(file, os.path.join('Temp',file))
        print('Moving %s to Temp folder' % (file,))

    
    


def Temp_To_New():
    '''Move all files to New folder from temp folder'''
    
    print('Creating New folder')
    os.mkdir('New')
    print('Creating Used folder')
    os.mkdir('Used')
    print('Creating Errors folder')    
    os.mkdir('Errors')


    # take list of all files and directories in temp
    folder_dir = os.listdir('Temp')
    
    while len(folder_dir)>0:
    
        root, dirs, files = next(os.walk('Temp'))
        
        
        # first deal with loose files
        for file in files:
            head = file.split(".")[0]
            tail = file.split(".")[-1]
    
     
            # if not a picture move to error file and we will deal with it later
            if tail not in ['pjpeg', 'gif', 'bmp','jpg','jpeg','png']:
                #move to main folder first to avoid bad interactions
                shutil.move(os.path.join('Temp',file),file)
                dst_file = os.path.join('Errors', file)
                tail = '.' + tail
                # now check no name overlaps
                count = 0
                while os.path.exists(dst_file):
                    count += 1
                    dst_file = os.path.join('Errors', '%s-%d%s' % (head, count, tail))
                print('Renaming %s to %s' % (file, dst_file))
                shutil.move(file, dst_file)
                continue

    
    
            # now check no name overlaps then move to New folder   
            shutil.move(os.path.join('Temp',file),file)
            
            dst_file = os.path.join('New', file)
            tail = '.' + tail
            # rename if necessary
            count = 0
            while os.path.exists(dst_file):
                count += 1
                dst_file = os.path.join('New', '%s-%d%s' % (head, count, tail))
            print('Renaming %s to %s' % (file, dst_file))
            shutil.move(file, dst_file)     

    
      
        # takes all objects in all folders in temp and moves them into temp themselves, then deletes the empty folders
        for folder_name in dirs:
            second_path = os.path.join('Temp', folder_name)
            
            second_root, second_dirs, second_files = next(os.walk(second_path))
            
            # move files from folder_name to temp, renaming where needed
            for file in second_files:
                head = file.split(".")[0]
                tail = '.' + file.split(".")[-1]
                
                # now check no name overlaps
                shutil.move(os.path.join('Temp',folder_name,file), file)
                dst_file = os.path.join('Temp', file)
                count = 0
                while os.path.exists(dst_file):
                    count += 1
                    dst_file = os.path.join('Temp', '%s-%d%s' % (head, count, tail))
                print('Renaming %s to %s' % (file, dst_file))
                shutil.move(file, dst_file)
                
                
                
            # move folders to temp folder
            for folder in second_dirs:
                # first move to main folder
                if folder == 'New':
                    shutil.move(os.path.join('Temp',folder_name,folder),'New-1')
                    folder = 'New-1'
                elif folder == 'Temp':
                    shutil.move(os.path.join('Temp',folder_name,folder),'Temp-1')
                    folder = 'Temp-1'
                elif folder == 'Used':
                    shutil.move(os.path.join('temp',folder_name,folder),'Used-1')
                    folder = 'Used-1'
                elif folder == 'Errors':
                    shutil.move(os.path.join('Temp',folder_name,folder),'Errors-1')
                    folder = 'Errors-1'
                else:
                    shutil.move(os.path.join('Temp',folder_name,folder),folder)
                
                # now check no name overlaps
                dst_dir = os.path.join('Temp', folder)
                count = 0
                while os.path.exists(dst_dir):
                    count += 1
                    dst_dir = os.path.join('Temp', '%s-%d' % (folder, count))
                print('Renaming %s to %s' % (folder, dst_dir))
                shutil.move(folder, dst_dir)
                
                
            os.rmdir(os.path.join('Temp',folder_name))
            
        # recheck temp folder
        folder_dir = os.listdir('Temp')
        
    
    shutil.rmtree('Temp')
     



        

    
    
def DataFrame_Populate():
    '''start data frame of all images'''
    data = []
    df = pd.DataFrame(data, columns = ['Names','Extension','Kept','Rejected','Total Score','New or Used', 'Weight'])
    
    
    newdir_list = os.listdir('New')
    
    
    for file in newdir_list:
        head = file.split(".")[0]
        tail = file.split(".")[-1]
            
        # add file and etension to dataframe
        df2 = pd.DataFrame([[file,tail,0,0,0,0,1/len(newdir_list)]], columns=['Names','Extension','Kept','Rejected','Total Score','New or Used','Weight'])
        df=df.append(df2, ignore_index=True, sort = True)
    

    cols = ['Names','Extension','Kept','Rejected','Total Score','New or Used','Weight']
    df = df[cols]
    print(df.head())
    df.to_csv('wallpaper_data.csv')
    print('A list of all your wallpapers can be found in your wallpaper folder as a .csv file')
        
        
    # need to analyse each pic at the end for rgb values
    
    
    
    
    
    
    
def Check_Errors_Folder(main_path):
    '''Informs user about the number of errors or delete folder if empty'''
    no_of_errors = len(os.listdir('Errors'))
    if  no_of_errors == 1:
        print("There was 1 incompatible file.")
        print("It can be found in", os.path.join(main_path,'Errors'))
        print("If you would like to use this file as a wallpaper, please convert it to a valid format and rerun this program.")

    elif no_of_errors > 1:
        print("There were ", no_of_errors," incompatible files.")
        print("They can be found in", os.path.join(main_path,'Errors'))
        print("If you would like to use any of those files as wallpapers, please convert them to a valid format and rerun this program.")
    else:
        shutil.rmtree('Errors')

        
        
        
        
        