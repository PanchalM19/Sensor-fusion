#!/usr/bin/env python
import serial
import rospy
from sensor_msgs.msg import Imu
from sensor_msgs.msg import MagneticField
import numpy as np
  
def Sender1():
    pub = rospy.Publisher('Receiver1',Imu,queue_size=10)
    # rospy.init_node('Sender1',anonymous=True)
    mesg1=Imu()
    # mesg1.header.seq = seq+1
    mesg1.header.stamp = rospy.Time.now()
    mesg1.header.frame_id = "IMU Data"
    mesg1.orientation.x = Qx
    mesg1.orientation.y = Qy
    mesg1.orientation.z = Qz
    mesg1.angular_velocity.x = Gx
    mesg1.angular_velocity.y = Gy
    mesg1.angular_velocity.z = Gz
    mesg1.linear_acceleration.x = Ax
    mesg1.linear_acceleration.y = Ay
    mesg1.linear_acceleration.z = Az
    pub.publish(mesg1)

def Sender2():
    pub = rospy.Publisher('Receiver2',MagneticField,queue_size=10)
    # rospy.init_node('Sender2',anonymous=True)
    mesg2=MagneticField()
    mesg2.header.stamp = rospy.Time.now()
    mesg2.header.frame_id = "Magnetic Field Data"
    mesg2.magnetic_field.x = Mx
    mesg2.magnetic_field.y = My
    mesg2.magnetic_field.z = Mz
    pub.publish(mesg2)

if __name__=='__main__':
    # SENSOR_NAME = "IMU"
    rospy.init_node('Sender1','Sender2', anonymous=True)
    rate = rospy.Rate(40) # 40hz
    while not rospy.is_shutdown():
        data=serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
        # port = serial.Serial(serial_port, serial_baud)
        # serial_port = rospy.get_param('~port','/dev/ttyUSB0')
        # serial_baud = rospy.get_param('~baudrate',115200)
        line=data.readline()
        # print(line)
        if line.startswith(b'$VNYMR'):
            myimu=line.decode()
            # print(imu)
            # line = $VNYMR,-165.980,-037.300,+001.245,+00.2893,+00.0748,+00.7405,-05.970,-00.4
            # line = $VNYMR,+098.271,-002.209,+113.219,-00.0591,+00.3633,+00.3419,-00.455,-08.852,+03.721,+00.036270,+00.000459,-00.002356*64
            myimu_data=myimu.split(",")
            # print(myimu_data)
            # print(type(myimu_data))
            # needed_data1=Mag(G3,B8), Acc(G3,B9), Gyr(G3,B10), YPR(G1,B3 or G5,B1)
            # seq=0
            Yaw=float(myimu_data[1])
            Pit=float(myimu_data[2])
            Rol=float(myimu_data[3])
            Mx=float(myimu_data[4])
            My=float(myimu_data[5])
            Mz=float(myimu_data[6])
            Ax=float(myimu_data[7])
            Ay=float(myimu_data[8])
            Az=float(myimu_data[9])
            Gx=float(myimu_data[10])
            Gy=float(myimu_data[11])
            Gzval=myimu_data[12].split("*")
            Gz=float(Gzval[0])
            # print("\n Yaw:",Yaw,"\n Pitch:",Pit,"\n Roll:",Rol, "\n Mx:",Mx, "\n My:",My, "\n Mz:",Mz, "\n Ax:",Ax, "\n Ay:",Ay, "\n Az:",Az, "\n Gx:",Gx, "\n Gy:",Gy,  "\n Gz:",Gz)
            # print(Yaw,Pit,Rol,Mx,My,Mz,Ax,Ay,Az,Gx,Gy,Gz)
            Qx=np.sin(Rol/2)*np.cos(Pit/2)*np.cos(Yaw/2)
            Qy=np.cos(Rol/2)*np.sin(Pit/2)*np.cos(Yaw/2)
            Qz=np.cos(Rol/2)*np.cos(Pit/2)*np.sin(Yaw/2)
            Qw=np.cos(Rol/2)*np.cos(Pit/2)*np.cos(Yaw/2)
            Sender1()
            Sender2()
            rate.sleep()
        elif rospy.ROSInterruptException:
            pass