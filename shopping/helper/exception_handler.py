import logging
import traceback
from functools import wraps
from time import strftime, localtime
from fastapi import requests
from config import settings


class ExceptionHandler:
    def __init__(self, message: str):
        self.now = str(strftime("%Y-%m-%d %H:%M:%S", localtime())).replace(" ", "-")
        self.message = message

    def logger(self):
        logging.error(self.message)

    def send_sms(self):
        if settings.DEBUG_MODE:
            return
        message = self.message.replace(" ", "_")
        for number in settings.RECIPIENTS:

            url = f"receptor={number}&"
            url += f"token={settings.APP_NAME}&"
            url += f"token2={self.now}&"
            url += f"token3={message}&"
            url += f"template={settings.TEMPLATE}"
            result = requests.post(url)
            print(result.status_code)
            if result.status_code == 200:
                pass
            elif result.status_code == 418:
                print("اعتبار حساب شما کافی نیست")
            elif result.status_code == 422:
                print("داده ها به دلیل وجود کاراکتر نامناسب قابل پردازش نیست")
            elif result.status_code == 424:
                print("الگوی مورد نظر پیدا نشد ، زمانی که نام الگو نادرست باشد "
                      "یا طرح آن هنوز تائید نشده باشد رخ می‌دهد")
            elif result.status_code == 426:
                print("استفاده از این متد نیازمند سرویس پیشرفته می‌باشد")
            elif result.status_code == 428:
                print("ارسال کد از طریق تماس تلفنی امکان پذیر نیست، "
                      "درصورتی که توکن فقط حاوی عدد نباشد این خطا رخ می‌دهد")
            elif result.status_code == 431:
                print("ساختار کد صحیح نمی‌باشد ، "
                      "اگر توکن حاوی خط جدید،فاصله، UnderLine یا جداکننده باشد این خطا رخ می‌دهد")
            elif result.status_code == 432:
                print("پارامتر کد در متن پیام پیدا نشد ، "
                      "اگر در هنگام تعریف الگو پارامتر token% را تعریف نکرده باشید این خطا رخ می‌دهد")
            else:
                print("خطای نامشخص")

    @staticmethod
    def exception_handler(func):
        try:
            return func
        except Exception:
            now = strftime("%Y-%m-%d %H:%M", localtime())
            message = f'{settings.APP_NAME} | {now}: {func.__name__} failed with exception:\n{traceback.format_exc()}'
            print(message)
            logging.error(message)
            if not settings.DEBUG_MODE:
                ExceptionHandler(message).send_sms()

    @staticmethod
    def fastapi_exception_handler(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception:
                now = strftime("%Y-%m-%d %H:%M", localtime())
                message = \
                    f'{settings.APP_NAME} | {now}: {func.__name__} failed with exception:\n{traceback.format_exc()}'
                print(message)
                logging.error(message)
                if not settings.DEBUG_MODE:
                    ExceptionHandler(message).send_sms()

        return wrapper
