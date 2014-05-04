import edmonds
import pandas as pd
from collections import defaultdict

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

	return trans

G = get_graph('KC (Original)')
G = get_graph('KC')
print G

min_weight = 1e5
min_h = None
for root in G.keys():
	h = edmonds.mst(root,G)
	total_weight = 0
	for s in h:
		for t in h[s]:
			total_weight += G[s][t]
			# print "%s->%s (weight: %s)" % (s,t,G[s][t])
	# print "total_weight", total_weight
	if total_weight < min_weight:
		min_weight = total_weight
		min_h = h

for s in h:
	for t in h[s]:
		print "%s->%s (weight: %s)" % (s,t,G[s][t])
