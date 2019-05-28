#Image to read image and get rgb values
#numpy as always
#KMeans to find clusters
#plt to plot for testing purposes
from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt



#returns an array, of size equal to the size of the image, with each element holding the rgb values of that pixel
def get_image_data(image_file):
    img = img_file.load()
    [xs, ys] = img_file.size
    img_array = [[0,0,0]]
    for x in range(0, xs):
            for y in range(0, ys):
                # (4)  Get the RGB color of the pixel
                [r, g, b, a] = img[x, y]
                img_array = np.append(img_array,[[r, g, b]], axis=0)
                
    img_array = np.float32(img_array.reshape(-1, 3))
    img_array = img_array[1:]
    return xs, ys, img_array


#returns a list of n_colours, sorted from most common to least common with percentages of each
def get_main_colours(num_colours, xs, ys, img_array):
    #run kmeans
    kmeans = KMeans(n_clusters=num_colours, random_state=0).fit(img_array)

    #a list of how many of each centre there are in the whole picture
    counts = np.unique(kmeans.labels_, return_counts=True)[1]
    
    #gives a list of centres with their counts, freq and percentages
    all_centres = []
    for i in range(num_colours):
        name = 'colour_'+ str(i)
        all_centres.append((name, kmeans.cluster_centers_[i], counts[i], counts[i]/(xs*ys), int(100*counts[i]/(xs*ys))))

    #sort previous list by most counts
    def takeCounts(elem):
        return elem[2]
    sorted_list = sorted(all_centres, reverse = True, key=takeCounts)
    
    return sorted_list

    
    

#a decent spread of colours to find
main_colours = {
    'Black' : (0,0,0),
    'White' : (255,255,255),
    'Red' : (255,0,0),
    'Lime' : (0,255,0),
    'Blue' : (0,0,255),
    'Yellow' : (255,255,0),
    'Cyan' : (0,255,255),
    'Magenta' : (255,0,255),
    'Silver' : (192,192,192),
    'Gray' : (128,128,128),
    'Maroon' : (128,0,0),
    'Olive' : (128,128,0),
    'Green' : (0,128,0),
    'Purple' : (128,0,128),
    'Teal' : (0,128,128),
    'Navy' : (0,0,128),
}

def find_dist(a,b):
    return np.linalg.norm(a-b)

#returns the name of the closest colour
def find_best_colour(colour):
    colo = np.array(colour)
    distances = [find_dist(colo, main_colours[main_colo]) for main_colo in main_colours]
    smallest_dist_index = distances.index(min(distances))
    return list(main_colours.keys())[smallest_dist_index]

#approximate each colour with one of the chosen standard colours           
def assign_best_colours(sorted_list):
    best_fit_colours = []
    for colour in sorted_list:
        best_fit_colours.append((find_best_colour(colour[1]), colour[3]))
    return best_fit_colours
    


if __name__ == "__main__":
    #test file
    image = 'lego.png'
    img_file = Image.open('C:\\Users\\Doug\\Dropbox\\' + image)
    n_colours = 5
    
    xs,ys,img_array = get_image_data(img_file)
    sorted_list = get_main_colours(n_colours, xs, ys, img_array)
    best_colours = assign_best_colours(sorted_list)

    