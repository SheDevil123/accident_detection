import pywhatkit
import time 

h=int(time.strftime('%H'))
m=int(time.strftime('%M'))+1
#pywhatkit.sendwhatmsg("C1XZNm9Vfdn5kmU7L32MTI","person on road \n bike pedestrian collision",h,m)
pywhatkit.sendwhatmsg_to_group("C1XZNm9Vfdn5kmU7L32MTI","person on road \n bike pedestrian collision",h,m)