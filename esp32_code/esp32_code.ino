#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <FirebaseESP32.h>
#include <Adafruit_PWMServoDriver.h>

// ----- WiFi credentials -----
#define WIFI_SSID "iFiW"
#define WIFI_PASSWORD "ABCD1234"

// ----- Firebase credentials -----
#define FIREBASE_HOST "braille-display-b87be-default-rtdb.asia-southeast1.firebasedatabase.app"
#define FIREBASE_AUTH "JmfhE3a7bXgX93GxdliKbI3uRbE5DpU2FGi45MZM"

// ----- Pin Definitions -----
#define BUTTON_PIN 35

// ----- Firebase objects -----
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

// ----- PCA9685 -----
Adafruit_PWMServoDriver pca1 = Adafruit_PWMServoDriver(0x40);
Adafruit_PWMServoDriver pca2 = Adafruit_PWMServoDriver(0x41);

uint16_t pwmSpeed = 2000;
int currentPos = 0;          
int lastButtonState = LOW;   
String fullText = "";        

struct BrailleChar { bool dots[6]; };

BrailleChar brailleAlphabet[] = {
  {{1,0,0,0,0,0}}, {{1,1,0,0,0,0}}, {{1,0,0,1,0,0}}, {{1,0,0,1,1,0}}, 
  {{1,0,0,0,1,0}}, {{1,1,0,1,0,0}}, {{1,1,0,1,1,0}}, {{1,1,0,0,1,0}}, 
  {{0,1,0,1,0,0}}, {{0,1,0,1,1,0}}, {{1,0,1,0,0,0}}, {{1,1,1,0,0,0}}, 
  {{1,0,1,1,0,0}}, {{1,0,1,1,1,0}}, {{1,0,1,0,1,0}}, {{1,1,1,1,0,0}}, 
  {{1,1,1,1,1,0}}, {{1,1,1,0,1,0}}, {{0,1,1,1,0,0}}, {{0,1,1,1,1,0}}, 
  {{1,0,1,0,0,1}}, {{1,1,1,0,0,1}}, {{0,1,0,1,1,1}}, {{1,0,1,1,0,1}}, 
  {{1,0,1,1,1,1}}, {{1,0,1,0,1,1}}                                    
};

// ----- Mapping Helper Function -----
// This handles the 9,8,11,10 swap logic
int getSwappedPin(int pin) {
  if (pin % 2 == 0) return pin + 1; // 0->1, 8->9, 10->11
  else return pin - 1;             // 1->0, 9->8, 11->10
}

void stopAllMotors() {
  for (int i = 8; i < 16; i++) pca1.setPWM(i, 0, 0);
  for (int i = 0; i < 16; i++) pca2.setPWM(i, 0, 0);
}

void driveBrailleCell(int cellIndex, char c, uint16_t pwmValue) {
  if (c >= 'A' && c <= 'Z') c += 32; 

  BrailleChar b;
  if (c < 'a' || c > 'z') {
    for (int i = 0; i < 6; i++) b.dots[i] = 0;
  } else {
    b = brailleAlphabet[c - 'a'];
  }

  for (int dot = 0; dot < 6; dot++) {
    int virtualIndex = (cellIndex * 6) + dot; 
    
    if (virtualIndex < 8) {
      // PCA1 logic (Pin 8-15) with swapped order
      int physicalPin = getSwappedPin(virtualIndex + 8);
      pca1.setPWM(physicalPin, 0, b.dots[dot] ? pwmValue : 0);
    } 
    else {
      // PCA2 logic (Pin 0-15) with swapped order
      int physicalPin = getSwappedPin(virtualIndex - 8);
      pca2.setPWM(physicalPin, 0, b.dots[dot] ? pwmValue : 0);
    }
  }
}

String filterText(String input) {
  String filtered = "";
  for (int i = 0; i < input.length(); i++) {
    char c = input[i];
    if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
      filtered += c;
    }
  }
  return filtered;
}

void displayCurrentWindow() {
  Serial.printf("\n--- Window: %d to %d ---\n", currentPos, currentPos + 3);
  for (int i = 0; i < 4; i++) {
    int charIdx = currentPos + i;
    char c = (charIdx < fullText.length()) ? fullText[charIdx] : ' ';
    driveBrailleCell(i, c, pwmSpeed);
    Serial.print(c);
  }
  Serial.println("\n--------------------");
}

void setup() {
  Serial.begin(115200);
  pinMode(BUTTON_PIN, INPUT_PULLDOWN);

  pca1.begin();
  pca1.setPWMFreq(200);
  pca2.begin();
  pca2.setPWMFreq(200);

  stopAllMotors();
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }

  config.host = FIREBASE_HOST;
  config.signer.tokens.legacy_token = FIREBASE_AUTH;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void loop() {
  if (Firebase.getString(fbdo, "/brailleText")) {
    String cleaned = filterText(fbdo.stringData());
    if (cleaned != fullText) {
      fullText = cleaned;
      currentPos = 0; 
      displayCurrentWindow();
    }
  }

  int currentButtonState = digitalRead(BUTTON_PIN);
  if (currentButtonState == HIGH && lastButtonState == LOW) {
    if (fullText.length() > 0) {
      currentPos += 4;
      if (currentPos >= fullText.length()) currentPos = 0;
      displayCurrentWindow();
    }
  }
  lastButtonState = currentButtonState;
  delay(50); 
}