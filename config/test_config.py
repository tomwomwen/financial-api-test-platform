CONFIG = {
    "api": {
        "apifox_base_url": "http://127.0.0.1:4523/m1/6943198-6659588-default"
    },
    "test_data": {
        "default_amount": "0.01",
        "order_prefix": "TEST_",
        "refund_reason": "用户申请退款",
        "idempotent_order": "TEST_IDEMPOTENT_FIXED"
    },
    "mobile": {
        "appium_server_url": "http://localhost:4723",
        "devices": [
            {
                "name": "Pixel_4",
                "device_name": "emulator-5554",
                "app_package": "com.android.settings",
                "app_activity": ".Settings",
                "platform_name": "Android"
            },
            {
                "name": "Pixel_6",
                "device_name": "emulator-5556",
                "app_package": "com.android.settings",
                "app_activity": ".Settings",
                "platform_name": "Android"
            }
        ]
    }
}
