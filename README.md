# killmultinodes.py
Useful for disconnecting nodes that forget to disconnect from a previous system before connecting to yours. 

Has the following options:

Whitelist file option to allow privat nodes.  May just want to put 1990-1995 in here.  1 node per line

ignorelist file option to ignore your locally connected private nodes

loop option to run it as a service and loop at 10 second or more intervals

quiet option to supress any output

[events]

cop,62,GPIO4:1 = c|t|RPT_RXKEYED

cop,62,GPIO4:0 = c|f|RPT_RXKEYED



