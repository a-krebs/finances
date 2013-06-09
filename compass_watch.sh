#!/bin/bash

for i in $(find -type d -name 'sass' | sed -r 's/\/sass$//')
	do
		#echo $i
		compass watch --sass-dir $i/sass --css-dir $i/css &
done
