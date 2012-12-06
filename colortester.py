#!/bin/python
# -*- coding: utf8 -*- 

import sys, argparse, socket, math

#3 bytes per pixel
PIXEL_SIZE = 3

class RGBController:

    def __init__(self):
        self.gamma = bytearray(256)
        for i in range(256):
            self.gamma[i] = int(pow(float(i) / 255.0, 2.5) * 255.0 )

        self.verbose = False
        self.num_leds = 96
        self.color_red = 255
        self.color_green = 255
        self.color_blue = 255

    def correct_pixel_brightness(self, pixel):

    	corrected_pixel = bytearray(3)	
    	corrected_pixel[0] = int(pixel[0] / 1.1)
    	corrected_pixel[1] = int(pixel[1] / 1.1)
    	corrected_pixel[2] = int(pixel[2] / 1.3)
    	
    	return corrected_pixel

    # Apply Gamma Correction and RGB / GRB reordering
    # Optionally perform brightness adjustment
    def filter_pixel(self, input_pixel, brightness):
        input_pixel[0] = int(brightness * input_pixel[0])
        input_pixel[1] = int(brightness * input_pixel[1])
        input_pixel[2] = int(brightness * input_pixel[2])
        output_pixel = bytearray(PIXEL_SIZE)
        output_pixel[0] = self.gamma[input_pixel[0]]
        output_pixel[1] = self.gamma[input_pixel[1]]
        output_pixel[2] = self.gamma[input_pixel[2]]
        return output_pixel
    	
    def run(self):
        spidev = file(self.deviceName, "wb")

        print ("Start RGB Tester " + str(self.num_leds) + "leds in " + str(self.color_red) + ":" + str(self.color_green) + ":" + str(self.color_blue))
        
        pixels = bytearray(self.num_leds * PIXEL_SIZE)
        
        for pixel_index in range(self.num_leds):
            pixel_to_adjust = bytearray(PIXEL_SIZE)
            pixel_to_adjust.append(self.color_red)
            pixel_to_adjust.append(self.color_green)
            pixel_to_adjust.append(self.color_blue)

            pixel_to_filter = self.correct_pixel_brightness(pixel_to_adjust)

            pixels[((pixel_index)*PIXEL_SIZE):] = self.filter_pixel(pixel_to_filter[:], 1)

        spidev.write(pixels)
        spidev.flush()

def defineCliArguments(controller):
    parser = argparse.ArgumentParser(add_help=True,version='1.0', prog='pixelpi.py')
    parser.add_argument('--r', action='store', dest='color_red', default='255', help='Specify the red amount')
    parser.add_argument('--g', action='store', dest='color_green', default='255', help='Specify the green amount')
    parser.add_argument('--b', action='store', dest='color_blue', default='255', help='Specify the blue amount')
    parser.add_argument('--verbose', action='store_true', dest='verbose', default=True, help='enable verbose mode')
    parser.add_argument('--spi_dev', action='store', dest='spi_dev_name', required=False, default='/dev/spidev0.0', help='Set the SPI device descriptor')
    parser.add_argument('--num_leds', action='store', dest='num_leds', required=True, default='96', help='The number of LEDs')

    args = parser.parse_args()


    controller.deviceName = args.spi_dev_name
    controller.num_leds = args.num_leds
    controller.verbose = args.verbose
    controller.color_red = args.color_red
    controller.color_blue = args.color_blue
    controller.color_green = args.color_green

if __name__ == '__main__':
    print "starting..."
    
    controller = RGBController()
    defineCliArguments(controller)
    controller.run()

    print "shuting down..."
