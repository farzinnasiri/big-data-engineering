#! /bin/bash

mkdir test_repo
cd test_repo
git init 

create_file()
{
  file_name="$1"".txt"
  touch "$file_name"
  echo "$2" > "$file_name"
  git add "$file_name"
  
  if [[ "$i" -eq 1 ]]
  then
    git commit -m "added the ${i}st number"
  elif [[ "$i" -eq 2 ]]
  then
    git commit -m "added the ${i}nd number"
  elif [[ "$i" -eq 3 ]]
  then
    git commit -m "added the ${i}rd number"
  else
    git commit -m "added the ${i}th number"
  fi
}

for j in {1..2048}
do 
    branch_name="fib_""$j""_""$(($j+1))"
    git checkout -b $branch_name
    echo "currently on $branch_name"

    f1=$j
    f2=$(($j+1))

    for i in {1..1000}
    do
        create_file $i $f1
        temp=$f1 
        f1=$f2
        f2=$(($temp+$f2))
    done
done




