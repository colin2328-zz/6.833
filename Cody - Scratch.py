# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# Data manipulation
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.stats as ss
import sys
import datetime
import math
from collections import defaultdict

# <codecell>

data = pd.read_csv('transactions.csv')

# <codecell>

data.head()

# <markdowncell>

# # Exploration

# <codecell>

print "Number of KCs in KC original: {0}".format(len(data['KC (Original)'].unique()))
print "Number of KCs in KC (LFASearchModel0): {0}".format(len(data['KC (LFASearchModel0)'].unique()))
print "Number of Student: {0}".format(len(data['Anon Student Id'].unique()))

# <markdowncell>

# ## Finding 1: Students don't necessarily see all knowledge components

# <codecell>

data.loc[:,['Anon Student Id', 'KC (Original)']]\
    .groupby('Anon Student Id')\
    .agg(len)['KC (Original)']\
    .value_counts()\
    .sort_index()

# <markdowncell>

# ## Finding 2: Students see as few as 2 knowledge components

# <codecell>

data.loc[:,['Anon Student Id', 'KC (Original)']]\
    .drop_duplicates().groupby('Anon Student Id')\
    .agg(len)['KC (Original)']\
    .value_counts().sort_index()

# <markdowncell>

# # Probability of seeing knowledge components before one another

# <codecell>

seq = data.loc[:, ['Anon Student Id', 'KC (Original)', 'Time', 'Outcome']]
seq.rename(columns = {'Anon Student Id': 'student_id',
                      'KC (Original)': 'kc',
                      'Time': 'time',
                      'Outcome': 'outcome'}, inplace = True)
seq = seq.sort(['student_id', 'time'])
seq.head()

# <codecell>

firsts = seq.groupby(['student_id', 'kc'])\
    .apply(lambda x: x.sort('time')['time'].iloc[0])\
    .reset_index()\
    .rename(columns = {0: 'first_time'})\
    .sort(['student_id', 'first_time'])


print len(firsts)
print len(firsts.loc[:,['student_id','kc']].drop_duplicates())
    
firsts.head()

# <codecell>

# proof of concept
tmp1 = DataFrame({'a': {2013: 0, 2014: 2}, 'b': {2013: 5, 2014: 5}})
tmp2 = Series({'a': 5, 'b': 5})
tmp1 / tmp2

# <codecell>

firsts['kc'].value_counts()

# <codecell>

# Create a container for counting the transitions from one knowledge component to another
trans = {}
for kc in firsts['kc'].unique():
    trans[kc] = defaultdict(int)
    
# Group by student_id
grouped = firsts.groupby('student_id')

# Go through each student and count the transitions from one knowledge component to another
for name, group in grouped:
    seen = set()
    for index, row in group.iterrows():
        for kc in seen:
            trans[row['kc']][kc] += 1
        seen.add(row['kc'])
        
# Create a dataframe of transition probabilities from the counts
seen_prob = DataFrame(trans).fillna(0) / firsts['kc'].value_counts()

# <codecell>

seen_prob

# <markdowncell>

# # Probability of getting a knowledge components correct before one another

# <codecell>

correct_firsts = seq[seq.outcome == 'CORRECT'].groupby(['student_id', 'kc'])\
    .apply(lambda x: x.sort('time')['time'].iloc[0])\
    .reset_index()\
    .rename(columns = {0: 'first_time'})\
    .sort(['student_id', 'first_time'])


print len(firsts)
print len(firsts.loc[:,['student_id','kc']].drop_duplicates())
    
correct_firsts.head()

# <codecell>

(correct_firsts == firsts).head()

# <codecell>

diff = (correct_firsts == firsts)['first_time'] 
print "Number of time a KC was right on the first try: {0}".format(len(diff[diff == True]))
print "Number of time a KC was wrong on the first try: {0}".format(len(diff[diff == False]))

# <codecell>

# Create a container for counting the transitions from one knowledge component to another
trans = {}
for kc in correct_firsts['kc'].unique():
    trans[kc] = defaultdict(int)
    
# Group by student_id
grouped = correct_firsts.groupby('student_id')

# Go through each student and count the transitions from one knowledge component to another
for name, group in grouped:
    seen = set()
    for index, row in group.iterrows():
        for kc in seen:
            trans[row['kc']][kc] += 1
        seen.add(row['kc'])
        
# Create a dataframe of transition probabilities from the counts
correct_prob = DataFrame(trans).fillna(0) / correct_firsts['kc'].value_counts()

# <codecell>

correct_prob

# <markdowncell>

# ## Finding (3): Students must get a KC correct before moving on

# <codecell>

seen_prob - correct_prob

# <codecell>


