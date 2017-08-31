
/// A
int PowerTail_D = 12;
int PowerTail_pwm = 3;
int PowerTail_break = 9;

//B
int Motor_D = 13;
int Motor_pwm = 11;
int Motor_break = 8;
int Motor_pot = A0;


///float target = 0;
//float val = 0;

int target = 0;
int val = 0;
//const float A = 255.0 / 1024.0;
int open = 29;
int closed = 40;
bool startstop = false;


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
	digitalWrite(Motor_break, HIGH);
}



void loop()
{
	if (Serial.available() ) 
	{
		char c = Serial.read();
		if (c == 'o') 
		{
			Serial.print("o");
			target = open;
			startstop = true;
		}
		else if (c == 'c') 
		{
			Serial.print("c");
			target = closed;
			startstop = true;
		}
		else if (c == 's')
		{
			Serial.print("s");
			target = val;
			startstop = false;
			digitalWrite(Motor_pwm, LOW);
		}
		else if (c == 'b')
		{
			Serial.print("b");
			digitalWrite(PowerTail_pwm, HIGH);
		}
		else if (c == 'B')
		{
			Serial.print("B");
			digitalWrite(PowerTail_pwm, LOW);
		}
	}
	if (startstop) { MotorController(); }

}


void MotorController() 
{
	val = analogRead(Motor_pot);
	int  delta = target - val;
	int delta_abs = abs(delta);
	int pwm = 0;

	if (delta > 0) 
	{
		digitalWrite(Motor_D, LOW);
	}
	else 
	{
		digitalWrite(Motor_D, HIGH);
	}

	if ( (delta_abs > 1) && ( (val>open) || (val <closed) ) )
	{
		pwm = 255;
		digitalWrite(Motor_pwm, 255);
		digitalWrite(Motor_break, LOW);
	}
	else 
	{
		startstop = false;
		Serial.print("s");
		digitalWrite(Motor_pwm, 0);
		digitalWrite(Motor_break, HIGH);
	}

	//Serial.print("read: ");
	//Serial.println(val);
}
