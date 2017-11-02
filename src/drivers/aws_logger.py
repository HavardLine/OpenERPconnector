'''
/*
 * Copyright 2010-2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */
 '''

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging
import time
from os import path, environ, name

# Get path to client-files
if name == 'nt':
    path_iot = path.join(environ['localappdata'], "LTS AS", "iot")
else:
    path_iot = environ['HOMEPATH']+"/config/iot/"

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(0)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s:%(message)s")
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# General message notification callback
def customOnMessage(message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


# Suback callback
def customSubackCallback(mid, data):
    print("Received SUBACK packet id: ")
    print(mid)
    print("Granted QoS: ")
    print(data)
    print("++++++++++++++\n\n")


# Puback callback
def customPubackCallback(mid):
    print("Received PUBACK packet id: ")
    print(mid)
    print("++++++++++++++\n\n")

host = "a3hdhr3r3b1d8r.iot.eu-central-1.amazonaws.com"
rootCAPath = path.join(path_iot, 'root-CA.crt')
certificatePath = path.join(path_iot, 'certificate.pem.crt')
privateKeyPath = path.join(path_iot, 'private.pem.key')
useWebsocket = False
clientId = "no-lts-ws1"
topic = "LOGGING"

if useWebsocket and certificatePath and privateKeyPath:
    logger.error("X.509 cert authentication and WebSocket are mutual exclusive. Please pick one.")
    exit(2)

if not useWebsocket and (not certificatePath or not privateKeyPath):
    logger.error("Missing credentials for authentication.")
    exit(2)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, 443)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
myAWSIoTMQTTClient.onMessage = customOnMessage

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
# Note that we are not putting a message callback here. We are using the general message notification callback.
myAWSIoTMQTTClient.subscribeAsync(topic, 1, ackCallback=customSubackCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while loopCount < 9:
   myAWSIoTMQTTClient.publishAsync(topic, "New Message " + str(loopCount), 1, ackCallback=customPubackCallback)
   loopCount += 1
   time.sleep(1)

if(__name__=="__main__"):
    print(path_iot)

