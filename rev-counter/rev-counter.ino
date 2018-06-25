int data[10];
int i = 0, j =0, k = 0, l = 1;

void setup() {
  Serial.begin(9600);
}

void loop() {
  
  Serial.println(String("1," + String(i, DEC)));    
  i++;
  if (i == 10) {
    i = 0;
  }

  Serial.println(String("2," + String(j*j / 10, DEC)));     
  j++;
  if (j == 30) {
    j = 0;
  }

 Serial.println(String("3," + String(30-k, DEC)));      
  k++;
  if (k == 30) {
    k = 0;
  }

  Serial.println(String("4," + String(l, DEC)));      
  l++;
  if (l == 50) {
    l = 1;
  }
   
  delay(0);
}
