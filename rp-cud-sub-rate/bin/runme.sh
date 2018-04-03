bulks="1000 100 10 1"
tasks="100000 1000000"

for t in $tasks; do
    for b in $bulks; do
        if [ $b -le $t ]; then
            mkdir bulk-${b}-tasks-${t}
            python runme.py $b $t
            mv *.txt bulk-${b}-tasks-${t}
            mv bulk-${b}-tasks-${t} ../raw-data/
            rm rp.session.* -rf
            echo "$b, $t done"
        fi
    done
done
