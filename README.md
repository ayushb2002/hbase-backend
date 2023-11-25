## To start HBase and Hbase Port for Web application- 
<br>
$ su -l hadoop <br>
$ start-all.sh <br>
$ start-hbase.sh <br>
$ hbase-daemon.sh start thrift -p 9090 --infoport 9091 <br>

## To stop HBase and Hadoop - 
<br>
$ stop-hbase.sh <br>
$ stop-all.sh <br>