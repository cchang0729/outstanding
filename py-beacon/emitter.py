#
# by Taka Wang
#

import paho.mqtt.client as mqtt
import time, ConfigParser, json
import MySQLdb
from proximity import *
from websocket import create_connection

DEBUG = True
calculator = 0
conf  = 0

def initDatabase():
    db=MySQLdb.connect(host="localhost",port=3306,user="root",passwd="root",db="outstanding")
    db.query("set character_set_connection=utf8;")
    db.query("set character_set_server=utf8;")
    db.query("set character_set_client=utf8;")
    db.query("set character_set_results=utf8;")
    db.query("set character_set_database=utf8;")
    return db

def onConnect(client, userdata, rc):
    """MQTT onConnect handler"""
    print("Connected to broker: " + str(rc))
    client.subscribe(conf["topic_id"] + "#")

def onMessage(client, userdata, msg):
    """MQTT subscribe handler
    Push new beacon info to calculator for proximity calculation
    """
    obj = json.loads(msg.payload) # decode json string
    calculator.add(obj["id"], int(obj["val"]))

def initMQTT(url = "localhost", port = 1883, keepalive = 60):
    """Init MQTT connection"""
    client = mqtt.Client()
    client.on_connect = onConnect
    client.on_message = onMessage
    try:
        client.connect(url, port, keepalive)
        client.loop_start()
        return client
    except Exception, e:
        print(e)
        return None

def init():
    """Read config file"""
    ret = {}
    config = ConfigParser.ConfigParser()
    config.read("config")
    global DEBUG
    DEBUG = True if int(config.get('Emitter', 'debug')) == 1 else False
    ret["url"]           = config.get('MQTT', 'url')
    ret["port"]          = int(config.get('MQTT', 'port'))
    ret["keepalive"]     = int(config.get('MQTT', 'keepalive'))
    ret["queueCapacity"] = int(config.get('Calculator', 'queueCapacity'))
    ret["chkTimer"]      = int(config.get('Calculator', 'chkTimer'))
    ret["threshold"]     = int(config.get('Calculator', 'threshold'))
    ret["topic_id"]      = config.get('Scanner', 'topic_id')
    ret["nearest_id"]    = config.get('Scanner', 'nearest_id')
    ret["topic_id_len"]  = len(ret["topic_id"])
    ret["sleepInterval"] = int(config.get('Emitter', 'sleepInterval'))
    return ret

if __name__ == '__main__':
    conf = init()
    db = initDatabase()
    cursor = db.cursor()
    calculator = Calculator(conf["queueCapacity"], conf["chkTimer"], conf["threshold"])
    clnt = initMQTT(conf["url"], conf["port"], conf["keepalive"])
    while True:
        time.sleep(conf["sleepInterval"])
        for key, erssi in calculator.eRssi.iteritems():
            print "UPDATE distance SET distance='%d', timestamp='%f' WHERE beacon_uuid='%s' and artik_type='%s'"%(erssi,time.time(),key.upper(), "ARTIK-50")
            cursor.execute("UPDATE distance SET distance='%d', timestamp='%f' WHERE beacon_uuid='%s' and artik_type='%s'"%(erssi,time.time(),key.upper(), "ARTIK-50"))
            db.commit()
            cursor.execute("SELECT * FROM distance")
            cursor.fetchall()
#        ret, val = calculator.nearest()
#        if ret:
#            clnt.publish(conf["nearest_id"], str('{"id":"%s","val":"%s"}' % (ret, val)))
#        if DEBUG: print(ret, val)
        
