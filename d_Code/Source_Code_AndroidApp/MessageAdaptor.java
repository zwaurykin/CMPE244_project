package com.sjsu.edu.myapplication;

import android.util.Log;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import java.nio.charset.StandardCharsets;

public class MessageAdaptor {
    private String brokerUri = "tcp://broker.hivemq.com:1883";
    private String topic = "Sindhu_244";
    private final String TAG = "HiveMQ1";
    private MqttClient client = null;
    private MessageSubscribeInterface subscriber;

    public interface MessageSubscribeInterface {
        void handleMessage(String message);
    }

    public MessageAdaptor(MessageSubscribeInterface subscriber) {
        this.subscriber = subscriber;
    }

    public void publishMessage(String messageStr) {
        try {
            client.publish(topic, messageStr.getBytes(StandardCharsets.UTF_8), 2, false);
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void subscribeAndConnectToMqtt(boolean alsoSubscribe) {
        try {
            client = new MqttClient(brokerUri, MqttClient.generateClientId(), new MemoryPersistence());
            if(alsoSubscribe) {
                client.setCallback(new MqttCallback() {
                    @Override
                    public void connectionLost(Throwable cause) {
                    }

                    @Override
                    public void messageArrived(String topic, MqttMessage message) throws Exception {
                        String payload = new String(message.getPayload());
                        if(subscriber != null) {
                            subscriber.handleMessage(payload);
                        }
                    }

                    @Override
                    public void deliveryComplete(IMqttDeliveryToken token) {
                    }
                });
            }
            client.connect();
            client.subscribe(topic, 2);
            Log.i(TAG, "isConnected: " + client.isConnected());
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public void disconnect(){
        try {
            client.unsubscribe(topic);
            client.disconnect();
        } catch (MqttException e) {
            throw new RuntimeException(e);
        }
    }
}
