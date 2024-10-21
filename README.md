# Phrase Query Search

This repository contains the implementation of a text processing pipeline, unigram inverted index, and phrase query search using a positional index. The project is organized to preprocess a collection of text files, create inverted indices, and perform various query operations on the dataset.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Dataset](#dataset)
- [Preprocessing](#preprocessing)
- [Unigram Inverted Index](#unigram-inverted-index)
- [Positional Index](#positional-index)
- [Setup](#setup)
- [Usage](#usage)
- [Output Format](#output-format)
- [License](#license)

## Introduction

This project performs text preprocessing, creates a unigram inverted index and a positional index for efficient search, and handles both boolean queries and phrase queries. The focus is on designing these components from scratch without using any external libraries for indexing.

## Features

- **Text Preprocessing**: Lowercasing, tokenization, stopword removal, punctuation removal, and trimming whitespace.
- **Unigram Inverted Index**: Supports Boolean queries (`AND`, `OR`, `AND NOT`, `OR NOT`) for retrieving documents containing the specified terms.
- **Positional Index**: Handles phrase queries by finding documents where the terms occur in a given order.
- **Query Parsing**: Supports multiple operations in a single query and provides a flexible way to handle input.

## Dataset

The dataset consists of multiple text files, each containing raw text data. You can add your own files to the `dataset/` directory.

Example file: `file1.txt`

`Loving these vintage springs on my vintage strat. They have a good tension and great stability. If you are floating your bridge and want the most out of your springs then these are the way to go.`


## Preprocessing

The following preprocessing steps are applied to each file in the dataset:

1. **Lowercase the text**: Convert all text to lowercase.
2. **Tokenization**: Split text into individual words.
3. **Stopword Removal**: Remove common stopwords such as "and", "the", etc.
4. **Punctuation Removal**: Remove punctuation marks.
5. **Whitespace Removal**: Remove tokens that are just empty spaces.

After preprocessing, the processed files are stored back in the `preprocessed/` directory for further use.

## Unigram Inverted Index

- **Inverted Index**: An index that maps terms to the documents they appear in.
- **Query Operations Supported**:
  - `T1 AND T2`
  - `T1 OR T2`
  - `T1 AND NOT T2`
  - `T1 OR NOT T2`
  - Complex queries like `T1 AND T2 OR T3 AND T4`
  
The inverted index is saved and loaded using Python’s `pickle` module.

## Positional Index

- **Positional Index**: An index that maps terms to their positions in documents, allowing for phrase queries where the exact sequence of words matters.
- Supports querying phrases like `"car bag in a canister"`.

The positional index is also saved and loaded using Python’s `pickle` module.

## Setup

To set up the project on your local machine, follow these steps:

1. **Clone the repository**:
   ```bash
   https://github.com/Talkative-Banana/Phrase_Query_Search.git
   cd Phrase_Query_Search
2. **Add your dataset:**
  - Place your raw text files in the text_files_raw/ directory.
  - Ex: file1.txt

## Usage

- **Text Preprocessing:** Run the script to clean and process the dataset:
  ```bash
  python main.py
  
## Output Format
For both Boolean and phrase queries, the output includes:

**Query:** The formatted query string.

**Number of documents retrieved:** The total count of documents matching the query.

**Document names:** The names of the files where the terms/phrases were found.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
