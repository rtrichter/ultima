#include "Arduino.h"

typedef uint16_t time_s_t; /* 1 second */
typedef uint32_t time_ms_t; /* 1 millisecond */
typedef uint32_t time_us_t; /* 1 microsecond */
typedef uint16_t frequency_hz_t; /* 1 Hertz */

#define MOTOR (2) // motor port
#define FREQUENCY ((frequency_hz_t)50) 
#define PERIOD ((time_us_t)(1000000/FREQUENCY))
// #define VALUE (10) // percent power (-100 to 100)
// #define HIGH_DELAY (long)(((float)(VALUE+300) / (float)200) * 1000) 


void setup() {
    pinMode(MOTOR, OUTPUT);
}

void waitMicroseconds(long time_us) {
    delay(time_us / 1000);
    delayMicroseconds(time_us % 1000);
}

void wait(time_us_t time);
void wait(time_ms_t time);

# define MAX_MICRO_DELAY ((int)16383)
void wait(time_us_t time) {
    while ( time > 0 ) {
        if ( time < MAX_MICRO_DELAY ) {
            delayMicroseconds(time);
            break;
        }
        delayMicroseconds(MAX_MICRO_DELAY);
        time /= MAX_MICRO_DELAY;
    }
}

void wait(time_ms_t time) {
    while ( time > 0 ) {
        if ( time < MAX_MICRO_DELAY ) {
            delay(time);
            break;
        }
        delay(MAX_MICRO_DELAY);
        time /= MAX_MICRO_DELAY;
    }
}

void loop() {
    static double value = 10;
    time_us_t width = (value+3)/2 * 1000;
    digitalWrite(MOTOR, HIGH);
    waitMicroseconds(width);
    digitalWrite(MOTOR, LOW);
    waitMicroseconds(PERIOD - width);
}
