import request
import config

'''
目前仅支持【无需选座】的项目
'''
show_id = config.show_id
session_id = config.session_id
buy_count = config.buy_count
audience_idx = config.audience_idx
deliver_method = config.deliver_method
seat_plan_id = ''
session_id_exclude = []  # 被排除掉的场次
price = 0

while True:
    try:
        # 如果没有指定场次，则默认从第一场开始刷
        if not session_id:
            # 如果项目不是在售状态就一直刷，直到变成在售状态拿到场次id，如果有多场，默认拿第一场
            while True:
                sessions = request.get_sessions(show_id)
                if sessions:
                    for i in sessions:
                        if i["sessionStatus"] == 'ON_SALE' and i["bizShowSessionId"] not in session_id_exclude:
                            session_id = i["bizShowSessionId"]
                            print("session_id:" + session_id)
                            break
                    if session_id:
                        break
                    else:
                        print("未获取到在售状态且符合购票数量需求的session_id")
                        session_id_exclude = []  # 再给自己一次机会，万一被排除掉的场次又放票了呢
        # 获取座位余票信息，默认从最低价开始
        seat_plans = request.get_seat_plans(show_id, session_id)
        seat_count = request.get_seat_count(show_id, session_id)
        print(seat_count)

        for i in seat_count:
            if i["canBuyCount"] >= buy_count:
                seat_plan_id = i["seatPlanId"]
                for j in seat_plans:
                    if j["seatPlanId"] == seat_plan_id:
                        price = j["originalPrice"]  # 门票单价
                        break
                break
        # 如果没有拿到seat_plan_id，说明该场次所有座位的余票都不满足购票数量需求，就重新开始刷下一场次
        if not seat_plan_id:
            print("该场次" + session_id + "没有符合条件的座位，将为你继续搜寻其他在售场次")
            session_id_exclude.append(session_id)  # 排除掉这个场次
            session_id = ''
            continue

        if not deliver_method:
            deliver_method = request.get_deliver_method(show_id, session_id, seat_plan_id, price, buy_count)
        print("deliver_method:" + deliver_method)

        if deliver_method == "VENUE_E":
            request.create_order(show_id, session_id, seat_plan_id, price, buy_count, deliver_method, 0, None,
                                 None, None, None, None, [])
        else:
            # 获取观演人信息
            audiences = request.get_audiences()
            if len(audience_idx) == 0:
                audience_idx = range(buy_count)
            audience_ids = [audiences[i]["id"] for i in audience_idx]

            if deliver_method == "EXPRESS":
                # 获取默认收货地址
                address = request.get_address()
                address_id = address["addressId"]  # 地址id
                location_city_id = address["locationId"]  # 460102
                receiver = address["username"]  # 收件人
                cellphone = address["cellphone"]  # 电话
                detail_address = address["detailAddress"]  # 详细地址

                # 获取快递费用
                express_fee = request.get_express_fee(show_id, session_id, seat_plan_id, price, buy_count,
                                                      location_city_id)

                # 下单
                request.create_order(show_id, session_id, seat_plan_id, price, buy_count, deliver_method,
                                     express_fee["priceItemVal"], receiver,
                                     cellphone, address_id, detail_address, location_city_id, audience_ids)
            elif deliver_method == "VENUE" or deliver_method == "E_TICKET":
                request.create_order(show_id, session_id, seat_plan_id, price, buy_count, deliver_method, 0, None,
                                     None, None, None, None, audience_ids)
            else:
                print("不支持的deliver_method:" + deliver_method)
        break
    except Exception as e:
        print(e)
        session_id_exclude.append(session_id)  # 排除掉这个场次
        session_id = ''

