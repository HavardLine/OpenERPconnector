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

import time, json
from os import path, environ, name
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("--start--")
    shadow_state = json.loads(message.payload)
    for value in shadow_state['state']['reported']:
        for element in shadow_state['state']['reported'][value]:
            print(element['timedate'][:-4], element['msg'])
    print("--end--")
    
# Get path to client-files
if name == 'nt':
    path_iot = path.join(environ['localappdata'], "LTS AS", "iot")
else:
    path_iot = environ['HOMEPATH']+"/config/iot/"

with open(path.join(path_iot, 'conf.json'), "r") as f:
    config = json.loads(f.read())

host = config['host']
rootCAPath = path.join(path_iot, 'root-CA.crt')
certificatePath = path.join(path_iot, 'certificate.pem.crt')
privateKeyPath = path.join(path_iot, 'private.pem.key')
client_id = config['client_id']

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
myAWSIoTMQTTClient = AWSIoTMQTTClient(client_id)
myAWSIoTMQTTClient.configureEndpoint(host, 8883)
myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe('$aws/things/no-lts-ws1/shadow/get/accepted', 1, customCallback)

# Publish to the same topic in a loop forever
myAWSIoTMQTTClient.publish('$aws/things/no-lts-ws1/shadow/get', None, 1)


time.sleep(5)