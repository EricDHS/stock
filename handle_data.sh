#!bin/shell
grep "DTD HTML 4.01" history_data/* | awk -F':'  '{print $1}' | xargs rm -f
while read line ; do head -6 history_data/$line | tail -5  >  recent_data/$line; done < history_data/code
