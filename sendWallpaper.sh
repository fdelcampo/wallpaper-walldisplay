#!/bin/bash


function colNum {
  case "$1" in
          "a" ) return 0;;
          "b" ) return 2;;
          "c" ) return 4;;
  esac
}

#start client nodes
for col in {a..c}
do
  for row in {1..4}
    do
      echo $1$col$row_l.jpg
      scp $1$col$row_l.jpg wall@$col$row.wall.inria.cl:/usr/share/backgrounds/images/default_l.png
      echo $1$col$row_r.jpg
      scp $1$col$row_r.jpg wall@$col$row.wall.inria.cl:/usr/share/backgrounds/images/default_r.png
    done
done
