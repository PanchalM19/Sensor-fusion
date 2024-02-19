# Sensor-fusion
A navigation stack is developed using the GPS & IMU sensors while also understanding their accuracies. The data was recorded via the Northeastern University's Autonomous car, NUance, on a planned path to perform corrections and generate the plots. As prescribed, data was collected in loops followed by a linear path, returning to the starting point.

## Estimate the heading (yaw) – Magnetometer calibration
Even if a perfect magnetometer were available, it still relies on the earth’s magnetic field to produce accurate orientation/heading estimates. Any condition that influences the magnitude or direction of the earth’s magnetic field can influence heading accuracy. The magnetometer calibration
parameters are then calculated from the captured raw magnetometer measurements. Assuming a homogeneous field such as the earth magnetic field without disturbances, the locus of the true magnetometer measurements in the sensor frame is on the surface of a sphere with the center at the origin and the radius equal to the intensity of the local magnetic field. This sphere is deformed to an ellipsoid as the effect of biases, scale factors and non-orthogonality.

The offset of the center of this ellipsoid is due to the Hard-iron errors which is caused by permanent magnetic fields around the sensor. The deviation of the path from a circle to an ellipsoid is due to the Soft-iron errors and causes it to rotate. These are caused by the paramagnetic materials like ferrous metals.

<img width="230" alt="image" src="https://github.com/PanchalM19/Sensor-fusion/assets/115374409/31187334-6dc9-4ac7-bac5-fd0428b7cfc4">

To get the yaw angle from the yaw rate sensor, we integrate it. This gives us the yaw angle from the Gyro z-axis. To implement a complementary filter, we process the magnetometer's yaw angle with a Low Pass Filter (LPF) to reduce noise, and the gyro's yaw angle with a High Pass Filter (HPF) to eliminate bias. By combining these outputs, the complementary filter prioritizes the stable, long-term data from the magnetometer while compensating for short-term drift in the gyro. This results in an accurate and stable estimation of yaw angle over varying time scales.

![image](https://github.com/PanchalM19/Sensor-fusion/assets/115374409/ece630d8-6675-4aaf-8628-604bbfb431d5)

The yaw angle from the complementary filter is compared with the yaw angle directly obtained from the Inertial Measurement Unit (IMU). The IMU's yaw angle is derived by converting orientation from quaternion to Euler angles, followed by unwrapping the x-axis. Comparing these two yaw angles, we observe a close match between the yaw angle provided by the complementary filter and the one calculated directly from the IMU.
![image](https://github.com/PanchalM19/Sensor-fusion/assets/115374409/e374a730-2fae-4f58-8411-c686ebd37657)



