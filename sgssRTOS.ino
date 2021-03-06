/*
Sensor
Ultrasonic 5  5V
PIR Motion 3 5V
Magnetic Switch 4
RFID 2 53 52 51 50 3.3V

Actuators
LED RGB 12 11 10 5V
Buzzer 6
LCD SDA/SCL 20/21 5V

*/
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <RFID.h>
#include <SPI.h>
#include <Arduino_FreeRTOS.h>
#include <string.h>
#include <stdlib.h>

// Deklarasi pin sensor
#define ultraPin 5
#define pirPin 3
#define magPin 4

// RFID pin
#define rstPin 2
#define ssPin 53

// Deklarasi pin aktuator
#define buzPin 6

RFID rfid(ssPin, rstPin);
LiquidCrystal_I2C lcd(0x27, 16, 2);

// Deklarasi variable
int ultra;
bool mag, latest_mag, access, pir, latest_pir;
String nama;

// Registrasi RFID ID and Name
int cards[][5] = {
  {41,173,125,194,59},
  {136,4,41,29,184}
};

String names[] = {
  "Odin",
  "Ali"  
};

// Deklarasi Task
void Task_Ultra(void *pvParameters);
void Task_Pir(void *pvParameters);
void Task_Mag_Rfid(void *pvParameters);

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(buzPin, OUTPUT);
  pinMode(magPin, INPUT_PULLUP);
  pinMode(pirPin, INPUT);
  SPI.begin();
  rfid.init();
  lcd.init();
  lcd.backlight();
  xTaskCreate(Task_Ultra, "Ultra" , 128, NULL, 1, NULL );
  xTaskCreate(Task_Pir, "Pir" , 128, NULL, 1, NULL );
  xTaskCreate(Task_Mag_Rfid, "MagRfid" , 128, NULL, 1, NULL );
  
}

void loop() {}

void readSignalUltra(){
  pinMode(ultraPin, OUTPUT);
  digitalWrite(ultraPin, LOW);
  delayMicroseconds(2);
  digitalWrite(ultraPin, HIGH);
  delayMicroseconds(2);
  digitalWrite(ultraPin, LOW);
  pinMode(ultraPin, INPUT);

  ultra = pulseIn(ultraPin, HIGH) * 0.01723 ;
  Serial.print("U ");
  Serial.println(ultra);
  
  if (ultra < 100){
    digitalWrite(LED_BUILTIN, HIGH);  
  } else {
    digitalWrite(LED_BUILTIN, LOW);  
  }
}

void readSignalPir(){
  pir = digitalRead(pirPin);
  if (latest_pir != pir){
    latest_pir = pir;
    Serial.print("P ");
    Serial.println(latest_pir);
  }
}

void readSignalMag(){
  mag = digitalRead(magPin);
  if (latest_mag != mag){
    latest_mag = mag;
    boolean buz = latest_mag;
    if(access){
      buz = false;
      access = false;
    }
    digitalWrite(buzPin, buz);
    Serial.print("M ");
    Serial.println(latest_mag);
  }
}

void readSignalRfid(){
  if (rfid.isCard()){
    if(rfid.readCardSerial()){
      digitalWrite(buzPin, HIGH);
      delay(100);
      digitalWrite(buzPin, LOW);
            
      for(int x = 0; x < sizeof(cards); x++){
        for(int i = 0; i < sizeof(rfid.serNum); i++ ){
          if(rfid.serNum[i] != cards[x][i]) {
            access = false;
            break;
          } else {
            nama = names[x];
            access = true;
          }
        }
        if(access) break;
      }     
    }
    if(access){
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Authenticated");
      lcd.setCursor(0,1);
      lcd.print("Welcomeback ");
      lcd.print(nama);
      Serial.print("R ");
      Serial.print("1 ");
      Serial.println(nama);
    } else {
      lcd.clear();
      lcd.setCursor(0,0);
      lcd.print("Unauthenticated");
      lcd.setCursor(0,1);
      lcd.print("Please move back!");    
      Serial.print("R ");
      Serial.print("0 ");
      Serial.print(rfid.serNum[0]);
      Serial.print(rfid.serNum[1]);
      Serial.print(rfid.serNum[2]);
      Serial.print(rfid.serNum[3]);
      Serial.println(rfid.serNum[4]);  
    }
    delay(1000);
  }
  else {
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Smart Gate");
    lcd.setCursor(0,1);
    lcd.print("Security Systems");  
  }  
}

void Task_Ultra(void *pvParameters)
{   
    (void) pvParameters;
    Serial.begin(9600);
    for (;;) 
    {
    readSignalUltra();
    vTaskDelay(50);
    } 
}

void Task_Pir(void *pvParameters)
{   
    (void) pvParameters;
    Serial.begin(9600);
    for (;;) 
    {
    readSignalPir();
    vTaskDelay(50);
    } 
}

void Task_Mag_Rfid(void *pvParameters)
{   
    (void) pvParameters;
    Serial.begin(9600);
    for (;;) 
    {
    readSignalMag();
    readSignalRfid();
    vTaskDelay(50);
    } 
}
