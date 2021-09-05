'''
created on Fri 09/03/2021

@author : Julien

to create `.csv` files to use this code, please get a look at :
https://github.com/Elektriman/fractal_curves
'''

#  _____                            _
# |_   _|                          | |
#   | |  _ __ ___  _ __   ___  _ __| |_ ___
#   | | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
#  _| |_| | | | | | |_) | (_) | |  | |_\__ \
# |_____|_| |_| |_| .__/ \___/|_|   \__|___/
#                 | |
#                 |_|

from manim import *
import csv
import os
import re


#  __  __       _
# |  \/  |     (_)
# | \  / | __ _ _ _ __    ___  ___ ___ _ __   ___
# | |\/| |/ _` | | '_ \  / __|/ __/ _ \ '_ \ / _ \
# | |  | | (_| | | | | | \__ \ (_|  __/ | | |  __/
# |_|  |_|\__,_|_|_| |_| |___/\___\___|_| |_|\___|

class curve(Scene):

    def construct(self):

        #recovering data from csv files (must be pasted in a folder named "fractals_tabs")
        print('recovering data')
        data = dict_to_lists(recover_points("dragon_curve"), k=4.5)

        #creating the Line objects
        print('creating curves')
        curves_list = [] #list of Line mobjects
        N = 10 #number of maximum order of the curve to display
        n = min(len(data), N)
        for Points in data[:N] :
            curves_list.append(create_curve(Points))
            print("curve created ", len(curves_list), "/", n)
            curves_list[-1].set_stroke(width=7/np.log(len(Points)))

        #applying an offset to center the curve on the screen
        #this allow the animation to be centered on the last computed curve
        for c in curves_list :
            c.set_x(c.get_x() - curves_list[n - 1].get_x())
            c.set_y(c.get_y() - curves_list[n - 1].get_y())

        #animate the curves
        print('animating')
        for c in curves_list :
            self.play(Transform(curves_list[0],c)) #transforming the first mobject into each one of the curves_list mobject


#  ______                _   _
# |  ____|              | | (_)
# | |__ _   _ _ __   ___| |_ _  ___  _ __  ___
# |  __| | | | '_ \ / __| __| |/ _ \| '_ \/ __|
# | |  | |_| | | | | (__| |_| | (_) | | | \__ \
# |_|   \__,_|_| |_|\___|\__|_|\___/|_| |_|___/

def recover_points(fname):
    '''
    this function recovers the points stored as csv files

    Parameters
    ------------
    fname : string
        the name of the fractal to recover the points from. It must be formatted as follows :
        "name_of_curve" for the folder,
        "name_of_curve_n.csv" for the csv file with n the order of the fractal curve developpement

    Returns
    ------------
    fdict : dict{string : list[[string, string]]}
        The dictionnary associating the files with their raw string-like data
        structure : dict{file_name : list[[x_coordinate, y_coordinate]]}
    '''
    #recovering the path to the csv files directory
    directory = os.path.dirname(__file__)
    directory = os.path.join(directory, f"fractals_tabs\{fname}")

    fdict = {}
    for file in os.listdir(directory): #iterating over the files
        f = os.path.join(directory, file)
        if os.path.isfile(f): #making sure we don't look at directories
            with open(f, 'r') as csvtab :
                try :
                    R = csv.reader(csvtab, delimiter=',', lineterminator='\r') #initiating a csv reader

                    #turning the csv data into a list
                    L = []
                    for row in R :
                        L.append(row)

                    fdict[os.path.split(f)[1]]=L # appending the list into the dictionnary with the proper key
                except Exception as e :
                    #in case a non-csv file was in the directory
                    raise e

    print('points recovered')
    return fdict

def dict_to_lists(fdict, k=1):
    '''
    This function transforms the raw data into a proper list of plottable data

    Parameters
    ------------
    fdict : dict{string : list[[string, string]]}
        the dictionnary of the raw data values

    Returns
    ------------
    res list[list[float, float, float]]
        the nested list for all data related to the curve
        structure : all_curves[curve_of_order_i[x, y, z]]
    '''

    res = [None]*len(fdict.keys()) #initialising the result list

    for file, data in fdict.items() : #going through the dictionnary
        #use of regular expressions to recover the order of the function
        s = re.search('.*_(\d+).csv', file)
        i = int(s.groups(0)[0])
        #this together with the non-empty result list initialisation is needed because the data saved in the dictionnary is not ordered

        #transtyping the raw string data into the actual float data, and addition of the null z componant
        for j in range(len(data)):
            data[j] = list(map(lambda x:float(x)*k, data[j]))
            data[j].append(0.0)


        res[i] = data # appending the data list into its correct place into the super list
        # (ordered following the fractal construction algorithm steps)

    print('list finished')
    return res

def create_curve(Points):
    '''
    Creates the Line mobject composed of all the points in "Points".

    Parameters
    ------------
    Points : list[[float, float, float]]
        list of the points of the future line

    Returns
    ------------
    l : manim.mobject.geometry.Line
        a "Line" mobject with all the points from "Points" appended to it
    '''

    l = Line(Points[0],Points[1]) #create the first Line of the first vertice
    for i in range(1, len(Points)-1):
        l.append_points(Line(Points[i],Points[i+1]).get_points()) #add the line of each next vertices
    return l