# Open the input file for reading
with open('cleaned_pantadeusz.txt', 'r') as input_file:
    # Open a new file for writing
    with open('cleaned_pantadeusz_no_empty_lines.txt', 'w') as output_file:
        # Iterate over each line in the input file
        for line in input_file:
            # Check if the line is not empty
            if line.strip():
                # Write the non-empty line to the output file
                output_file.write(line)