from pythonosc import dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
import serial
import time

# connections of the circuit found in Arduino IDE
ARDUINO_PORT = "/dev/cu.usbmodem1101"
BAUD_RATE = 115200
OSC_IP = "127.0.0.1"
OSC_PORT = 8000

def setup_arduino():
    try:
        arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE)
        print(f"Connected to Arduino on {ARDUINO_PORT}")
        time.sleep(2)
        return arduino
    except serial.SerialException as e:
        print(f"Error connecting to Arduino: {e}")
        return None

def vibration_handler(unused_addr, *values):
    print(f"Received OSC message: {values}")
    if arduino:
        if len(values) == 1:
            value = values[0]
            intensity = int(value * 255) if value <= 1 else min(255, int(value))
        else:
            intensity = 127 # mapping values
        
        command = f"VIB{intensity}\n"
        arduino.write(command.encode())
        print(f"Sent: VIB{intensity}")

def main():
    global arduino
    
    print("HAPTIC BRIDGE")
    print("=" * 30)
    
    arduino = setup_arduino()
    
    disp = dispatcher.Dispatcher()
    disp.map("/vibration", vibration_handler)
    disp.map("/led", vibration_handler)
    
    server_instance = ThreadingOSCUDPServer((OSC_IP, OSC_PORT), disp)
    
    print("Haptic bridge ready!")
    
    try:
        server_instance.serve_forever()
    except KeyboardInterrupt:
        if arduino:
            arduino.close()

if __name__ == "__main__":
    arduino = None
    main()
