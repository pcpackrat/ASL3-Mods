# Enable RX LED
in rpt.conf:

[events]

cop,62,GPIO4:1 = c|t|RPT_RXKEYED

cop,62,GPIO4:0 = c|f|RPT_RXKEYED



