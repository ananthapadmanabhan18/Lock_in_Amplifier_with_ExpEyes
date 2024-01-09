##################### List of functions for Expeyes #####################

import eyes17.eyes

p=eyes17.eyes.open()    # open the serial port
p.set_pv1(1.5)          # set the voltage of PV1 to 1.5 V
p.set_pv2(2.5)          # set the voltage of PV2 to 2.5 V
v=p.get_voltage('SEN')  # get the voltage of SEN



