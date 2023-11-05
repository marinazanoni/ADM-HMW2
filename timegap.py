#timegap.py

import time
import math
import pandas as pd
import matplotlib.pyplot as plt
import json
from collections import Counter
from collections import defaultdict
import numpy as np
from datetime import datetime
from datetime import date
import re

# Return num and den of average will be used later on to compute a series or a non series time gap
def numden(lis):
    # If the list has less than two elements time gap can't be computed
    if len(lis)<2:
        return (0,0)
    else:
        # Computing average time gap
        return (lis[-1]-lis[0], len(lis)-1)

#Define a function which stores all dates from a non series book as negative to distinguish from it later
def negatelist(ll):
    for i in range(len(ll)):
        # If a list of books which belongs to a non-series books, which is only a list
        if ll[i] != '':
            # Store all dates as negative
            ll[i] = -ll[i]
    return ll


# Creating a dictionary that stores books for each author
def transf (dic):
    aut_dict = defaultdict(lambda: [])
    for aut in dic.keys():
        # If a book is a non-series book
        if aut[1] == '':
            # Insert negative value
            aut_dict[aut[0]].append(negatelist(dic[aut]))
        else:
            # For series-books we insert the value
            aut_dict[aut[0]].append(dic[aut])
    return aut_dict

#Compute the numerators and denominators for each author
def oneavg(li):
    num = 0
    den = len(li)
    c = 0
    if len(li) > 1:
        for i in range(den):
            # If I have a missing value for a year I assign a very low number
            if li[i]=='':
                li[i] = -10000
                # But still count a publication
                c += 1
        # Order the list
        li.sort()
        # If there were only missing values in a list
        if c == den:
            # I compute the maximum value, 100 - a LIFETIME - to write c books
            num = 100*c
        else:
            # If not then I get a negative value because it is a non-series book and I have to do
            #the subtracion with the first (at position c which is the first not-empty value) year minus the last one
            if li[-1] <0:
                num = li[c]-li[-1]
            else:
                #Otherwise I just compute the time gap in which I published the series
                num = li[-1]-li[c]
    #Returning a numerator and denominator in order to compute average for series-book properly as soon as I get all authors
    return (num, den)

# Create a list of tuple where I store all avgone results
def totavg(lists):
    m = []
    for elem in lists:
        m.append(oneavg(elem))
    return m

#Compute the average of the avereges for the series of books for each all authors or the average of the avereges
#of non-series book for all the authors
#returning a tuple (average for series-books, average for non-series-books)
def avgaut(d):
    #create a list to store tuples of means for a single author
    dd = []
    # For each list of years in the dictionary author-years
    for item in d.values():
        dd = dd + (totavg(item))
    # Average of series
    m_series = 0
    # Numerator of series
    num_series = 0
    # Average of non-series
    m_nonseries = 0
    # For each tuple (num, den)
    for i in dd:
        # If it is a serie-book
       if i[0]>=0:
            # If the avg time gap is not zero
            if i[1]>0:
                # Sum the averages of series- book
                m_series += (i[0]/i[1])
            # Count how many series for a author
            num_series += 1
        # If it is a non-series book there is only one division to compute for each author
       else:
           # Excluding ZeroDivision Error
           if i[1]>0:
               m_nonseries += (-i[0]/i[1])
    # There as many non-series books as the total tuple (auth, years) minus the series tuples
    num_nonseries = len(dd) - num_series
    # If there are no series-book
    if num_series == 0:
        #And no non-serie books
        if num_nonseries == 0:
            #There's no average to compute
            return(0,0)
        else:
            # Computing only average for non-series books
            return(0, m_nonseries/num_nonseries)
    else:
        if num_nonseries == 0:
            # Computing only average for series books
            return(m_series/num_series, 0)
        else:
            # Computing both averages and rounding them
            return (round(m_series/num_series,3), round(m_nonseries/num_nonseries,3))
