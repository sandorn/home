package com.example.kevin_liu.myapplication

import android.annotation.SuppressLint
import android.content.Context
import android.support.v7.app.AppCompatActivity
import android.os.Bundle
import android.os.Handler
import android.os.Message
import android.util.Log
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import com.ftdi.j2xx.D2xxManager;
import com.ftdi.j2xx.FT_Device;

class MainActivity : AppCompatActivity() {

    lateinit var ftDev: FT_Device
    lateinit var ftdid2xx: D2xxManager
    var DeviceUARTContext: Context? = null
    private lateinit var handler: Handler
    var uart_configured = false
    var iavailable:Int = 0
    private var Receiver:String = ""


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val Bt_Search:Button = findViewById(R.id.button1)
        val Bt_Config:Button = findViewById(R.id.button2)
        val Bt_Send:Button = findViewById(R.id.button3)
        val Text_Send:EditText= findViewById(R.id.editText_s)
        val Text_Reciver:TextView = findViewById(R.id.textView_r)


        DeviceUARTContext = this
        ftdid2xx = D2xxManager.getInstance(this)

        Bt_Search.setOnClickListener {
            var tempDevCount = ftdid2xx?.createDeviceInfoList(DeviceUARTContext)

            Toast.makeText(this,"$tempDevCount",1).show()
        }

        Bt_Config.setOnClickListener {
            val tmpProtNumber = 0
            ftDev = ftdid2xx?.openByIndex(DeviceUARTContext, 0);
            if(ftDev == null)
            {
                Toast.makeText(DeviceUARTContext,"open device port("+tmpProtNumber+") NG, ftDev == null", Toast.LENGTH_LONG).show();
                uart_configured = false
                return@setOnClickListener
            }

            if (ftDev?.isOpen() == true)
            {
                Toast.makeText(DeviceUARTContext, "open device port(" + tmpProtNumber + ") OK", Toast.LENGTH_SHORT).show();
                SetConfig(9600, 8, 1, 0, 0)
                uart_configured = true
//                if(false == bReadThreadGoing)
//                {
//                    read_thread = new readThread(handler);
//                    read_thread.start();
//                    bReadThreadGoing = true;
//                }
                readThread().start()
            }
            else
            {
                Toast.makeText(DeviceUARTContext, "open device port(" + tmpProtNumber + ") NG", Toast.LENGTH_LONG).show();
                uart_configured = false
                //Toast.makeText(DeviceUARTContext, "Need to get permission!", Toast.LENGTH_SHORT).show();
            }
        }

        Bt_Send.setOnClickListener {
            val to_send:ByteArray = Text_Send.getText().toString().toByteArray()
            val retval = ftDev?.write(to_send, to_send.size)//写数据，第一个参数为需要发送的字节数组，第二个参数为需要发送的字节长度，返回实际发送的字节长度
            if (retval!! < 0){
                Toast.makeText(this@MainActivity, "写失败!", Toast.LENGTH_SHORT).show()
            }

        }
        handler = @SuppressLint("HandlerLeak")
        object : Handler() {
            override fun handleMessage(msg: Message) {
                Text_Reciver.setText(Receiver)
            }
        }

    }

    fun SetConfig(baud: Int, dataBits: Int, stopBits: Int, parity: Int, flowControl: Int) {
        var dataBits = dataBits
        var stopBits = stopBits
        var parity = parity
        if (ftDev?.isOpen() === false) {
            Log.e("j2xx", "SetConfig: device not open")
            return
        }

        // configure our port
        // reset to UART mode for 232 devices
        ftDev?.setBitMode(0.toByte(), D2xxManager.FT_BITMODE_RESET)

        ftDev?.setBaudRate(baud)

        when (dataBits) {
            7 -> dataBits = D2xxManager.FT_DATA_BITS_7.toInt()
            8 -> dataBits = D2xxManager.FT_DATA_BITS_8.toInt()
            else -> dataBits = D2xxManager.FT_DATA_BITS_8.toInt()
        }

        when (stopBits) {
            1 -> stopBits = D2xxManager.FT_STOP_BITS_1.toInt()
            2 -> stopBits = D2xxManager.FT_STOP_BITS_2.toInt()
            else -> stopBits = D2xxManager.FT_STOP_BITS_1.toInt()
        }

        when (parity) {
            0 -> parity = D2xxManager.FT_PARITY_NONE.toInt()
            1 -> parity = D2xxManager.FT_PARITY_ODD.toInt()
            2 -> parity = D2xxManager.FT_PARITY_EVEN.toInt()
            3 -> parity = D2xxManager.FT_PARITY_MARK.toInt()
            4 -> parity = D2xxManager.FT_PARITY_SPACE.toInt()
            else -> parity = D2xxManager.FT_PARITY_NONE.toInt()
        }

        ftDev?.setDataCharacteristics(dataBits.toByte(), stopBits.toByte(), parity.toByte())

        val flowCtrlSetting: Short
        when (flowControl) {
            0 -> flowCtrlSetting = D2xxManager.FT_FLOW_NONE
            1 -> flowCtrlSetting = D2xxManager.FT_FLOW_RTS_CTS
            2 -> flowCtrlSetting = D2xxManager.FT_FLOW_DTR_DSR
            3 -> flowCtrlSetting = D2xxManager.FT_FLOW_XON_XOFF
            else -> flowCtrlSetting = D2xxManager.FT_FLOW_NONE
        }

        // TODO : flow ctrl: XOFF/XOM
        // TODO : flow ctrl: XOFF/XOM
        ftDev?.setFlowControl(flowCtrlSetting, 0x0b.toByte(), 0x0d.toByte())

        Toast.makeText(DeviceUARTContext, "Config done", Toast.LENGTH_SHORT).show()
    }

    private inner class readThread : Thread() {
        val buffer = ByteArray(4096)
        override fun run() {


            while (true) {
                val msg = Message.obtain()
                if (!uart_configured) {
                    break
                }
                iavailable = ftDev.getQueueStatus();
                ftDev?.read(buffer, iavailable)
                if (iavailable > 0) {
                    Receiver = String(buffer)
                    handler.sendMessage(msg)
                }
            }
        }
    }
}
