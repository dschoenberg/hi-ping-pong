#!/usr/bin/env python



class decoder:
    """Class to decode mechanical rotary encoder pulses."""
    def __init__(self, GPIO, gpioA, gpioB, callback):
        """
        Instantiate the class with the pi and gpios connected to
        rotary encoder contacts A and B.  The common contact
        should be connected to ground.  The callback is
        called when the rotary encoder is turned.  It takes
        one parameter which is +1 for clockwise and -1 for
        counterclockwise.
        """

        self.GPIO = GPIO
        self.gpioA = gpioA
        self.gpioB = gpioB
        self.callback = callback

        self.levA = 0
        self.levB = 0

        self.lastGpio = None

        self.GPIO.setup(self.gpioA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.GPIO.setup(self.gpioB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.GPIO.add_event_detect(self.gpioA, GPIO.BOTH, self._pulse)
        self.GPIO.add_event_detect(self.gpioB, GPIO.BOTH, self._pulse)

    def _pulse(self, pin, level, tick):
        """
        Decode the rotary encoder pulse.

                    +---------+         +---------+      0
                    |         |         |         |
            A       |         |         |         |
                    |         |         |         |
            +---------+         +---------+         +----- 1

                +---------+         +---------+            0
                |         |         |         |
            B   |         |         |         |
                |         |         |         |
            ----+         +---------+         +---------+  1
        """

        if pin == self.gpioA:
            self.levA = level
        else:
            self.levB = level

        if pin != self.lastGpio:  # debounce
            self.lastGpio = pin

            if pin == self.gpioA and level == 1:
                if self.levB == 1:
                    self.callback(1)
            elif pin == self.gpioB and level == 1:
                if self.levA == 1:
                    self.callback(-1)

    def cancel(self):
        """
        Cancel the rotary encoder decoder.
        """
        pass
        #self.cbA.cancel()
        #self.cbB.cancel()


if __name__ == "__main__":

    import time
    import RPi.GPIO as GPIO
    import RPi.GPIO as GPIO
    from time import sleep
    import rotary_encoder

    pos = 0

    def callback(way):
        global pos
        pos += way
        print("pos={}".format(pos))

    GPIO.setmode(GPIO.BOARD)

    decoder = rotary_encoder.decoder(GPIO, 10, 12, callback)
    time.sleep(300)
    decoder.cancel()
#    pi.stop()
