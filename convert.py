import subprocess

def fetch_sequences_from_bed(bed_input, fasta_reference, processed_output):
    # Temporary file to store the initial output from bedtools
    temp_file = 'temp_sequences.fasta'

    # Step 1: Use bedtools to extract sequences to a temporary file
    bedtools_command = f"bedtools getfasta -fi {fasta_reference} -bed {bed_input} -fo {temp_file}"

    try:
        subprocess.run(bedtools_command, shell=True, check=True)

        # Step 2: Open the temporary file and process it to remove headers
        with open(temp_file, 'r') as temp_input, open(processed_output, 'w') as final_output:
            for line in temp_input:
                if not line.startswith('>'):
                    # Write the sequence lines to the final output file
                    final_output.write(line)

        print(f"Sequences extracted and processed into {processed_output}")

    except subprocess.CalledProcessError as error:
        print(f"An error occurred while running bedtools: {error}")

# Usage of the function
bed_input = 'regions.bed'
fasta_reference = '/users/hemasai/reference/hg38.fa'
processed_output = 'extracted_sequences.txt'

fetch_sequences_from_bed(bed_input, fasta_reference, processed_output)
