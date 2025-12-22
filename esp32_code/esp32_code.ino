#include <WiFi.h>
#include <FirebaseESP32.h> // Install "Firebase ESP32 Client" by Mobizt

// ----- WiFi credentials -----
#define WIFI_SSID "iFiW"
#define WIFI_PASSWORD "ABCD1234"

// ----- Firebase credentials -----
#define FIREBASE_HOST "braille-display-b87be-default-rtdb.asia-southeast1.firebasedatabase.app" // e.g., braille-display.firebaseio.com
#define FIREBASE_AUTH "JmfhE3a7bXgX93GxdliKbI3uRbE5DpU2FGi45MZM" // In Realtime Database -> Rules (legacy token)

// ----- Firebase objects -----
FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

// Braille patterns: each char → 2x3 boolean matrix
// Dots numbered:
// 1 4
// 2 5
// 3 6
// true = raised, false = flat
struct BrailleChar {
  bool dots[6];
};

// Lookup table for letters a–z
BrailleChar brailleAlphabet[] = {
  {{1,0,0,0,0,0}}, // a
  {{1,1,0,0,0,0}}, // b
  {{1,0,0,1,0,0}}, // c
  {{1,0,0,1,1,0}}, // d
  {{1,0,0,0,1,0}}, // e
  {{1,1,0,1,0,0}}, // f
  {{1,1,0,1,1,0}}, // g
  {{1,1,0,0,1,0}}, // h
  {{0,1,0,1,0,0}}, // i
  {{0,1,0,1,1,0}}, // j
  {{1,0,1,0,0,0}}, // k
  {{1,1,1,0,0,0}}, // l
  {{1,0,1,1,0,0}}, // m
  {{1,0,1,1,1,0}}, // n
  {{1,0,1,0,1,0}}, // o
  {{1,1,1,1,0,0}}, // p
  {{1,1,1,1,1,0}}, // q
  {{1,1,1,0,1,0}}, // r
  {{0,1,1,1,0,0}}, // s
  {{0,1,1,1,1,0}}, // t
  {{1,0,1,0,0,1}}, // u
  {{1,1,1,0,0,1}}, // v
  {{0,1,0,1,1,1}}, // w
  {{1,0,1,1,0,1}}, // x
  {{1,0,1,1,1,1}}, // y
  {{1,0,1,0,1,1}}  // z
};

void printBrailleGrid(char c) {
  if (c >= 'A' && c <= 'Z') c += 32; // convert to lowercase

  BrailleChar b;

  if (c < 'a' || c > 'z') {
    // Unknown character → all zeros
    for (int i = 0; i < 6; i++) b.dots[i] = 0;
  } else {
    int index = c - 'a';
    b = brailleAlphabet[index];
  }

  // Print 2x3 grid
  Serial.println("------");
  Serial.printf("%c:\n", c);
  Serial.printf("%d %d\n", b.dots[0], b.dots[3]); // Row 1: dots 1,4
  Serial.printf("%d %d\n", b.dots[1], b.dots[4]); // Row 2: dots 2,5
  Serial.printf("%d %d\n", b.dots[2], b.dots[5]); // Row 3: dots 3,6
}

void setup() {
  Serial.begin(115200);

  // WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi");

  // Firebase setup
  config.host = FIREBASE_HOST;
  config.signer.tokens.legacy_token = FIREBASE_AUTH;
  Firebase.begin(&config, &auth);
  Firebase.reconnectWiFi(true);
}

void loop() {
  if (Firebase.getString(fbdo, "/brailleText")) {
    String text = fbdo.stringData();
    Serial.println("Received: " + text);
    for (size_t i = 0; i < text.length(); i++) {
      printBrailleGrid(text[i]);
      delay(500);
    }
  } else {
    Serial.println("Firebase read failed: " + fbdo.errorReason());
  }
  delay(2000); // check every 2s
}

  WiFi.disconnect(true);  // Clear old credentials
  delay(1000);

  Serial.printf("Connecting to %s...\n", WIFI_SSID);
  WiFi.mode(WIFI_STA); // Station mode (ESP32 as client)
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int retries = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print("Connecting");
    for (int i = 0; i < 3; i++) { Serial.print("."); delay(300); }
    Serial.println();

    int status = WiFi.status();
    if (status == WL_NO_SSID_AVAIL) Serial.println("⚠ SSID not found!");
    if (status == WL_CONNECT_FAILED) Serial.println("⚠ Wrong password?");
    if (status == WL_DISCONNECTED) Serial.println("⚠ Disconnected");

    retries++;
    if (retries > 20) {
      Serial.println("❌ Failed to connect, restarting...");
      ESP.restart(); // Restart if can't connect after ~20 sec
    }
  }

  Serial.println("✅ Connected to Wi-Fi!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200);
  delay(500);
  connectToWiFi();
}

void loop() {
  // Your main code here
}
