import numpy as np
import scipy.stats as st
from scipy.stats import rv_discrete
import matplotlib
from matplotlib import pyplot as plt

#全局卡池设定
_TOTAL_HOSHI4 = 88  #初始常驻4星数目（粗算，不包括本期）
TOTAL_HOSHI4_ADD = 14  #要抽的两期池子间新出的4星数目（按4团2混，4常驻2限定估计）
PT_LINE_HOSHI4 = 50  #常驻池必4PT线
PT_LINE_PICKUP = 100  #常驻池pickup的PT线
MAX_TICKET_USE = 10  #当期最多可使用交换券数目
MAX_TICKET_GET = 10  #当期最多可获得交换券数目
PRICE_PER_TICKET = 10  #每个交换券相当于多少贴纸
PRICE_PER_WELL = 300  #井卡消耗贴纸数

#全局抽卡设定
PT_SINGLE = 1  #单抽对应PT值上升
ONCE_GACHA_TIMES = 10  #一次抽多少发，默认十连
MAX_GACHA_TIMES = 300  #单期抽卡的最大抽卡次数
STOP_ON_WELL = True  #是否在井卡时停止当期抽卡
BLOCK_TICKET_INCREASE = False  #是否禁止交换券数目变化


#随机抽卡，模拟一发单抽，类型由pk指定
def gacha_single(pickup_cur, xk, pk):
    distribution = rv_discrete(values=(xk, pk))
    result = distribution.rvs(size=1)[0]
    #print(result)
    if (result < len(pickup_cur)):
        pickup_cur[result] = True
    return


#计数当前抽到了多少张当期UP卡
def cnt_pickup_cur(pickup_cur):
    ret = 0
    for b in pickup_cur:
        if b is True:
            ret += 1
    return ret


#模拟一次抽卡，返回新抽出的四星张数
def gacha_once(pickup_cur, model, pt_cur):
    cnt_pickup_before = cnt_pickup_cur(pickup_cur)
    if model['type'] == "normal":
        pt_after = pt_cur + ONCE_GACHA_TIMES * PT_SINGLE
        if pt_after >= PT_LINE_HOSHI4 and pt_cur < PT_LINE_HOSHI4:
            gacha_single(pickup_cur, model['xk'], model['pk_hoshi4'])
        elif pt_after >= PT_LINE_PICKUP and pt_cur < PT_LINE_PICKUP:
            gacha_single(pickup_cur, model['xk'], model['pk_pickup'])
        else:
            gacha_single(pickup_cur, model['xk'], model['pk_normal'])
    else:
        #限定池没有pt
        gacha_single(pickup_cur, model['xk'], model['pk_normal'])

    for i in range(ONCE_GACHA_TIMES - 1):
        gacha_single(pickup_cur, model['xk'], model['pk_normal'])
    cnt_pickup_after = cnt_pickup_cur(pickup_cur)
    return cnt_pickup_after - cnt_pickup_before


#模拟井卡
def well(pickup_cur):
    for i in range(len(pickup_cur)):
        if pickup_cur[i] is False:
            pickup_cur[i] = True
            break
    return


