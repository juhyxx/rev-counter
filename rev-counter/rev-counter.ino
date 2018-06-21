int data[10];
int i = 0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  
  Serial.print(1);    
  Serial.print(",");    
  Serial.println(i*i);    
  i++;
  if (i == 10) {
    i = 0;
  }
  
  delay(1000);
}
