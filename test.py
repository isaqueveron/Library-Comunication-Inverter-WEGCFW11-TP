#inicializing serial port
import time
import serial
import serial.tools.list_ports
ports = list(serial.tools.list_ports.comports())
for i in range(len(ports)):
    print("connected to: ",ports[i][0])
port = ports[0][0]
time.sleep(1)
########################

from LCINVfunctions import Inverter



meu_inversor = Inverter(Port=ports[0][0], ADR=1, Baudrate=57600)
meu_inversor = Inverter(Port=ports[1][0], ADR=1, Baudrate=57600)


meu_inversor.SendReferenceAngularVelocity(0)
meu_inversor.StopMotor()            

meu_inversor.SendReferenceAngularVelocity(10)
meu_inversor.ActivateMotor()    

time.sleep(5)

meu_inversor.SendReferenceAngularVelocity(0)
meu_inversor.StopMotor()            


