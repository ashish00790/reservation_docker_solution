#!/usr/bin/env python
# coding: utf-8

# In[4]:


from kafka import KafkaConsumer, KafkaProducer
import os
import json
from time import sleep
import pandas as pd


# In[3]:

# setting the environment variables
KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL")
TRANSACTIONS_TOPIC = os.environ.get("TRANSACTIONS_TOPIC")
OUTPUT_TOPIC = os.environ.get("OUTPUT_TOPIC")  

#consume the topic from kafka
consumer = KafkaConsumer (TRANSACTIONS_TOPIC,bootstrap_servers = KAFKA_BROKER_URL ,enable_auto_commit=True, auto_offset_reset='earliest', value_deserializer=lambda m: json.loads(m.decode('utf-8')))
currency = ['GBP', 'USD', 'INR', 'CNY']

#produce the output data into kafka topic 
producer = KafkaProducer(bootstrap_servers = KAFKA_BROKER_URL,value_serializer=lambda v: json.dumps(v).encode('utf-8'))


for message in consumer:
    new = pd.DataFrame.from_dict(message[6])
    if(new['currency'][0] == 'CYN'):
        new['normalised_booking_amount'] = new['booking_amount'][0]*0.1
    elif(new['currency'][0] == 'INR'):
        new['normalised_booking_amount'] = new['booking_amount'][0]*0.01
    elif(new['currency'][0] == 'USD'):
        new['normalised_booking_amount'] = new['booking_amount'][0]*0.8
    else:
        new['normalised_booking_amount'] = new['booking_amount'][0]*1.10
    new['normalised_currency'] = 'EUR'
    
    json_data = new.to_json(orient ='records')
    producer.send(OUTPUT_TOPIC, value=json_data)
    print(json_data) # DEBUG


# In[ ]:




