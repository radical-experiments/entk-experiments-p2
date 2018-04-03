tasks="1 10 100 1000 10000 100000 1000000"

for t in $tasks; do
    mkdir tasks-${t}
    python runme.py $t
    mv *.txt tasks-${t}
    mv tasks-${t} ../raw-data/
    echo "$t done"
done
