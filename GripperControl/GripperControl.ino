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

//#define SERVOMIN  250 // this is the 'minimum' pulse length count (out of 4096)
//#define SERVOMAX  1010 // this is the 'maximum' pulse length count (out of 4096)

// our servo # counter
uint8_t servonum = 0;

struct Servo {
	uint16_t channel;
	uint16_t min;
	uint16_t max;
};

Servo openclose = { 0,400,825 };
Servo slide = { 1,150,1010 }; //1010

#define nservos 2
Servo servos[nservos];

#define byt 2

void runThroughRange(struct Servo *s, uint16_t pause)
{
	// Drive each servo one at a time
	Serial.println(s->channel);
	Serial.println(s->min);
	Serial.println(s->max);
	for (uint16_t pulselen = s->min; pulselen < s->max; pulselen++) {
		pwm.setPWM(s->channel, 0, pulselen);
		Serial.println(pulselen);
		delay(pause);
	}
	pwm.setPin(s->channel, 0, false);
	delay(500);
	for (uint16_t pulselen = s->max; pulselen > s->min; pulselen--) {
		pwm.setPWM(s->channel, 0, pulselen);
		Serial.println(pulselen);
		delay(pause);
	}
	pwm.setPin(s->channel, 0, false);
	delay(500);

	//servonum++;
	//if (servonum > 7) servonum = 0;
}

void setup()
{
	servos[0] = openclose;
	servos[1] = slide;
	Serial.begin(9600);
	Serial.println("16 channel Servo test!");

	pwm.begin();

	pwm.setPWMFreq(100);  // Analog servos run at ~60 Hz updates

	yield();

}



void loop()
{
	if (Serial.available() > byt) 
	{
		static char buffer[byt];
		uint8_t channel = 0;
		for (int i = 0; i < (byt+1); i++) 
		{
			if (i == 0) { channel = Serial.read(); }
			else { buffer[i - 1] = Serial.read(); }
		}
		uint16_t ums = 0;
		for (size_t i = 0; i < byt; ++i) {
			ums = ums + uint8_t(buffer[i])*pow(256, i);
		}
		

		if (channel < nservos)
		{
			Servo s = servos[channel];
			if ( (s.max>ums) && (s.min < ums) ) 
			{
				pwm.setPWM(s.channel, 0, ums);
			}else
			{
				pwm.setPin(s.channel, 0, false);
			}
				
		}
		Serial.print("Channel ");
		Serial.print(channel);
		Serial.print(" Got ");
		Serial.println(ums);
		//Serial.println(uint8_t(buffer[0]));
		//Serial.println(uint8_t(buffer[1]));
	}
	//runThroughRange(&openclose,0);
	//runThroughRange(&slide,100);
}
