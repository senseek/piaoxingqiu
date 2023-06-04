import requests

from config import token


# 根据项目id获取所有场次和在售状态
def get_sessions(show_id) -> list | None:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json'
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/show/pub/v3/show/" + show_id + "/sessions_dynamic_data"
    response = requests.get(url=url, headers=headers).json()
    if response["statusCode"] == 200:
        return response["data"]["sessionVOs"]
    else:
        print("get_sessions异常:" + str(response))
    return None


# 根据场次id获取座位信息
def get_seat_plans(show_id, session_id) -> list:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json'
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/show/pub/v3/show/" + show_id + "/show_session/" + session_id + "/seat_plans_static_data"
    response = requests.get(url=url, headers=headers).json()
    if response["statusCode"] == 200:
        return response["data"]["seatPlans"]
    else:
        raise Exception("get_seat_plans异常:" + str(response))


# 获取座位余票
def get_seat_count(show_id, session_id) -> list:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json'
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/show/pub/v3/show/" + show_id + "/show_session/" + session_id + "/seat_plans_dynamic_data"
    response = requests.get(url=url, headers=headers).json()
    if response["statusCode"] == 200:
        return response["data"]["seatPlans"]
    else:
        raise Exception("get_seat_count异常:" + str(response))


# 获取门票类型（快递送票EXPRESS,电子票E_TICKET,现场取票VENUE,电子票或现场取票VENUE_E）
def get_deliver_method(show_id, session_id, seat_plan_id, price: int, qty: int) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        'access-token': token
    }
    data = {
        "items": [
            {
                "skus": [
                    {
                        "seatPlanId": seat_plan_id,  # 644fcf080f4f4e0001f1519d
                        "sessionId": session_id,  # 644fcb7dca916100017dda3d
                        "showId": show_id,  # 644fcb2aca916100017dcfef
                        "skuId": seat_plan_id,
                        "skuType": "SINGLE",
                        "ticketPrice": price,  # 388
                        "qty": qty  # 2
                    }
                ],
                "spu": {
                    "id": show_id,
                    "spuType": "SINGLE"
                }
            }
        ]
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/trade/buyer/order/v3/pre_order"
    response = requests.post(url=url, headers=headers, json=data).json()
    if response["statusCode"] == 200:
        return response["data"]["supportDeliveries"][0]["name"]
    else:
        raise Exception("获取门票类型异常:" + str(response))


# 获取观演人信息
def get_audiences() -> list | None:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        'access-token': token
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/user/buyer/v3/user_audiences"
    response = requests.get(url=url, headers=headers).json()
    if response["statusCode"] == 200:
        return response["data"]
    else:
        print("get_audiences异常:" + str(response))
    return None


# 获取收货地址
def get_address() -> dict | None:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        'access-token': token
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/user/buyer/v3/user/addresses/default"
    response = requests.get(url=url, headers=headers).json()
    if response["statusCode"] == 200:
        return response["data"]
    else:
        print("get_address异常:" + str(response))
    return None


# 获取快递费
def get_express_fee(show_id, session_id, seat_plan_id, price: int, qty: int, location_city_id: str) -> dict:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        'access-token': token
    }
    data = {
        "items": [
            {
                "skus": [
                    {
                        "seatPlanId": seat_plan_id,  # 644fcf080f4f4e0001f1519d
                        "sessionId": session_id,  # 644fcb7dca916100017dda3d
                        "showId": show_id,  # 644fcb2aca916100017dcfef
                        "skuId": seat_plan_id,
                        "skuType": "SINGLE",
                        "ticketPrice": price,  # 388
                        "qty": qty,  # 2
                        "deliverMethod": "EXPRESS"
                    }
                ],
                "spu": {
                    "id": show_id,
                    "spuType": "SINGLE"
                }
            }
        ],
        "locationCityId": location_city_id  # 460102
    }
    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/trade/buyer/order/v3/price_items"
    response = requests.post(url=url, headers=headers, json=data).json()
    if response["statusCode"] == 200:
        return response["data"][0]
    else:
        raise Exception("获取快递费异常:" + str(response))


