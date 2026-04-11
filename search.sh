#!/bin/bash

echo "Enter search pattern:"
read search_pattern
grep -r -i -n -C 2 --color=auto "$search_pattern" 
