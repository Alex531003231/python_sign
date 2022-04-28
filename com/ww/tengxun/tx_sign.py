import logging
import requests

# 腾讯Cookie,
tx_cookie = ''
auth_refresh_url = ''

# 腾讯视频签到
def tx_sign():
    url1 = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=hierarchical_task_system&cmd=2'
    url2 = 'https://v.qq.com/x/bu/mobile_checkin'
    url3 = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=1'  # 观看60分钟
    url4 = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=7'  # 下载
    url5 = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=6'  # 赠送
    url6 = 'https://vip.video.qq.com/fcgi-bin/comm_cgi?name=spp_MissionFaHuo&cmd=4&task_id=3'  # 弹幕
    login_headers = {
        'Referer': 'https://v.qq.com',
        'Cookie': tx_cookie
    }
    login = requests.get(auth_refresh_url, headers=login_headers)
    resp_cookie = requests.utils.dict_from_cookiejar(login.cookies)
    if not resp_cookie:
        logging.info('腾讯视频V力值签到通知' + '获取Cookie失败，Cookie失效')
    arr = tx_cookie.split('; ')
    sign_cookie = ''
    for str in arr:
        if 'vqq_vusession' in str:
            continue
        else:
            sign_cookie += (str + '; ')
    sign_cookie += ('vqq_vusession=' + resp_cookie['vqq_vusession'] + ';')
    sign_headers = {
        'Cookie': sign_cookie,
        'Referer': 'https://m.v.qq.com'
    }
    send_message = ''
    sign1 = response_handle(url1, sign_headers)
    send_message += '链接1' + sign1 + '\n'
    # sign2 = response_handle(url2, sign_headers)
    send_message += '链接2' + '任务未完成' + '\n'
    sign3 = response_handle(url3, sign_headers)
    send_message += '链接3' + sign3 + '\n'
    sign4 = response_handle(url4, sign_headers)
    send_message += '链接4' + sign4 + '\n'
    sign5 = response_handle(url5, sign_headers)
    send_message += '链接5' + sign5 + '\n'
    sign6 = response_handle(url6, sign_headers)
    send_message += '链接6' + sign6 + '\n'
    mes = '腾讯视频V力值签到通知\n\n' + send_message
    return mes


# 处理腾讯视频返回结果
def response_handle(url, sign_headers):
    resp_str = requests.get(url, headers=sign_headers).text
    if '-777903' in resp_str:
        return "已获取过V力值"
    elif '-777902' in resp_str:
        return "任务未完成"
    elif 'OK' in resp_str:
        return "成功，获得V力值：" + resp_str[42:-14]
    else:
        return "执行出错"


if __name__ == '__main__':
    message = tx_sign()
    logging.info("腾讯视频V力值签到通知",message)
    print(message)
