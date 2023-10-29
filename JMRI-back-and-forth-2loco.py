# This is an example script for a JMRI "Automat" in Python
# It is based on the AutomatonExample.
#
# It runs two locos back and forth on a timer forever
#
# Author:  Adam Knowles 2023 based on Howard Watkins, January 2007.

import jarray # for java array # type: ignore
import jmri # for sensors, turnouts, etc # type: ignore

# Configure trains
SHUNTER_LOCO_ID = 9744
ROYALSCOT_LOCO_ID = 6106
LONG_ADDRESS = True

RUN_FOR = 5 * 1000 # seconds
WAIT_FOR = 1 * 1000 # seconds
SPEED_SETTING = 0.7

class Test(jmri.jmrit.automat.AbstractAutomaton):
    def __init__(self, ShunterLocoAddress, RoyalScotLocoAddress):
        print("init(self)")
        # super().__init__()
        self.shunterLocoAddress = ShunterLocoAddress
        self.royalscotLocoAddress = RoyalScotLocoAddress

        # get loco addresses. For long address change "False" to "True"
        self.shunterThrottle = self.getThrottle(self.shunterLocoAddress, LONG_ADDRESS)
        self.royalscotThrottle = self.getThrottle(self.royalscotLocoAddress, LONG_ADDRESS)

        return

    def handle(self):
        # handle() is called repeatedly until it returns false.
        print("handle(self)")

        # set Shunter loco to forward
        print("Set Shunter Loco Forward")
        self.shunterThrottle.setIsForward(True)
        # set Tank loco to reverse
        print("Set Tank Loco Reverse")
        self.royalscotThrottle.setIsForward(False)

        # wait for layout to catch up
        print("Wait for {} seconds".format(WAIT_FOR / 1000))
        self.waitMsec(WAIT_FOR)

        # set speed
        print("Set speed to {}".format(SPEED_SETTING))
        self.shunterThrottle.setSpeedSetting(SPEED_SETTING)
        self.royalscotThrottle.setSpeedSetting(SPEED_SETTING)

        # Run for a moment, then stop
        print("Run for {} seconds".format(RUN_FOR / 1000))
        self.waitMsec(RUN_FOR)
        print("Set speed: Stop")
        self.shunterThrottle.setSpeedSetting(0)
        self.royalscotThrottle.setSpeedSetting(0)

        # set Shunter loco to reverse
        print("Set Shunter Loco Reverse")
        self.shunterThrottle.setIsForward(False)
        # set Tank loco to forward
        print("Set Tank Loco Forward")
        self.royalscotThrottle.setIsForward(True)

        # wait for layout to catch up
        print("Wait for {} seconds".format(WAIT_FOR / 1000))
        self.waitMsec(WAIT_FOR)

        # set speed
        print("Set speed to {}".format(SPEED_SETTING))
        self.shunterThrottle.setSpeedSetting(SPEED_SETTING)
        self.royalscotThrottle.setSpeedSetting(SPEED_SETTING)

        # wait, stop, wait
        print("Run for {} seconds".format(RUN_FOR / 1000))
        self.waitMsec(RUN_FOR)
        print("Set speed: Stop")
        self.shunterThrottle.setSpeedSetting(0)
        self.royalscotThrottle.setSpeedSetting(0)
        print("Wait for {} seconds".format(WAIT_FOR / 1000))
        self.waitMsec(WAIT_FOR)

        return True
    
# start one of these up
Test(SHUNTER_LOCO_ID, ROYALSCOT_LOCO_ID).start()