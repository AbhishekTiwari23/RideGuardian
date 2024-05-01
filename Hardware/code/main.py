from fastapi import FastAPI
import RPi.GPIO as GPIO
import time
import uvicorn

# Set warnings off (optional)
GPIO.setwarnings(False)

# Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Pins
impact_sensor = 16
ir_sensor = 18
micro_switch = 22
push_button = 32
led = 36
buzzer = 38

# Setup GPIO pins
GPIO.setup(impact_sensor, GPIO.IN)
GPIO.setup(ir_sensor, GPIO.IN)
GPIO.setup(micro_switch, GPIO.IN)

GPIO.setup(push_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(led, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)

# Constants and variables
led_status = False
buzzer_status = False
threshold = 100

# Function to define impact levels (adjust based on your sensor readings)
def levelCheck(impact_value):
    if impact_value >= 0 and impact_value <= 100:
        return 1
    elif impact_value >= 101 and impact_value <= 200:
        return 2
    elif impact_value >= 201 and impact_value <= 300:
        return 3
    elif impact_value >= 301:
        return 4
    else:
        return 0

# Function to cleanup GPIO and SPI on exit
def cleanup():
    GPIO.cleanup()
    print("GPIO Cleaned")
    print("SPI Closed")

# FastAPI setup
app = FastAPI()

# Endpoint for impact detection
@app.get("/impact")
async def impact():
    impact_value = GPIO.input(impact_sensor)
    impact_level = levelCheck(impact_value)

    # Send 200 OK response with impact level
    return {"statusCode": 200, "level": impact_level, "value": impact_value}

# Main loop (optional, can be removed)
try:
  # While loop for potential future logic or monitoring
  while True:
    impact_value = GPIO.input(impact_sensor)
    impact_level = levelCheck(impact_value)

      # LED and buzzer control based on impact level
    if impact_level > 1:
          led_status = True
          buzzer_status = True
          GPIO.output(led, led_status)
          GPIO.output(buzzer, buzzer_status)
          time.sleep(1)  # Adjust LED/buzzer activation duration
    else:
          led_status = False
          buzzer_status = False
          GPIO.output(led, led_status)
          GPIO.output(buzzer, buzzer_status)

    time.sleep(10)  # Delay between checks (optional)
    if __name__ == "__main__":
        uvicorn.run("main:app", host="0.0.0.0", port=8000)  # Adjust host and port as needed

except KeyboardInterrupt:
    cleanup()
