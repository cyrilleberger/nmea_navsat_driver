#! /usr/bin/env python3

# Software License Agreement (BSD License)
#
# Copyright (c) 2013, Eric Perko
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above
#    copyright notice, this list of conditions and the following
#    disclaimer in the documentation and/or other materials provided
#    with the distribution.
#  * Neither the names of the authors nor the names of their
#    affiliated organizations may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

def nmea_serial_driver():
    import serial

    import rclpy
    import rclpy.utilities
    import rclpy.exceptions
    import argparse

    import libnmea_navsat_driver.driver
    
    parser = argparse.ArgumentParser(description='driver for nmea GPS.')

    parser.add_argument('--baud', type=int, default=4800)
    parser.add_argument('--port', type=str, default='/dev/ttyUSB0')
    parser.add_argument('--frame_id', type=str, default='gps')
    parser.add_argument('--time_ref_source', type=str, default=None)
    parser.add_argument('--useRMC', action='store_true', default=False)
    parser.add_argument('rosargs', type=str, nargs='+')

    args = parser.parse_args()
    
    rclpy.init(args=args.rosargs)

    serial_port = args.port
    serial_baud = args.baud
    
    frame_id = libnmea_navsat_driver.driver.RosNMEADriver.get_frame_id(args.frame_id)

    GPS = serial.Serial(port=serial_port, baudrate=serial_baud, timeout=2)
    driver = libnmea_navsat_driver.driver.RosNMEADriver(args.time_ref_source, args.useRMC)
    while rclpy.utilities.ok():
        data = GPS.readline().strip()
        try:
            driver.add_sentence(data.decode('ascii'), frame_id)
            rclpy.spin_once(driver)
        except ValueError as e:
            driver.get_logger().warn("Value error, likely due to missing fields in the NMEA message. Error was: %s. Please report this issue at github.com/ros-drivers/nmea_navsat_driver, including a bag file with the NMEA sentences that caused it." % e)

    GPS.close() #Close GPS serial port

if __name__ == '__main__':
    nmea_serial_driver()
