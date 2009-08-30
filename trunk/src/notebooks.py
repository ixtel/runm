# coding=UTF-8

import csv
import re
import random
import math

class Notebook:
   pass

def getFloat(regex, raw):
    m = re.search(regex, raw).groups()
    return float(m[0] + '.' + m[1])

def getInt(regex, raw):
    m = re.search(regex, raw).groups()
    return int(m[0])

def create_notebook(raw):
    try:
        notebook = Notebook()
        notebook.vendor = raw[0].split(' ')[0]
        notebook.model = raw[0].split(' ')[1]
        notebook.cpu = getFloat(r"(\d+)\,(\d+)\s\Г", raw[0].split('/')[0])
        notebook.monitor = getFloat(r"(\d+)\.(\d+)\''", raw[0].split('/')[1])
        notebook.ram = getInt(r"(\d+)\Mb", raw[0].split('/')[2])
        notebook.hdd = getInt(r"(\d+)Gb", raw[0].split('/')[3])
        notebook.video = getInt(r"(\d+)Mb", raw[0].split('/')[4])
        notebook.price = getInt(r"(\d+)\s\руб.", raw[1])
        return notebook
    except Exception, e:
        return None
     

def get_notebooks():
    reader = csv.reader(open('data.csv'), delimiter=';', quotechar='|')
    return filter(lambda x: x != None, map(create_notebook, reader))

def normalized_set_of_notebooks():
    notebooks = get_notebooks()
    cpu = max([n.cpu for n in notebooks])
    monitor = max([n.monitor for n in notebooks])
    ram = max([n.ram for n in notebooks])
    hdd = max([n.hdd for n in notebooks])
    video = max([n.video for n in notebooks])
    rows = map(lambda n : [n.cpu/cpu, n.monitor/monitor, float(n.ram)/ram, float(n.hdd)/hdd, float(n.video)/video, n.price], notebooks)
    return rows

def get_price(note, koes):
    return sum([note[i]*koes[i] for i in range(5)])

def set_koes(note, koes, error=500):
    price = get_price(note, koes)
    lasterror = abs(note[5] - price)
    while (lasterror > error):
        k = random.randint(0,4)
        inc = (random.random()*2 - 1) * (error*(1 - error/lasterror))
        koes[k] += inc
        if (koes[k] < 0): koes[k] = 0

        price = get_price(note, koes)
        curerror = abs(note[5] - price)
        if (lasterror < curerror):
            koes[k] -= inc
        else:
            lasterror = curerror

def get_avg_koes(koeshistory):
    koes = [0, 0, 0, 0, 0]
    for row in koeshistory:
        for i in range(5):
            koes[i] += koeshistory[i]
    for i in range(5):
        koes[i] /= len(koeshistory)
    return koes


def analyze_params():
    koeshistory = []
    notes = normalized_set_of_notebooks()
    for i in range(len(notes)):
        koes = [0, 0, 0, 0, 0]
        set_koes(notes[i], koes)
        koeshistory.extend(koes)
        if (i % 100 == 0):
            print i
            print koes

    print "cpu, monitor, ram, hdd, video"
    print koes
    print get_avg_koes(koeshistory)

def get_avg_price():
    print sum([n.price for n in get_notebooks()])/len(get_notebooks())

def get_avg_parameters():
    print "cpu {0}".format(sum([n.cpu for n in get_notebooks()])/len(get_notebooks()))
    print "monitor {0}".format(sum([n.monitor for n in get_notebooks()])/len(get_notebooks()))
    print "ram {0}".format(sum([n.ram for n in get_notebooks()])/len(get_notebooks()))
    print "hdd {0}".format(sum([n.hdd for n in get_notebooks()])/len(get_notebooks()))
    print "video {0}".format(sum([n.video for n in get_notebooks()])/len(get_notebooks()))

def get_max_priced_notebook():
    maxprice = max([n.price for n in get_notebooks()])
    maxconfig = filter(lambda x: x.price == maxprice, get_notebooks())[0]
    print "cpu {0}".format(maxconfig.cpu)
    print "monitor {0}".format(maxconfig.monitor)
    print "ram {0}".format(maxconfig.ram)
    print "hdd {0}".format(maxconfig.hdd)
    print "video {0}".format(maxconfig.video)
    print "price {0}".format(maxconfig.price)

def get_min_priced_notebook():
    minprice = min([n.price for n in get_notebooks()])
    minconfig = filter(lambda x: x.price == minprice, get_notebooks())[0]
    print "cpu {0}".format(minconfig.cpu)
    print "monitor {0}".format(minconfig.monitor)
    print "ram {0}".format(minconfig.ram)
    print "hdd {0}".format(minconfig.hdd)
    print "video {0}".format(minconfig.video)
    print "price {0}".format(minconfig.price)

def euclidean(v1, v2):
    d = 0.0
    for i in range(len(v1)):
        d+=(v1[i] - v2[i])**2;
    return math.sqrt(d)

def getdistances(data, vec1):
    distancelist=[]
    for i in range(len(data)):
        vec2 = data[i]
        distancelist.append((euclidean(vec1,vec2),i))
    distancelist.sort()
    return distancelist

def knnestimate(data,vec1,k=10):
    dlist = getdistances(data, vec1)
    avg = 0.0
    for i in range(k):
        idx = dlist[i][1]
        avg +=data[idx][5]
    avg /= k
    return avg

def get_notebooks_list():
    return map(lambda n: [n.cpu, n.monitor, n.ram, n.hdd, n.video, n.price], get_notebooks())

def power_of_notebooks_config():
    return map(lambda x: x[0]*x[1]*x[2]*x[3]*x[4], normalized_set_of_notebooks())
def config_prices():
    return map(lambda x: x[5], normalized_set_of_notebooks())

from pylab import *

def draw_market():
    plot(config_prices(),power_of_notebooks_config(),'bo', linewidth=1.0)

    xlabel('price (Rub)')
    ylabel('config_power')
    title('Russian Notebooks Market')
    grid(True)
    show()
