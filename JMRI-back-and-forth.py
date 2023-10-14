# This is an example script for a JMRI "Automat" in Python
# It is based on the AutomatonExample.
#
# It runs a loco back and forth on a timer forever
#
# Author:  Adam Knowles 2023 based on Howard Watkins, January 2007.

import jarray # for java array # type: ignore
import jmri # for sensors, turnouts, etc # type: ignore

RUN_FOR = 5 * 1000 # seconds
WAIT_FOR = 1 * 1000 # seconds
SPEED_SETTING = 0.7

class Test(jmri.jmrit.automat.AbstractAutomaton):
    def __init__(self, locoAddress):
        print("init(self)")
        # super().__init__()
        self.locoAddress = locoAddress

        # get loco address. For long address change "False" to "True"
        self.throttle = self.getThrottle(self.locoAddress, False)

        return

    def handle(self):
        # handle() is called repeatedly until it returns false.
        print("handle(self)")

        # set loco to forward
        print("Set Loco Forward")
        self.throttle.setIsForward(True)

        # wait for layout to catch up
        print("Wait for {} seconds".format(WAIT_FOR / 1000))
        self.waitMsec(WAIT_FOR)
        print("Set speed to {}".format(SPEED_SETTING))
        self.throttle.setSpeedSetting(SPEED_SETTING)

        # Run for a moment, then stop
        print("Run for {} seconds".format(RUN_FOR / 1000))
        self.waitMsec(RUN_FOR)
        print("Set speed: Stop")
        self.throttle.setSpeedSetting(0)

        # set direction to reverse, set speed
        print("Set Loco Reverse")
        self.throttle.setIsForward(False)
        # wait for layout to catch up
        print("Wait for {} seconds".format(WAIT_FOR / 1000))
        self.waitMsec(WAIT_FOR)           
        print("Set speed to {}".format(SPEED_SETTING))
        self.throttle.setSpeedSetting(SPEED_SETTING)

        # wait, stop, wait
        print("Run for {} seconds".format(RUN_FOR / 1000))
        self.waitMsec(RUN_FOR)
        print("Set speed: Stop")
        self.throttle.setSpeedSetting(0)
        print("Wait for {} seconds".format(WAIT_FOR / 1000))
        self.waitMsec(WAIT_FOR)

        # Loop
        print("End of Loop")
        return 1

# end of class definition

# start one of these up
Test(3).start()