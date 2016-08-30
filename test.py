#! /usr/bin/env python

import spidev
import time
import sys

spi=spidev.SpiDev() # genarate spi instance
spi.open(0,0) # select ADC/MCP3008 : bus=0, CE=0

channel=0 # select CH0 : ADC/MCP3008


def readAdc(channel):
    adc = spi.xfer2([1,(8+channel)<<4,0])
    data = ((adc[1]&3) << 8) + adc[2]
    return data

def convertVolts(data):
    volts = (data * 3.3) / float(1023)
    volts = round(volts,4)
    return volts

def convertDistance(ADCValue):
	return 200.3775040589502\
        - 2.2657665648980 *ADCValue\
        + 0.0116395328796 *ADCValue*ADCValue\
        - 0.0000299194195 *ADCValue*ADCValue*ADCValue\
        + 0.0000000374087 *ADCValue*ADCValue*ADCValue*ADCValue\
        - 0.0000000000181 *ADCValue*ADCValue*ADCValue*ADCValue*ADCValue



if __name__ == '__main__':
    try:
        while True:
            data = readAdc(0)
            print("adc  : {:8} ".format(data))
            volts = convertVolts(data)
            distance = convertDistance(data)
            #temp = convertTemp(volts)
            print("volts: {:8.2f}".format(volts))
            print("distance: {:8.2f}".format(distance))
            #print("temp : {:8.2f}".format(temp))

            time.sleep(1)
    except KeyboardInterrupt:
        spi.close()
        sys.exit(0)
