package com.sjsu.edu.myapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.RadioGroup;
import android.widget.TextView;
import android.widget.Toast;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;

public class MainActivity extends AppCompatActivity implements MessageAdaptor.MessageSubscribeInterface {
    MessageAdaptor messageAdaptor = null;
    private final String TAG = "MainActivityTag";
    private Button sendButton = null;
    private EditText angleET = null;
    private EditText freqET = null;
    private EditText dutyCycleET = null;
    private RadioGroup rotationRadioGroup = null;

    private TextView magneMx = null;
    private TextView magneMy = null;
    private TextView magneMz = null;
    private TextView accelMx = null;
    private TextView accelMy = null;
    private TextView accelMz = null;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        messageAdaptor = new MessageAdaptor(this);

        messageAdaptor.subscribeAndConnectToMqtt(true);
//        new Handler().postDelayed(() -> {
//            messageAdaptor.publishMessage("Message 1");
//            messageAdaptor.publishMessage("Message 2");
//            messageAdaptor.publishMessage("Message 3");
//            messageAdaptor.publishMessage("Message 4");
//        }, 3000);

        magneMx = findViewById(R.id.magneMx);
        magneMy = findViewById(R.id.magneMy);
        magneMz = findViewById(R.id.magneMz);
        accelMx = findViewById(R.id.accelMx);
        accelMy = findViewById(R.id.accelMy);
        accelMz = findViewById(R.id.accelMz);

        sendButton = findViewById(R.id.sendBtn);
        angleET = findViewById(R.id.angle);
        freqET = findViewById(R.id.frequency);
        dutyCycleET = findViewById(R.id.dutyCycle);
        rotationRadioGroup = findViewById(R.id.rotationRadioGroup);
        sendButton.setOnClickListener(view -> handleSend());
    }

    private void handleSend() {
        if(angleET.getText().toString().isEmpty()
                || freqET.getText().toString().isEmpty()
                || freqET.getText().toString().isEmpty()) {
            Toast.makeText(this, "Some field(s) are missing", Toast.LENGTH_SHORT).show();
            return;
        }
        int selectedRotationId = rotationRadioGroup.getCheckedRadioButtonId();
        boolean isClockwise = selectedRotationId == R.id.rotationClockwise;
        String data = angleET.getText().toString()
                + "," + (isClockwise ? "clockwise" : "anticlockwise")
                + "," + freqET.getText().toString()
                + "," + dutyCycleET.getText().toString();
        messageAdaptor.publishMessage(data);
    }

    @Override
    public void handleMessage(String message) {
        message = message.replace(" ", "");
        String[] messageParts = message.split(",");
        if(messageParts.length == 6) {
            magneMx.setText(messageParts[0]);
            magneMy.setText(messageParts[1]);
            magneMz.setText(messageParts[2]);
            accelMx.setText(messageParts[3]);
            accelMy.setText(messageParts[4]);
            accelMz.setText(messageParts[5]);
        }
        Log.i(TAG, "Message: " + message);
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        if(messageAdaptor != null) messageAdaptor.disconnect();
    }
}