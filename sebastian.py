## ETTDirectControl API sample with Python

# last updated: 05/04/2026

# additional samples: emergingtechtrans.com / ettllc.net

# support: support@emergingtechtrans.com

import sys #

import time # for time.sleep

 

# reference to .NET clr

# this line requires to install python.net library via:

# pip install pythonnet

import clr

# add reference to ETTDirectControl/ETTAPI/ETTAPI.dll

# the dll in the sub folder ETTAPI of ETTDirectControl will be updated automatically

# other locations have to be maintained manually

clr.AddReference(r"C:\Program Files\ETTDirectControl\ETTAPI\ETTAPI.dll")

from System import Int32,Int64, Boolean, String

# dll import

from ETTAPI import ETTDeviceAPI

Device=ETTDeviceAPI()

bool_SetChannel = Device.SetChannel.__overloads__[Int32, Boolean, String]

int_SetChannel = Device.SetChannel.__overloads__[Int32, Int64, String]

 

# initialize object

 

olfAddress=""

# insert IP address in place of '127.0.0.1' for remote host

Device.Connect("127.0.0.1")  

 

if Device.IsConnected:

    print("success")      

    Device.ResetState()  

    Device.SubscribeToInhalationEvents(True,True)

else:

    print("Please try to connect to ETTDC again")

deviceList=Device.ScanDeviceList()

print(deviceList)

#if deviceList is "":

for device in deviceList:

    print(device)

    if("Olfactometer" in device.split('.')[1]):

        Device.CloseAllChannels()

        print("found an olfactometer")

        olfAddress=device.split('.')[0]

        bool_SetChannel(1,True,olfAddress)

        time.sleep(1)

        bool_SetChannel(1,False,olfAddress)

        time.sleep(1)

        bool_SetChannel(2,True,olfAddress)

        time.sleep(1)

        bool_SetChannel(2,False,olfAddress)

        time.sleep(1)

        Device.SetChannel(2,1500,olfAddress)

        time.sleep(1)

        Device.SetChannel(1,1050,olfAddress)

        time.sleep(1)

        Device.SetChannel(4,1200,olfAddress)

        time.sleep(1)

        Device.SetChannel(3,1400,olfAddress)

        time.sleep(1)

        Device.SetChannel(5,1300,olfAddress)

        time.sleep(1)

        Device.SetChannel(6,1100,olfAddress)

        time.sleep(1)

   

time.sleep(3) # give the program enough time for the last valve to close

Device.SaveRespirationData()

 

#else:

#    print("Connection established but no device found")