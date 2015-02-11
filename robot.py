import brickpi
import time
import math

class robot:

	global wheel_motors
	global wheel_seperation
	global wheel_radius
	global sonarMotor
	wheel_radius = 2.8
	wheel_motors = [0,1]
	wheel_seperation = 17.05
	sonarMotor = 2

#############################################################################
########     MAGIC METHODS    ###############################################
#############################################################################

	def __init__(self):
		self.interface = brickpi.Interface()
		self.interface.initialize()

		self.interface.motorEnable(wheel_motors[0])
		self.interface.motorEnable(wheel_motors[1])
		#self.interface.motorEnable(sonarMotor)
		
		motorParams = self.interface.MotorAngleControllerParameters()
		motorParams.maxRotationAcceleration = 6.0
		motorParams.maxRotationSpeed = 12.0
		motorParams.feedForwardGain = 255/10.0
		motorParams.minPWM = 39
		motorParams.pidParameters.minOutput = -255
		motorParams.pidParameters.maxOutput = 255

		#motorParams.pidParameters.k_p = 350.0
		#motorParams.pidParameters.k_i = 650
		#motorParams.pidParameters.k_d = 50
		# proportional gain, reduces error
		motorParams.pidParameters.k_p = 200.0
		# integral gain, removes steady_state error
		motorParams.pidParameters.k_i = 180
		# differential gain, reduce settling time
		motorParams.pidParameters.k_d = 330

		self.interface.setMotorAngleControllerParameters(wheel_motors[0], motorParams)
		self.interface.setMotorAngleControllerParameters(wheel_motors[1], motorParams)
		self.interface.setMotorAngleControllerParameters(sonarMotor. motorParams)
	

#############################################################################
########     PUBLIC INTERFACE METHODS    ####################################
#############################################################################


	def startLogging(self, file_name):
		self.interface.startLogging(file_name)

	def stopLogging(self):
		self.interface.stopLogging()

	def terminate(self):
		self.interface.terminate()

	def setMotorRotationSpeedReferences(self, motor, speed):
		self.interface.setMotorRotationSpeedReferences(motor, speed)

	def motorAngleReferencesReached(self, motors):
		return self.interface.motorAngleReferencesReached(motors)

	def increaseMotorAngleReferences(self, motors, angles):
		self.interface.increaseMotorAngleReferences(motors, angles)

	def getMotorAngles(self, motors):
		return self.interface.getMotorAngles(motors)

	def sensorEnableUltrasonic(self, port):
		self.interface.sensorEnable(port, brickpi.SensorType.SENSOR_ULTRASONIC)

	def sensorEnableTouch(self, port):
		self.interface.sensorEnable(port, brickpi.SensorType.SENSOR_TOUCH)

	def getSensorValue(self, port):
		return self.interface.getSensorValue(port)


#############################################################################
########     PUBLIC MOVEMENT METHODS    #####################################
#############################################################################

	#distance in cm
	def forward(self, distance):
		self.linearMove(-distance)
		print "Completed forward " + str(distance)

	def backward(self, distance):
		self.linearMove(distance)
		print "Completed backward " + str(distance)
 
	def turnRightRad(self, radius):
		length = radius*width/2
		angle = length/wheel_radius
		self.turn([-angle, angle])
		print "Completed right turn " + str(radius)

	def turnLeftRad(self, radius):
		length = radius*width/2
		angle = length/wheel_radius
		self.turn([angle, -angle])
		print "Completed left turn " + str(radius)

	def turnRightDeg(self, degrees):
		self.turnRightRad(degreeToRad(degrees))

	def turnLeftDeg(self, degrees):
		self.turnLeftRad(degreeToRad(degrees))

	def turnRight90(self):
		self.turnRightRad(math.pi/2)	

	def turnLeft90(self):
		self.turnLeftRad(math.pi/2)

	def instantStop(self):
		self.interface.setMotorPwm(0, 0)
		self.interface.setMotorPwm(1, 0)


#############################################################################
########     PUBLIC SENSOR METHODS    #######################################
#############################################################################

	def sonarFront(self):
		pass

	def sonarRightFollow(self):
		pass

	def sonarLeftFollow(self):
		pass

#############################################################################
########     PRIVATE METHODS    #############################################
#############################################################################

	def wheelRadianTurn(radians):
		return (radians * wheel_seperation) / (2 * wheel_radius)

	def degreeToRad(degree):
		return degree * math.pi / 180

	def turn(self, angles):
		self.interface.increaseMotorAngleReferences(wheel_motors, angles)
		while not self.interface.motorAngleReferencesReached(wheel_motors):
			motorAngles = self.interface.getMotorAngles(wheel_motors)
			time.sleep(0.1)

	# direction is true if forward, false if backward
	def linearMove(self, distance):
		angle = distance/wheel_radius
		self.interface.increaseMotorAngleReferences(wheel_motors, [angle, angle])
		while not self.interface.motorAngleReferencesReached(wheel_motors):
			motorAngles = self.interface.getMotorAngles(wheel_motors)
			time.sleep(0.1)


