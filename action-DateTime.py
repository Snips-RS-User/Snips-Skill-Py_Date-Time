#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
from hermes_python.hermes import Hermes
from hermes_python.ffi.utils import MqttOptions
from hermes_python.ontology import *
import io

# import datetime class
import time

# configuration
MQTT_ADDR = "localhost:1883"


CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(configparser.SafeConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()

def subscribe_intent_callback(hermes, intentMessage):
    conf = read_configuration_file(CONFIG_INI)
    action_wrapper(hermes, intentMessage, conf)


# #### Function define_time : define and translate time in text
def define_time():
    time_text=""
    time_object=time.localtime()
    hour=time_object.tm_hour
    if hour == 0:
        time_text += "minuit"
    elif hour == 1:
        time_text += "une heure"
    elif hour == 12:
        time_text += "midi"
    elif hour == 21:
        time_text += "vingt et une heures"  
    else:
        time_text += "{0} heures".format(hour)
    minute=time_object.tm_min
    if minute == 0:
        time_text += ""
    elif minute == 1:
        time_text += " une"
    elif minute == 21:
        time_text += " vingt et une"
    elif minute == 31:
        time_text += " trente et une" 
    elif minute == 41:
        time_text += " quarante et une" 
    elif minute == 31:
        time_text += " cinquante et une"    
    else:
        time_text += " {0}".format(minute)
    return time_text


# #### Actions
def action_wrapper(hermes, intentMessage, conf):
    #if intentMessage.intent.intent_name == "Snips-RS-User:askTime":
        hermes.publish_end_session(intentMessage.session_id, define_time())


if __name__ == "__main__":
    mqtt_opts = MqttOptions()
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intent("Snips-RS-User:askTime", subscribe_intent_callback) \
         .start()


