# stock

grep "DTD HTML 4.01" history_data/* | awk -F':'  '{print $1}' | xargs rm -f
while read line ; do head -6 history_data/$line | tail -5  >  recent_data/$line; done < history_data/code
while read line ; do awk -F',' 'BEGIN{max=0;}{if ($4<min){min=$4;}if ($3>max){max=$3;}}END{print max, min;}' recent_data/$line >> recent_data/$line; done < history_data/code

