import edmonds
import pandas as pd
from collections import defaultdict
from pandas import DataFrame

'''Get the graph for a KC column- usually either 'KC (Original)'' or 'KC' '''
def get_graph(kc_column):
	data = pd.read_csv('transactions.csv')

	seq = data.loc[:, ['Anon Student Id', kc_column, 'Time', 'Outcome']]
	seq.rename(columns = {'Anon Student Id': 'student_id',
						  kc_column: 'kc',
						  'Time': 'time',
						  'Outcome': 'outcome'}, inplace = True)
	seq = seq.sort(['student_id', 'time'])

	correct_firsts = seq[seq.outcome == 'CORRECT'].groupby(['student_id', 'kc'])\
		.apply(lambda x: x.sort('time')['time'].iloc[0])\
		.reset_index()\
		.rename(columns = {0: 'first_time'})\
		.sort(['student_id', 'first_time'])

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
	correct_prob = (1- (DataFrame(trans) / correct_firsts['kc'].value_counts()).T)

	return correct_prob.to_dict()

G = get_graph('KC (Original)')
# G = get_graph('KC')
print G

#loop through root to get the minimum weighted 
min_weight = 1e5
min_h = None
for root in G.keys():
	h = edmonds.mst(root,G)
	total_weight = 0
	for s in h:
		for t in h[s]:
			total_weight += G[s][t]
	if total_weight < min_weight:
		# print "min weight is %s. Total weight is %s" % (root, total_weight)
		min_weight = total_weight
		min_h = h

for s in min_h:
	for t in h[s]:
		print "%s->%s (weight: %s)" % (s,t, (1- G[s][t]))
