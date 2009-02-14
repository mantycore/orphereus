#!/bin/sh
# Directory for storing RRD Databases
RRDDATA=/opt/var/lib/rrd/

# Directory for storing images
RRDIMG=/opt/lampp/htdocs/rrd/radio/

HIRESRRD="${RRDDATA}/radio-hour.rrd"
MAINRRD="${RRDDATA}/radio-main.rrd"

CreateRRD ()
{	
	rrdtool create "${1}" --step "${2}"\
	DS:curr:GAUGE:600:0:12500000 \
	DS:max:GAUGE:600:0:12500000 \
	RRA:AVERAGE:0.5:1:576 \
	RRA:AVERAGE:0.5:6:672 \
	RRA:AVERAGE:0.5:24:732 \
	RRA:AVERAGE:0.5:144:1460
}

if [ ! -f "${MAINRRD}" ] ; then
    echo "RRD file : ${MAINRRD} does not exist...Creating Now..."
    CreateRRD "${MAINRRD}" 300
fi

if [ ! -f "${HIRESRRD}" ] ; then
    echo "RRD file : ${MAINRRD} does not exist...Creating Now..."
    CreateRRD "${MAINRRD}" 30
fi

listeners=`/opt/pyapps/C.C./graph/state.py`
CURR=`echo $listeners | awk '{print $1}'`
MAX=`echo $listeners | awk '{print $2}'`

echo "Curr $CURR Max $MAX"

rrdupdate "${MAINRRD}" -tcurr:max N:"${CURR}":"${MAX}"
rrdupdate "${HIRES}" -tcurr:max N:"${CURR}":"${MAX}"

# $1 = ImageFile , $2 = Time in secs to go back , $3 = RRDfil , $4 = GraphText 
CreateGraph ()
{
  rrdtool graph "${1}.new" -a PNG -s -"${2}" -w 700 -h 300 -v "ppl" -l 0 \
  'DEF:ds1='${3}':curr:AVERAGE' \
  'DEF:ds2='${3}':max:AVERAGE' \
  'LINE1:ds1#00FF00:Listeners' \
  GPRINT:ds1:MIN:"Min %6.0lf %s" \
  GPRINT:ds1:AVERAGE:"Avg %6.0lf %s" \
  GPRINT:ds1:LAST:"Curr %6.0lf %s\n" \
 'LINE1:ds2#0000FF:Max listeners' \
  GPRINT:ds2:LAST:"%6.0lf %s" \
  -t "${4}"
		        
  mv -f "${1}.new" "${1}"
}


CreateGraph "${RRDIMG}/list_hour.png" 3600 "${HIRES}" "Anoma-FM [last hour]" #86400
CreateGraph "${RRDIMG}/list_day.png" 86400 "${MAINRRD}" "Anoma-FM [last day]" #86400
CreateGraph "${RRDIMG}/list_week.png" 604800 "${MAINRRD}" "Anoma-FM [last week]" #86400