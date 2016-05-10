#!bin/shell
while read line
do
  echo $line
  curl http://hq.sinajs.cn/list=$line 2>/dev/null \
  | awk -F ',' '{print $31","$2","$5","$6","$4","$9","$4}' > tmp_data

  cat recent_data/$line >> tmp_data
  mv tmp_data recent_data/$line


done < history_data/code
