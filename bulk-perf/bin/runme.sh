bulks="1 10 100 1000"
tasks="1000000"

for t in $tasks; do
    for b in $bulks; do
        if [ $b -lt $t ]; then
            mkdir bulk-${b}-tasks-${t}
            python runme.py $b $t
            mv *.txt bulk-${b}-tasks-${t}
            mv bulk-${b}-tasks-${t} ../raw-data/
            echo "$b, $t done"
        fi
    done
done
