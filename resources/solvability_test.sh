#!/bin/bash

prog='./solver.py '



echo '--UNSOLVABLE------------------------'
echo '------------------------------------'

path1='resources/puzzles/UNSOLVABLE/snail*'
opt1='-s snail'
for f in $path1; do
    echo $prog $opt1 $f;
    $prog $opt1 $f;
done


path1='resources/puzzles/UNSOLVABLE/zerofirst*'
opt1='-s zero_first'
for f in $path1; do
    echo $prog $opt1 $f;
    $prog $opt1 $f;
done

path1='resources/puzzles/UNSOLVABLE/zerolast*'
opt1='-s zero_last'
for f in $path1; do
    echo $prog $opt1 $f;
    $prog $opt1 $f;
done


echo ''
echo ''
echo ''
echo ''
echo ''
echo ''
echo ''
echo ''
echo ''
echo ''
echo ''
echo ''
echo ''
echo ''
echo ''
echo ''
echo ''
echo ''
echo '--SOLVED----------------------------'
echo '------------------------------------'


path1='resources/puzzles/SOLVED/snail*'
opt1='-s snail'
for f in $path1; do
    echo $prog $opt1 $f;
    $prog $opt1 $f;
done


path1='resources/puzzles/SOLVED/zerofirst*'
opt1='-s zero_first'
for f in $path1; do
    echo $prog $opt1 $f;
    $prog $opt1 $f;
done


path1='resources/puzzles/SOLVED/zerolast*'
opt1='-s zero_last'
for f in $path1; do
    echo $prog $opt1 $f;
    $prog $opt1 $f;
done
