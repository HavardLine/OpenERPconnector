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
import logging, json
from os import path, environ, name

class MqttHandler(logging.Handler):
    mqtt_client = None
    message_buffer = []

    def __init__(self):
        logging.Handler.__init__(self)

        # Get path to client-files
        if name == 'nt':
            path_iot = path.join(environ['localappdata'], "LTS AS", "iot")
        else:
            path_iot = environ['HOMEPATH']+"/config/iot/"

        with open(path.join(path_iot, 'conf.json'), "r") as f:
            config = json.loads(f.read())

        host = config['host']
        self.client_id = config['client_id']
        rootCAPath = path.join(path_iot, 'root-CA.crt')
        certificatePath = path.join(path_iot, 'certificate.pem.crt')
        privateKeyPath = path.join(path_iot, 'private.pem.key')

        # Init AWSIoTMQTTClient
        self.mqtt_client = AWSIoTMQTTClient(self.client_id)
        self.mqtt_client.configureEndpoint(host, 8883)
        self.mqtt_client.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

        # AWSIoTMQTTClient connection configuration
        self.mqtt_client.configureAutoReconnectBackoffTime(1, 32, 20)
        self.mqtt_client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.mqtt_client.configureMQTTOperationTimeout(5)  # 5 sec

        # Connect
        self.mqtt_client.connect()

    def emit(self, record):
        print(self.format(record))
        payload = {
                'timedate': record.asctime,
                'name': record.name,
                'levelname': record.levelname,
                'msg': record.msg
        }
        self.message_buffer.append(payload)

    def publish_to_shadow(self, property_name):
        # Publishing all events that are acumulated in the MqttHandler object
        token = '$aws/things/' + self.client_id + '/shadow/update'
        data = '{"state": {"reported": {"' + property_name + '":' + json.dumps(self.message_buffer) + '} } }'
        print(property_name, token, data)
        self.mqtt_client.publish(token, data, 1)  

#Test-code for module
if __name__ == '__main__':
        # Configure logging
        logger = logging.getLogger('logger/test')
        logger.setLevel(logging.INFO)
        handler = MqttHandler()
        formatter = logging.Formatter(datefmt=None, fmt="%(asctime)s:%(name)s:%(levelname)s:%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.info('this is an info message')
        handler.publish_to_shadow(logger.name)
