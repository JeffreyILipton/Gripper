#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);

// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define SERVOMIN  250 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  1010 // this is the 'maximum' pulse length count (out of 4096)

// our servo # counter
uint8_t servonum = 0;

struct Servo {
	uint8_t channel;
	uint8_t min;
	uint8_t max;
};

void setup()
{

	Serial.begin(9600);
	Serial.println("16 channel Servo test!");

	pwm.begin();

	pwm.setPWMFreq(100);  // Analog servos run at ~60 Hz updates

	yield();

}

void loop()
{

	// Drive each servo one at a time
	Serial.println(servonum);
	for (uint16_t pulselen = SERVOMIN; pulselen < SERVOMAX; pulselen++) {
		pwm.setPWM(servonum, 0, pulselen);
		Serial.println(pulselen);
		delay(100);
	}

	delay(500);
	for (uint16_t pulselen = SERVOMAX; pulselen > SERVOMIN; pulselen--) {
		pwm.setPWM(servonum, 0, pulselen);
		Serial.println(pulselen);
		delay(100);
	}

	delay(500);

	//servonum++;
	//if (servonum > 7) servonum = 0;

}
