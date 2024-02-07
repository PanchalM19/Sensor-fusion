import serial
import rospy
import utm
from gps_data.msg import Code

pub = rospy.Publisher('Receiver', Code , queue_size=10)
info=Code()
def sender():
    #rate = rospy.Rate(10)
    info.latitu=lat
    info.longitu=long
    info.altitu=alt
    info.utm_e=u[0]
    info.utm_n=u[1]
    info.fix=int(gps_dat[6])
    info.Zone_no=u[2]
    info.Zone_let=u[3]
    pub.publish(info)
    #rate.sleep()
if __name__ == '__main__':
    rospy.init_node('Sender', anonymous=True)
    while not rospy.is_shutdown():
        data = serial.Serial(port='/dev/ttyACM0',baudrate=9600)
        line = data.readline()
        # print(line)
        if line.startswith(b'$GNGGA'):
            gps1 = line.decode()           
            # line = "$GPGGA,199304.973,3248.7780,N,11355.7832,W,1,06,02.2,25722.5,M,,,*00"
            gps_dat = gps1.split(",")
            # print(gps_dat)
            # neededData1 = (float(gps_dat[2]), float(gps_dat[4]), float(gps_dat[9]))
            # print(neededData1)
            lat = float(gps_dat[2])
            long = float(gps_dat[4])
            latD = int(lat)/100
            longD = int(long)/100
            Nlat = latD + (((latD*100)-lat)/60)
            Nlong = longD + (((longD*100)-long)/60)
            if (gps_dat[3])=='S':
                Nlat=-Nlat;
            if (gps_dat[5])=='W':
                Nlong=-Nlong
            # print(type(gps_dat[2]))
            alt = float(gps_dat[9])
            u = utm.from_latlon(Nlat, Nlong)
            # print (u)
            # neededData2 = (float(utm_data[0]), float(utm_data[1]))
            # rate = rospy.Rate(10)
            # print("\n Latitude:",lat,"\n Longitude:",long,"\n Altitude:",alt, "\n UTM_Easting:",u[0], "\n UTM_Northing:",u[1], "\n Zone number:", u[2], "\n Zone letter:", u[3])
            sender()
            #rospy.sleep()