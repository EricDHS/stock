#!bin/shell
rate=$1
while read line
do
  #awk -F',' -v var="$line"  'BEGIN{max=0;}{if ($3 > max){max = $3;}END{if ((abs($2-$5)<0.02) && ($4 < max * 0.8)){print var;}  }' recent_data/$line
  awk -F',' -v var=$line -v  num=1 -v rate_aws=$rate 'BEGIN{max=0;op=0;cl=0;min=0;}{if(NR == num){op=$2;cl=$5;min=$4;}if ($3 > max){max = $3;}}END{if ((sqrt((op-cl)*(op-cl))<0.02) && (min < max*rate_aws)){print var, max*0.85;}}' recent_data/$line
done < history_data/code
