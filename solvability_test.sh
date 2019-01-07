#!/bin/bash

prog='./solver.py'



echo '--UNSOLVABLE------------------------'
echo '------------------------------------'

path1='samples/UNSOLVABLE/snail*'
opt1='-s snail'
for f in $path1; do
    echo $prog $opt1 $f;
    $prog $opt1 $f;
done


path1='samples/UNSOLVABLE/zerofirst*'
opt1='-s zero_first'
for f in $path1; do
    echo $prog $opt1 $f;
    $prog $opt1 $f;
done

path1='samples/UNSOLVABLE/zerolast*'
opt1='-s zero_last'
for f in $path1; do
    echo $prog $opt1 $f;
    $prog $opt1 $f;
done


echo ''
echo ''
echo '--SOLVED----------------------------'
echo '------------------------------------'


path1='samples/SOLVED/snail*'
opt1='-s snail'
for f in $path1; do
    echo $prog $opt1 $f;
    $prog $opt1 $f;
done


path1='samples/SOLVED/zerofirst*'
opt1='-s zero_first'
for f in $path1; do
    echo $prog $opt1 $f;
    $prog $opt1 $f;
done


path1='samples/SOLVED/zerolast*'
opt1='-s zero_last'
for f in $path1; do
    echo $prog $opt1 $f;
    $prog $opt1 $f;
done
