# DNase-seq Accessible and Non-Accessible DNA Region Pipeline

## Overview
This project implements a genomic data preprocessing pipeline to generate
**accessible (positive)** and **non-accessible (negative)** DNA sequence regions
from DNase-seq narrowPeak data. The pipeline was developed as part of a
computational genomics coursework project and focuses on preparing fixed-length
DNA sequences suitable for downstream machine learning experiments.

---

## Objectives
- Process DNase-seq narrowPeak BED files
- Determine an optimal fixed-length DNA segment size
- Generate positive samples from DNase-accessible regions
- Generate negative samples from genomic regions between peaks
- Extract nucleotide sequences using `bedtools`

---



## Methodology

### 1. Optimal Sequence Length Selection
The pipeline computes the **median sequence length** from the input data and
uses this value as the fixed block size for all generated DNA segments.

### 2. Positive Sample Generation
DNase-accessible regions (peaks) are split into equal-length sub-intervals,
producing **positive samples** that represent open chromatin regions.

### 3. Negative Sample Generation
Negative samples are generated from **genomic gaps between consecutive peaks**
on the same chromosome, ensuring that these regions are not DNase-accessible.

### 4. Sequence Extraction
Nucleotide sequences corresponding to the generated BED intervals are extracted
from the human reference genome (hg38) using:

FASTA headers are removed to produce clean sequence files.

---

## Scripts

### `code1.py`
- Computes optimal block length
- Splits peak regions into positive samples
- Generates negative samples from inter-peak gaps

### `convert.py`
- Extracts nucleotide sequences using `bedtools`
- Outputs processed DNA sequences without FASTA headers

---

## Requirements
- Python 3.9+
- bedtools
- Human reference genome (hg38)

Install dependencies:
```bash
pip install -r requirements.txt
