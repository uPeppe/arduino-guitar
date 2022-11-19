const int NUM_BUTTONS = 9; 
// Maximum buttons for the current code: 16

const int BITS_PER_BYTE = 8;

int button[NUM_BUTTONS];

byte msg[3];

void setup() {
  
  Serial.begin(115200);

  // Configuring buttons: [ID] PIN
  button[0] = 2;
  button[1] = 3;
  button[2] = 4;
  button[3] = 5;
  button[4] = 6;
  button[5] = 7;
  button[6] = 8;
  button[7] = 9;
  button[8] = 12;

  for(int i = 0; i < NUM_BUTTONS; i++)
  {
    pinMode(button[i], INPUT);
    digitalWrite(button[i], HIGH);
  }
}

void loop() {
  
  byte out[2] = {0, 0};

  for(int i = 0; i < BITS_PER_BYTE, i < NUM_BUTTONS; i++)
  {    
    if( digitalRead(button[i]) == 0 )
      out[0] |= 1 << i;

  }
  for(int i = BITS_PER_BYTE; i < NUM_BUTTONS; i++)
  {
    if( digitalRead(button[i]) == 0 )
      out[1] |= (1 << i - BITS_PER_BYTE);

  }
  if( !(out[0] == msg[0] && out[1] == msg[1])  )
  {
    msg[0] = out[0];
    msg[1] = out[1];
    msg[2] = ~(out[0] | out[1]); // check for message safety
    Serial.write(msg, 3);
  }

}