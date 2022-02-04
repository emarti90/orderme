menu_schema = {
    "type":"object",
    "properties":
    {
        "restaurant_id":{"type":"string"},
        "menu_items":
        {
            "type":"array","items": 
            {
                "type": "object",
                "properties": 
                {
                    "item_id":{"type": "string"},
                    "description":{"type":"string"},
                    "allergens":{"type":"array","items":{"type":"string",
                                                        "enum":["gluten" ,"crustacean","egg","fish","peanut",
                                                        "soybean","milk","nut","celery","mustard",
                                                        "sesame" ,"sulph","lupin","molluc","none"]}
                    },
                    "category":{"type": "string"},
                    "prize":{"type": "number"},
                    "picture":{"type":"string"}
                },

                "required":["item_id","allergens","category","prize"]
            }
        }
    },
    "required":["restaurant_id", "menu_items"]
}

order_schema = {
    "type":"object",
    "properties":
    {
        "restaurant_id":{"type":"string"},
        "table_id":{"type":"string"},
        "orders":
        {
            "type":"array","items":
            {
                "type":"object",
                "properties":
                {
                    "item_id":{"type":"string"},
                    "quantity":{"type":"number"},
                    "timestamp":{"type":"string","format":"date-time"}
                }
            }      
        },
        "tab":
        {
            "type":"array","items":
            {
                "type":"object",
                "properties":
                {
                    "item_id":{"type":"string"},
                    "quantity":{"type":"number"},
                    "item_prize":{"type":"number"}                    
                }
            } 
        },
        "total_amount":{"type":"number"}
    },
    "required":["restaurant_id","table_id","orders","total_amount"]
}

checkout_schema = {
    "type":"object",
    "properties":
    {
        "restaurant_id":{"type":"string"},
        "table_id":{"type":"string"},
        "tab":
        {
            "type":"array","items":
            {
                "type":"object",
                "properties":
                {
                    "item_id":{"type":"string"},
                    "quantity":{"type":"number"},
                    "item_prize":{"type":"number"}
                }
            } 
        },
        "total_amount":{"type":"number"}
    },
    "required":["restaurant_id","table_id","tab","total_amount"]
}

user_schema = {
    "type":"object",
    "properties":
    {
        "user":{"type":"string"},
        "password":{"type":"string"},
        "access":{"type":"string"},
        "role":{"type":"string", "enum":{"OWNER", "TABLE"}},
        "email":{"type":"string","format":"email"}
    },
    "required":["user","password"]
}

access_schema = {
    "type":"object",
    "properties":
    {
        "user":{"type":"string"},
        "token":{"type":"string"},
        "expires":{"type":"string"}
    },
    "required":["user"]
}

