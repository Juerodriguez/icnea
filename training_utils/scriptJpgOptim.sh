#!/bin/bash

#echo "Enter variable init [number]"
#read init
#echo "Enter variable end [number]"
#read end

cd spanner

for filename in $(ls)
do
    echo processing $filename
    jpegoptim --size=30% $filename;
done

echo "All rigth! Images JPG compressed"