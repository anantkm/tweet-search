#!/bin/bash

if [ $# -ne 3 ]
then
    echo "Usage: $0 <index_type> <input_dir> <output_dir>"
    exit 1
fi

index_type=$1
input_dir=$2
output_dir=$3

if [ ! -d "$input_dir" ]
then
    echo "Input directory does not exist: $input_dir"
    exit 1
fi

if [ ! -d "$output_dir" ]
then
    echo "Output directory does not exist: $output_dir"
    exit 1
fi

if [ $index_type = "bert" ]
then
    python bertIndexer.py $input_dir $output_dir
elif [ $index_type = "lucene" ]
then
    python luceneIndexer.py $output_dir $input_dir
else
    echo "Invalid index type. Please specify 'bert' or 'lucene'."
    exit 1
fi
