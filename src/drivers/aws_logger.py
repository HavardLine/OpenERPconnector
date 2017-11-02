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

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import logging, json
import time
from os import path, environ, name

class BananaHandler(logging.Handler):
    mqtt_client = None

    def __init__(self):
        logging.Handler.__init__(self)

        # Get path to client-files
        if name == 'nt':
            path_iot = path.join(environ['localappdata'], "LTS AS", "iot")
        else:
            path_iot = environ['HOMEPATH']+"/config/iot/"

        host = 'a3hdhr3r3b1d8r.iot.eu-central-1.amazonaws.com'
        rootCAPath = path.join(path_iot, 'root-CA.crt')
        certificatePath = path.join(path_iot, 'certificate.pem.crt')
        privateKeyPath = path.join(path_iot, 'private.pem.key')
        clientId = "no-lts-ws2"

        # Init AWSIoTMQTTClient
        self.mqtt_client = AWSIoTMQTTShadowClient(clientId)
        self.mqtt_client.configureEndpoint(host, 8883)
        self.mqtt_client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

        # AWSIoTMQTTClient connection configuration
        self.mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
        self.mqtt_client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.mqtt_client.configureMQTTOperationTimeout(5)  # 5 sec

        # Connect
        self.mqtt_client.connect()

        # Create a deviceShadow with persistent subscription
        self.deviceShadowHandler = self.mqtt_client.createShadowHandlerWithName(clientId, True)


    def emit(self, record):
        # Custom Shadow callback
        def customShadowCallback_Update(payload, responseStatus, token):
            # payload is a JSON string ready to be parsed using json.loads(...)
            # in both Py2.x and Py3.x
            if responseStatus == "timeout":
                print("Update request " + token + " time out!")
            if responseStatus == "accepted":
                payloadDict = json.loads(payload)
                print("~~~~~~~~~~~~~~~~~~~~~~~")
                print("Update request with token: " + token + " accepted!")
                print("property: " + str(payloadDict["state"]["desired"]["property"]))
                print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
            if responseStatus == "rejected":
                print("Update request " + token + " rejected!")

        def customShadowCallback_Delete(payload, responseStatus, token):
            if responseStatus == "timeout":
                print("Delete request " + token + " time out!")
            if responseStatus == "accepted":
                print("~~~~~~~~~~~~~~~~~~~~~~~")
                print("Delete request with token: " + token + " accepted!")
                print("~~~~~~~~~~~~~~~~~~~~~~~\n\n")
            if responseStatus == "rejected":
                print("Delete request " + token + " rejected!")


        self.format(record)

        payload = {'reported': {
                'timedate': record.asctime,
                'name': record.name,
                'levelname': record.levelname,
                'msg': record.msg
            }
        }
        payload = {"state":{"desired":{"property": "egenskap"}}}
        print(json.dumps(payload))
        #self.deviceShadowHandler.shadowDelete(customShadowCallback_Delete, 5)

        self.deviceShadowHandler.shadowUpdate(json.dumps(payload), customShadowCallback_Update, 5)

#Test-code for module
if __name__ == '__main__':
        # Configure logging
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = BananaHandler()
        formatter = logging.Formatter(datefmt=None, fmt="%(asctime)s:%(name)s:%(levelname)s:%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info('info message')