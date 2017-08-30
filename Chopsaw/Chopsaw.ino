
int PowerTail_D = 12;
int PowerTail_pwm = 3;
int PowerTail_break = 9;

int Motor_D = 13;
int Motor_pwm = 11;
int Motor_break = 8;
int Motor_pot = A0;


float target = 0;
float val = 0;

void setup()
{
	pinMode(PowerTail_D, OUTPUT);
	pinMode(PowerTail_pwm, OUTPUT);
	pinMode(PowerTail_break, OUTPUT);
	pinMode(Motor_D, OUTPUT);
	pinMode(Motor_pwm, OUTPUT);
	pinMode(Motor_break, OUTPUT);
	Serial.begin(9600);
	Serial.println("Starting!");

	digitalWrite(PowerTail_D, HIGH);
	digitalWrite(Motor_D, HIGH);
	digitalWrite(PowerTail_break, LOW);
	digitalWrite(Motor_break, LOW);
}



void loop()
{
	if (Serial.available() ) 
	{
		char c = Serial.read();
		if (c == 'o') 
		{
			Serial.print("Opening");
			target = 0.9;
		}
		else if (c == 'c') 
		{
			Serial.print("Closing");
			target = 0.10;
		}
		else if (c == 'b')
		{
			Serial.print("Blade Starting");
			digitalWrite(PowerTail_pwm, HIGH);
		}
		else if (c == 'b')
		{
			Serial.print("Blade Stoping");
			digitalWrite(PowerTail_pwm, LOW);
		}
		


	}

}


void MotorController() 
{
	val = analogRead(Motor_pot)/1023;
	float p = target - val;
	float pabs = fabs(p);
	if (p > 0) 
	{
		digitalWrite(Motor_D, HIGH);
	}
	else 
	{
		digitalWrite(Motor_D, LOW);
	}
	int pwm = 0;
	if (pabs > 0.10) {
		pwm = int(pabs * 255);
	}
	analogWrite(Motor_pwm, pwm);
}
