int data[10];
int i = 0, j =0, k = 0;

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

  Serial.print(2);    
  Serial.print(",");    
  Serial.println(j*j / 4);    
  j++;
  if (j == 30) {
    j = 0;
  }

   Serial.print(3);    
  Serial.print(",");    
  Serial.println(30-k);    
  k++;
  if (k == 30) {
    k = 0;
  }
  
  
  delay(1000);
}
