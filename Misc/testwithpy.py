import csv

input_file = "input.csv"
output_file = "output.csv"

# Open input and output files
with open(input_file, "r") as in_file, open(output_file, "w", newline="") as out_file:
    reader = csv.reader(in_file)
    writer = csv.writer(out_file)

    # Write header row to output file

    # Initialize row number to 1
    row_num = 0

    # Create an empty list to store rows after row number 1187
    rows_after_1187 = []

    # Loop through each row in the input file
    for row in reader:
        # Extract the domain from the first column in the row
        domain = row[1].split(".")[-1]

        # Check if the domain is ".nl"
        if domain == "nl":
            # Increment the row number
            row_num += 1

            # Check if the row number is greater than or equal to 1187
            if row_num >= 7197:
                # Append the row to the list
                rows_after_1187.append([row_num - 7197, "https://www."+ row[1] + "/"])
            else:
                # Write the row number and domain to the output file
                writer.writerow([row_num, "https://www."+ row[1] + "/"])

    # Write the list of rows after row number 1187 to a separate output file
    with open("output_list.csv", "w", newline="") as list_file:
        writer = csv.writer(list_file)
        writer.writerows(rows_after_1187)
