import csv

in_file = "transactions.csv"
with open(in_file) as in_csv:
	row_count = sum(1 for row in in_csv)

with open(in_file) as in_csv:
	csv_reader = csv.DictReader(in_csv)
	in_header = csv_reader.fieldnames

	last_student = ""
	student_count = 0
	student_KCs = []
	KCs = {}
	for row in csv_reader:
		student_id = row["Anon Student Id"]
		KC = row["KC"]
		correct = row["Outcome"]

		if (last_student != student_id and last_student != "") or int(row["Row"]) == row_count - 1:
			print student_KCs
			KCs[",".join(student_KCs)] = True
			student_KCs = []
			student_count+=1

		elif correct == "CORRECT":
				student_KCs.append(KC)

		last_student = student_id


	print "student_count", student_count
	print "number of unique KC paths", len(KCs)


