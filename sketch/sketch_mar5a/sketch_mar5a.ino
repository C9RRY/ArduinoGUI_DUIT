#include <LiquidCrystal_I2C.h>
#include <Arduino.h>
#include <TM1637Display.h>
#include <MatrizLed.h>
#include <GyverEncoder.h>


#define REL 3
#define DISP_CLK 4
#define DISP_DIO 5
#define POT 0
#define MOSFET 9
#define ENC_CLK 17
#define ENC_DT 16
#define ENC_SW 15
#define SOIL_DET A0
#define RAIN_DET A7
#define MATRIX_DIN 12
#define MATRIX_CLK 11
#define MATRIX_CS 10


LiquidCrystal_I2C lcd(0x27, 16, 2); //Рідкокристалічний дисплей I2C1602
TM1637Display tm_display(DISP_CLK, DISP_DIO); // Дисплей 4 семисигментних індикатора
MatrizLed matrix; // 8x8 світлодіодна матриця (MAX7219)
Encoder enc(ENC_CLK, ENC_DT, ENC_SW); // Енкодер

 
void setup() {
  Serial.begin(9600); // встановлюємо з'єднання 
  lcd.init(); 
  lcd.backlight(); 
  pinMode(REL, OUTPUT);
  tm_display.setBrightness(0x0f);
  matrix.begin(MATRIX_DIN, MATRIX_CLK, MATRIX_CS, 1); // DIN, CLK, CS, кількість матриць 8x8
  matrix.rotar(false);
  matrix.setIntensidad(3); // яскравість (0 - 15)  
}
 

void loop() {
  read_port(); // читання з порта
  write_port(); // запис у порт

  // енкодер
  enc.tick(); 
  if (enc.isTurn()) {
    Serial.println(1);
    Serial.println(':');    
    if (enc.isRight()) Serial.println(2);
    if (enc.isLeft()) Serial.println(-2);
  }  
}


void read_port() {
  if (Serial.available() > 0) { //перевіряємо наявність даних
    char incomingByte[30];  // встановлюємо розмір буфера
    int amountByte = Serial.readBytesUntil(',', incomingByte, 30); // ":" - термінатор, записуємо дані у incomingByte, amountByte - кількість байт 
    incomingByte[amountByte] = NULL; // пишемо null в зону amountByte  
    char* str_data = strchr(incomingByte, ':'); // стрічка починаючи з розділювача ":"
    char key[5] = ""; 
    strncpy(key, incomingByte, str_data-incomingByte); //виділяєм ключ
    int int_data = atoi(++str_data); // виділяєм значення
    int int_key = atoi(key); // інвертуєм ключ у тип даних int

    // розподіляєм кейси відносно пристроїв
    switch (int_key) {
      case 1: // перша стрічка дисплей I2C1602
        lcd.setCursor(0, 0);
        lcd.print("                ");
        lcd.setCursor(1, 0);
        lcd.print(str_data); break;
      case 2: // друга стрічка дисплей I2C1602
        lcd.setCursor(0, 1);
        lcd.print("                ");
        lcd.setCursor(1, 1);
        lcd.print(str_data); break;
      case 3: // дисплей TM1637
        tm_display.clear();
        tm_display.showNumberDec(int_data, false); break;
      case 4: // матриця 8х8 MAX7219
        matrix.escribirFrase(str_data); break;
        matrix.encender(); break;                                                  
      case 5: // реле
        digitalWrite(REL, int_data); break;
      case 6: // мосфіт модуль
        analogWrite(MOSFET, int_data); break;
    };        
  }        
}


void write_port() {
  // надсилання даних малої частоти
  static uint32_t tmr = 0;
  if (millis() - tmr > 200) {
    tmr = millis();
    Serial.print(2);
    Serial.print(':');
    Serial.print(analogRead(SOIL_DET));
    Serial.print(',');        
    }
  
  // швидке надсилання даних
  static uint32_t tmr2 = 0;
  if (millis() - tmr2 > 50) {
    tmr2 = millis();
    Serial.print(3);
    Serial.print(':');
    Serial.print(analogRead(RAIN_DET));
    Serial.print(',');
  }      
}