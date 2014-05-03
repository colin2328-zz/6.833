import csv

in_file = "transactions.csv"
out_file = "transactions2.csv"
with open(in_file) as in_csv:
	with open(out_file, 'wb') as out_csv:		
		csv_reader = csv.DictReader(in_csv)
		in_header = csv_reader.fieldnames
		print in_header

		csv_writer = csv.DictWriter(out_csv, fieldnames = in_header + ["KC"])
		csv_writer.writeheader()

		last_row = ""
		KCs = {}
		count = 0
		for row in csv_reader:
			KC = row["KC (Original)"]
			if not KC in KCs:
				KCs[KC] = count
				count+=1
			row["KC"] = chr(KCs[KC] + ord('A'))
			csv_writer.writerow(row)