#!/bin/bash

max=400000
for((i=120000;i<=max;i++))
do
  j=$(printf "%08x\n" $i)
  k="\U"
  t=$(echo -e $k$j | ./a | grep "HV19")
  if (( ${#t} > 0 )); then
    echo -e $t
    echo -e $k$j
    break
  fi
done

