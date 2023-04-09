#!/usr/bin/python

from logs import log
import pyudev
import evdev

# wait for reader to connect
def waitForDevice():
    print ( "Wait for device..." )
    # Create a context object
    context = pyudev.Context()
    # Create a monitor object for USB devices
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')
    # Start the monitor
    monitor.start()
    # Wait for a new USB device to be connected
    for device in iter(monitor.poll, None):
        if device.action == 'add':
            return device

def searchDevice(  ):
    listDevices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    try:
        for device in listDevices:
            device.grab()
            # check if device is HID device (data as keyword)
            if evdev.ecodes.EV_KEY in device.capabilities(verbose=False):
                # check if the device is has RFID signe in device name and if is usb
                if device and "usb" in device.phys and "RFID" or "rfid" in device.name:
                    log().info( 'Reader started: %s', device.name )
                    print ( device.name )
                    return device
            device.close()
    except:
            pass