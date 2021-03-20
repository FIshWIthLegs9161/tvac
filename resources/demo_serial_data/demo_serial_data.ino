// Testing code used to supply serial data to the temperature plotting script

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("secs/4    BLU    GRN     RED     YELLOW  Setting   Error   Int   Der   Action     ");

}

 float   a = 0;

void loop() {
  // put your main code here, to run repeatedly:


  
  float b = random(1000, 5000) / 100.0;
  float c = random(1000, 5000) / 100.0;
  float d = random(1000, 5000) / 100.0;
  float e = random(1000, 5000) / 100.0;
  float f = random(1000, 5000) / 100.0;
  float g = random(1000, 5000) / 100.0;
  float h = random(1000, 5000) / 100.0;
  float i = random(1000, 5000) / 100.0;
  float j = random(1000, 5000) / 100.0;
  float k = random(1000, 5000) / 100.0;

  Serial.print(a,0);
  Serial.print("   ");
  Serial.print(b);
  Serial.print("   ");
  Serial.print(c);
  Serial.print("   ");
  Serial.print(d);
  Serial.print("   ");
  Serial.print(e);
  Serial.print("   ");
  Serial.print(f);
  Serial.print("   ");
  Serial.print(g);
  Serial.print("   ");
  Serial.print(h);
  Serial.print("   ");
  Serial.print(i);
  Serial.print("   ");
  Serial.print(j);
  Serial.print("   ");
  Serial.print(k);
  Serial.println();

  a = a+0.25 ;
  delay(500);
}