#模拟整期抽卡循环，返回一个字典记录该期统计信息
def gacha_cycle(model, ticket):
    ticket_cur = ticket[0]
    total_pickup = len(model['xk']) - 1
    ticket_before = ticket_cur

    #临时计数器
    gacha_times_cur = 0  #当前抽卡次数
    gacha_seals_cur = 0  #当前贴纸数
    pickup_cur = [False] * total_pickup  #当前抽到UP卡的情况
    pt_cur = 0  #当前奖励pt

    #单期统计信息
    ret = {}
    ret['get_pickup_times'] = [0]  #拿到相应张数UP卡对应的抽卡次数
    ret['is_welled'] = False  #当期是否吃井

    while gacha_times_cur < MAX_GACHA_TIMES and cnt_pickup_cur(
            pickup_cur) < total_pickup:
        cnt_pickup_once = gacha_once(pickup_cur, model, pt_cur)
        if model['type'] == 'normal':
            pt_cur += ONCE_GACHA_TIMES * PT_SINGLE
            if pt_cur >= PT_LINE_PICKUP:
                pt_cur -= PT_LINE_PICKUP
        gacha_times_cur += ONCE_GACHA_TIMES
        gacha_seals_cur += ONCE_GACHA_TIMES

        if gacha_seals_cur + min(
                MAX_TICKET_USE, ticket_cur
        ) * PRICE_PER_TICKET >= PRICE_PER_WELL and cnt_pickup_cur(
                pickup_cur) < total_pickup:
            ret['is_welled'] = True  #当期是否吃井
            well(pickup_cur)
            ticket_use = max(MAX_TICKET_USE, ticket_cur)
            gacha_seals_cur -= PRICE_PER_WELL - ticket_use * PRICE_PER_TICKET
            if BLOCK_TICKET_INCREASE is False:
                ticket_cur -= ticket_use
            cnt_pickup_once += 1
            #吃井就停手
            if STOP_ON_WELL is True:
                for i in range(cnt_pickup_once):
                    ret['get_pickup_times'].append(gacha_times_cur)
                break

        for i in range(cnt_pickup_once):
            ret['get_pickup_times'].append(gacha_times_cur)

    if BLOCK_TICKET_INCREASE is False:
        ticket_cur += min(MAX_TICKET_GET, gacha_seals_cur // PRICE_PER_TICKET)
        ret['change_ticket'] = ticket_cur - ticket_before

    ticket[0] = ticket_cur
    ret['cnt_pickup_get'] = cnt_pickup_cur(pickup_cur)
    ret['cnt_pickup_not_get'] = total_pickup - cnt_pickup_cur(pickup_cur)
    ret['gacha_times'] = gacha_times_cur
    return ret


#模拟一整期常驻抽卡，返回该期统计信息
def normal_gacha(ticket):
    #卡池设定
    gacha_type = "normal"  #卡池类型
    total_pickup = 3  #当期up卡数目
    pb_pickup = 0.004  #up率

    #自定义离散分布模拟抽卡使用的数组，最后一个元素代表非UP卡
    xk = [i for i in range(1 + total_pickup)]
    pk_normal = [pb_pickup] * total_pickup
    pk_normal.append(1 - total_pickup * pb_pickup)
    pk_hoshi4 = [1 / (_TOTAL_HOSHI4 + total_pickup)] * total_pickup
    pk_hoshi4.append(1 - 1 / (_TOTAL_HOSHI4 + total_pickup) * total_pickup)
    pk_pickup = [1 / total_pickup] * total_pickup
    pk_pickup.append(0)
    model = {
        'type': gacha_type,
        'xk': xk,
        'pk_normal': pk_normal,
        'pk_hoshi4': pk_hoshi4,
        'pk_pickup': pk_pickup
    }
    return gacha_cycle(model, ticket)


#模拟一整期限定/Fes抽卡
def limited_gacha(ticket):
    #卡池设定
    gacha_type = "limited"  #卡池类型
    total_pickup = 2  #当期up卡数目，普限为3，Fes为2
    pb_pickup = 0.004  #up率

    #自定义离散分布模拟抽卡使用的数组，最后一个元素代表非UP卡
    xk = [i for i in range(1 + total_pickup)]
    pk_normal = [pb_pickup] * total_pickup
    pk_normal.append(1 - total_pickup * pb_pickup)
    model = {'type': gacha_type, 'xk': xk, 'pk_normal': pk_normal}
    return gacha_cycle(model, ticket)


#长期抽卡模拟
def longtime_gacha():
    max_gachas = 5000  #抽卡期数上限
    ticket_normal = [0]  #初始持有的常驻交换券数目
    ticket_limited = [0]  #初始持有的限定交换券数目

    MAX_TOTAL_PICKUP = 5  #书写方便临时设置的最大up卡数

    #统计信息
    total_gachas = 0  #总抽卡期数
    total_wells = 0  #总吃井期数
    freq_wells = []  #吃井频率

    record_gacha_times = []  #各期抽卡次数
    sum_gacha_times = 0
    avg_gacha_times = []  #平均每期抽卡次数
    record_pickup_get = []  #各期抽出的up卡数
    sum_pickup_get = 0
    avg_pickup_get = []  #平均每期抽出的up卡数
    record_pickup_not_get = []  #各期少拿up卡的张数
    sum_pickup_not_get = 0
    avg_pickup_not_get = []  #平均每期少拿up卡的张数

    sum_pickup_not_get_each = [0] * MAX_TOTAL_PICKUP  #少拿指定张数up卡的期数之和
    freq_pickup_not_get_each = []  #少拿指定张数up卡的频率
    record_get_pickup_times = []  #各期拿到指定张数up卡的抽卡次数
    sum_get_pickup_times = [0] * MAX_TOTAL_PICKUP
    avg_get_pickup_times = []  #平均拿到指定张数up卡的抽卡次数（不考虑拿不到的情况）

    for i in range(MAX_TOTAL_PICKUP):
        freq_pickup_not_get_each.append([])
        record_get_pickup_times.append([])
        avg_get_pickup_times.append([])

    record_change_ticket = []  #各期交换券变动情况
    sum_change_ticket = 0
    avg_change_ticket = []  #平均每期交换券变动情况

    while total_gachas < max_gachas:
        total_gachas += 1
        record = normal_gacha(ticket_normal)  #常驻抽卡
        # record = limited_gacha(ticket_limited)  #限定抽卡
        global _TOTAL_HOSHI4
        _TOTAL_HOSHI4 += TOTAL_HOSHI4_ADD

        if record['is_welled'] is True:
            total_wells += 1
        freq_wells.append(total_wells / total_gachas)

        record_gacha_times.append(record['gacha_times'])
        sum_gacha_times += record['gacha_times']
        avg_gacha_times.append(sum_gacha_times / total_gachas)
        record_pickup_get.append(record['cnt_pickup_get'])
        sum_pickup_get += record['cnt_pickup_get']
        avg_pickup_get.append(sum_pickup_get / total_gachas)
        record_pickup_not_get.append(record['cnt_pickup_not_get'])
        sum_pickup_not_get += record['cnt_pickup_not_get']
        avg_pickup_not_get.append(sum_pickup_not_get / total_gachas)

        sum_pickup_not_get_each[record['cnt_pickup_not_get']] += 1
        for i in range(MAX_TOTAL_PICKUP):
            freq_pickup_not_get_each[i].append(sum_pickup_not_get_each[i] /
                                               total_gachas)

        for i in range(len(record['get_pickup_times'])):
            record_get_pickup_times[i].append(record['get_pickup_times'][i])
            sum_get_pickup_times[i] += record['get_pickup_times'][i]
            avg_get_pickup_times[i].append(sum_get_pickup_times[i] /
                                           total_gachas)

        if BLOCK_TICKET_INCREASE is False:
            record_change_ticket.append(record['change_ticket'])
            sum_change_ticket += record['change_ticket']
            avg_change_ticket.append(sum_change_ticket / total_gachas)

        if total_gachas % 10 == 0:
            print(
                f"抽卡期数：第{total_gachas}期，平均每期抽卡次数为{avg_gacha_times[total_gachas - 1]}，平均抽出{avg_pickup_get[total_gachas - 1]}张UP四星，吃井率{freq_wells[total_gachas - 1]}"
            )

    #绘图
    zhfont1 = matplotlib.font_manager.FontProperties(fname="SourceHanSansCN-Normal.otf") 

    x = np.arange(1, max_gachas + 1)

    y1 = np.asarray(avg_gacha_times)
    std_y1 = np.std(np.asarray(record_gacha_times))  #标准差
    print(f"抽卡次数标准差：{std_y1}")
    intercept_y1 = np.mean(y1[max_gachas // 5: max_gachas - 1])
    expectation_y1 = np.asarray([intercept_y1] * max_gachas)
    print(f"抽卡次数期望：{intercept_y1}")

    y2 = np.asarray(avg_pickup_get)
    std_y2 = np.std(np.asarray(record_pickup_get))
    print(f"抽出UP四星张数标准差：{std_y2}")
    intercept_y2 = np.mean(y2[max_gachas // 5: max_gachas - 1])
    expectation_y2 = np.asarray([intercept_y2] * max_gachas)
    print(f"抽出UP四星数期望：{intercept_y2}")


    y3 = np.asarray(freq_wells)
    intercept_y3 = np.mean(y3[max_gachas // 5: max_gachas - 1])
    expectation_y3 = np.asarray([intercept_y3] * max_gachas)
    print(f"吃井率期望：{intercept_y3}")

    y4 = np.asarray(freq_pickup_not_get_each[1])
    intercept_y4 = np.mean(y4[max_gachas // 5: max_gachas - 1])
    expectation_y4 = np.asarray([intercept_y4] * max_gachas)
    print(f"少出一张UP率期望：{intercept_y4}")


    fig1 = plt.figure()
    p1 = fig1.add_subplot(111)
    p1.plot(x, y1)
    p1.plot(x, expectation_y1)
    plt.ylim((0, MAX_GACHA_TIMES))
    plt.title("平均抽卡次数趋势", fontproperties=zhfont1)
    plt.xlabel("期数", fontproperties=zhfont1)
    plt.ylabel("平均抽卡次数", fontproperties=zhfont1)
    # plt.plot(x, y2)
    # plt.plot(x, y3)

    d = np.asarray(record_gacha_times)
    fig2 = plt.figure()
    p2 = fig2.add_subplot(111)
    p2.hist(d, bins = range(0, 20 + MAX_GACHA_TIMES, 10))
    plt.title("抽卡次数分布", fontproperties=zhfont1)
    plt.xlabel("抽卡次数", fontproperties=zhfont1)
    plt.ylabel("频数", fontproperties=zhfont1)

    fig3 = plt.figure()
    p3 = fig3.add_subplot(111)
    p3.plot(x, y2)
    p3.plot(x, expectation_y2)
    plt.ylim((0, MAX_TOTAL_PICKUP))
    plt.title("平均抽出UP卡数趋势", fontproperties=zhfont1)
    plt.xlabel("期数", fontproperties=zhfont1)
    plt.ylabel("平均UP卡数", fontproperties=zhfont1)
    
    fig4 = plt.figure()
    p4 = fig4.add_subplot(111)
    p4.plot(x, y3)
    p4.plot(x, expectation_y3)
    plt.ylim((0, 1))
    plt.title("平均吃井率趋势", fontproperties=zhfont1)
    plt.xlabel("期数", fontproperties=zhfont1)
    plt.ylabel("平均吃井率", fontproperties=zhfont1)

    fig5 = plt.figure()
    p5 = fig5.add_subplot(111)
    p5.plot(x, y4)
    p5.plot(x, expectation_y4)
    plt.ylim((0, 1))
    plt.title("平均少出一张UP率趋势", fontproperties=zhfont1)
    plt.xlabel("期数", fontproperties=zhfont1)
    plt.ylabel("平均少出一张UP率", fontproperties=zhfont1)

    plt.show()
    return

longtime_gacha()
