import logger
import json
import requests
import time
from login import get_cookies
import random
import hashlib

# PC端签到接口
# sign_url = "https://tieba.baidu.com/sign/add"

# 移动端签到接口
sign_url = "https://c.tieba.baidu.com/c/c/forum/sign"


# 单个贴吧签到
# tieba_name:贴吧名
def tieba_sign_in(tieba_name, tbs, BDUSS):
    sign_str = f"kw={tieba_name}tbs={tbs}tiebaclient!!!"
    sign = hashlib.md5(sign_str.encode("utf-8")).hexdigest()
    payload = {
        "kw": tieba_name,
        "tbs": tbs,
        "sign": sign,
    }
    Cookies = {
        "BDUSS": BDUSS,
    }
    resp = requests.post(
        sign_url,
        cookies=Cookies,
        data=payload,
    )
    
    try:
        json_resp = resp.json()
        if "user_info" in json_resp:
            logger.debug("签到成功：" + tieba_name + "吧")
            return True
        elif json_resp["error_code"] == "160002":
            # 已签到
            logger.error(
                "签到失败：" + tieba_name + "吧" + " 失败原因：" + json_resp["error_msg"]
            )
        else:
            logger.error("签到失败：" + tieba_name + "吧")
            logger.debug(str(json_resp))
            logger.error("失败原因：" + json_resp["error_msg"])
    except Exception as e:
        logger.error("签到失败：" + tieba_name + "吧")
        logger.error("报错：" + str(e))
        logger.debug("返回数据：" + resp.text)
        return False
    
    return False


def sign_in():
    logger.info("开始签到\n")
    with open("tieba_dict.json", "r", encoding="utf-8") as f:
        tieba_dict = json.load(f)
    sign_sum, faliure_sum = 0, 0
    tbs, BDUSS, _ = get_cookies()
    for tieba_name, tieba_url in tieba_dict.items():
        if tieba_sign_in(tieba_name, tbs, BDUSS) == False:
            faliure_sum += 1
        sign_sum += 1
        logger.info("共计" + str(sign_sum) + "个吧")
        logger.info("已签到成功" + str(sign_sum - faliure_sum) + "个吧\n")
        time.sleep(random.randint(1, 5))

    logger.info("共计" + str(sign_sum) + "个贴吧")
    logger.info("成功" + str(sign_sum - faliure_sum) + "个")
    logger.info("失败" + str(faliure_sum) + "个")


if __name__ == "__main__":
    tieba_name = "余额宝"
    tieba_url = "https://tieba.baidu.com/f?kw=%D3%E0%B6%EE%B1%A6"
    logger.set_logger("debug")
    tieba_sign_in(tieba_name, tieba_url)