# 提交订单（快递送票EXPRESS,电子票E_TICKET,现场取票VENUE,电子票或现场取票VENUE_E）
def create_order(show_id, session_id, seat_plan_id, price: int, qty: int, deliver_method, express_fee: int, receiver,
                 cellphone,
                 address_id, detail_address, location_city_id, audience_ids: list):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36',
        'Content-Type': 'application/json',
        'access-token': token
    }
    if deliver_method == "EXPRESS":
        data = {
            "priceItemParam": [
                {
                    "applyTickets": [],
                    "priceItemName": "票款总额",
                    "priceItemVal": price * qty,
                    "priceItemType": "TICKET_FEE",
                    "priceItemSpecies": "SEAT_PLAN",
                    "direction": "INCREASE",
                    "priceDisplay": "￥" + str(price * qty)
                },
                {
                    "applyTickets": [],
                    "priceItemName": "快递费",
                    "priceItemVal": express_fee,
                    "priceItemId": show_id,
                    "priceItemSpecies": "SEAT_PLAN",
                    "priceItemType": "EXPRESS_FEE",
                    "direction": "INCREASE",
                    "priceDisplay": "￥" + str(express_fee)
                }
            ],
            "items": [
                {
                    "skus": [
                        {
                            "seatPlanId": seat_plan_id,
                            "sessionId": session_id,
                            "showId": show_id,
                            "skuId": seat_plan_id,
                            "skuType": "SINGLE",
                            "ticketPrice": price,
                            "qty": qty,
                            "deliverMethod": deliver_method
                        }
                    ],
                    "spu": {
                        "id": show_id,
                        "spuType": "SINGLE"
                    }
                }
            ],
            "contactParam": {
                "receiver": receiver,  # 张三
                "cellphone": cellphone  # 13812345678
            },

            "one2oneAudiences": [{"audienceId": i, "sessionId": session_id} for i in audience_ids],
            "addressParam": {
                "address": detail_address,  # 星巴克咖啡门口
                "district": location_city_id[4:],
                "city": location_city_id[2:4],
                "province": location_city_id[0:2],
                "addressId": address_id
            }
        }
    elif deliver_method == "E_TICKET":
        data = {
            "priceItemParam": [
                {
                    "applyTickets": [],
                    "priceItemName": "票款总额",
                    "priceItemVal": price * qty,
                    "priceItemType": "TICKET_FEE",
                    "priceItemSpecies": "SEAT_PLAN",
                    "direction": "INCREASE",
                    "priceDisplay": "￥" + str(price * qty)
                }
            ],
            "items": [
                {
                    "skus": [
                        {
                            "seatPlanId": seat_plan_id,
                            "sessionId": session_id,
                            "showId": show_id,
                            "skuId": seat_plan_id,
                            "skuType": "SINGLE",
                            "ticketPrice": price,
                            "qty": qty,
                            "deliverMethod": deliver_method
                        }
                    ],
                    "spu": {
                        "id": show_id,
                        "spuType": "SINGLE"
                    }
                }
            ],
            "many2OneAudience": {
                "audienceId": audience_ids[0],
                "sessionIds": [
                    session_id
                ]
            }
        }
    elif deliver_method == "VENUE":
        data = {
            "priceItemParam": [
                {
                    "applyTickets": [],
                    "priceItemName": "票款总额",
                    "priceItemVal": price * qty,
                    "priceItemType": "TICKET_FEE",
                    "priceItemSpecies": "SEAT_PLAN",
                    "direction": "INCREASE",
                    "priceDisplay": "￥" + str(price * qty)
                }
            ],
            "items": [
                {
                    "skus": [
                        {
                            "seatPlanId": seat_plan_id,
                            "sessionId": session_id,
                            "showId": show_id,
                            "skuId": seat_plan_id,
                            "skuType": "SINGLE",
                            "ticketPrice": price,
                            "qty": qty,
                            "deliverMethod": deliver_method
                        }
                    ],
                    "spu": {
                        "id": show_id,
                        "spuType": "SINGLE"
                    }
                }
            ],
            "one2oneAudiences": [{"audienceId": i, "sessionId": session_id} for i in audience_ids]
        }
    elif deliver_method == "VENUE_E":
        data = {
            "priceItemParam": [
                {
                    "applyTickets": [],
                    "priceItemName": "票款总额",
                    "priceItemVal": price * qty,
                    "priceItemType": "TICKET_FEE",
                    "priceItemSpecies": "SEAT_PLAN",
                    "direction": "INCREASE",
                    "priceDisplay": "￥" + str(price * qty)
                }
            ],
            "items": [
                {
                    "skus": [
                        {
                            "seatPlanId": seat_plan_id,
                            "sessionId": session_id,
                            "showId": show_id,
                            "skuId": seat_plan_id,
                            "skuType": "SINGLE",
                            "ticketPrice": price,
                            "qty": qty,
                            "deliverMethod": deliver_method
                        }
                    ],
                    "spu": {
                        "id": show_id,
                        "spuType": "SINGLE"
                    }
                }
            ]
        }
    else:
        raise Exception("不支持的deliver_method:" + str(deliver_method))

    url = "https://m.piaoxingqiu.com/cyy_gatewayapi/trade/buyer/order/v3/create_order"
    response = requests.post(url=url, headers=headers, json=data).json()
    if response["statusCode"] == 200:
        print("下单成功！请尽快支付！")
    else:
        raise Exception("下单异常:" + str(response))
