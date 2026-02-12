import re

def calculate_optimal_length(input_file_path):
    sequence_sizes = []

    # Collect all nucleotide sequence sizes
    with open(input_file_path, 'r') as input_file:
        for sequence in input_file:
            sequence = sequence.strip()
            # Skip lines that are chromosome intervals
            if not sequence.startswith('>'):
                sequence_sizes.append(len(sequence))

    # Determine the optimal size using median
    sorted_sizes = sorted(sequence_sizes)
    if sorted_sizes:
        median_size = sorted_sizes[len(sorted_sizes) // 2]
        return median_size
    else:
        return 0

def split_intervals_for_positive(input_file_path, output_bed_file, block_length):
    # Regular expression to parse chromosome intervals
    interval_pattern = re.compile(r'>?(chr[\w\d]+):(\d+)-(\d+)')
    interval_list = []

    # Read and store chromosome intervals
    with open(input_file_path, 'r') as input_file:
        for sequence in input_file:
            sequence = sequence.strip()
            match = interval_pattern.match(sequence)
            if match:
                chromosome, start_pos, end_pos = match.groups()
                interval_list.append((chromosome, int(start_pos), int(end_pos)))

    # Write split intervals to the output bed file
    with open(output_bed_file, 'w') as output_bed:
        for chromosome, start_pos, end_pos in interval_list:
            # Split the interval into blocks of specified length
            for block_start in range(start_pos, end_pos, block_length):
                block_end = block_start + block_length
                if block_end <= end_pos:
                    output_bed.write(f"{chromosome}\t{block_start}\t{block_end}\n")

def create_intervals_for_negative(input_file_path, output_negative_file, block_length):
    # Regular expression to parse chromosome intervals
    interval_pattern = re.compile(r'>?(chr[\w\d]+):(\d+)-(\d+)')
    interval_list = []

    # Read and store chromosome intervals
    with open(input_file_path, 'r') as input_file:
        for sequence in input_file:
            sequence = sequence.strip()
            match = interval_pattern.match(sequence)
            if match:
                chromosome, start_pos, end_pos = match.groups()
                interval_list.append((chromosome, int(start_pos), int(end_pos)))

    # Calculate gaps and split them for the negative file
    with open(output_negative_file, 'w') as output_bed:
        for i in range(len(interval_list) - 1):
            current_chr, current_start, current_end = interval_list[i]
            next_chr, next_start, next_end = interval_list[i + 1]

            if current_chr == next_chr:  # Ensure intervals are on the same chromosome
                gap_start = current_end
                gap_end = next_start
                gap_size = gap_end - gap_start

                if gap_size > 0 and gap_size % block_length == 0:
                    # Write each sub-interval of the block size
                    for block_start in range(gap_start, gap_end, block_length):
                        block_end = block_start + block_length
                        output_bed.write(f"{current_chr}\t{block_start}\t{block_end}\n")

# Example usage
input_file_path = 'ENCFF027BPY.txt'

# Step 1: Determine the optimal block length
optimal_block_length = calculate_optimal_length(input_file_path)

# Step 2: Divide intervals into sub-intervals and write to positive and negative files
positive_bed_file = 'positive_intervals.bed'
negative_bed_file = 'negative_intervals.bed'

split_intervals_for_positive(input_file_path, positive_bed_file, optimal_block_length)
create_intervals_for_negative(input_file_path, negative_bed_file, optimal_block_length)
