from shopping.customer.register.models import Customer
from shopping.customer.register.modules import log
from shopping.customer.register.modules.auth import AuthHandler


auth_handler = AuthHandler()


# mobile number generator and validation
def check_is_registered(customer_phone_number: str):
    """
    returns a flag, indicates that user is registered
    :param customer_phone_number: a valid mobile number
    :return: a dict with success flag
    """
    customer = Customer(phone_number=customer_phone_number)
    status = customer.get_status()
    if customer.is_exists_phone_number():
        redirect = "login" if customer.is_mobile_confirm() else "loginOtp"
        message = {
            "customerIsMobileConfirm": customer.is_mobile_confirm(),
            "hasRegistered": True,
            "message": "شما قبلا ثبت نام کرده اید.",
            "redirect": redirect,
            "customerStatus": status,
            "customerIsActive": customer.is_customer_active()
        }
    else:
        message = {
            "hasRegistered": False,
            "message": "شما قبلا ثبت نام نکرده اید",
            "redirect": "register",

        }
    return {"success": True, "status_code": 200, "message": message}



def checking_login_password(customer_phone_number: str, customer_password: str):
    customer = Customer(phone_number=customer_phone_number)
    if user := customer.get_customer_password():
        if auth_handler.verify_password(customer_password, user.get("customerPassword")):
            if user.get("customerIsMobileConfirm"):
                log.save_login_log(customer_phone_number)
                user_info = customer.get_customer()
                message = {
                    "message": f"{user_info.get('customerFirstName')} {user_info.get('customerLastName')} عزیز به آسود خوش آمدید",
                    "data": user_info
                }
                return dict({"success": True, "status_code": 202}, **message)
            else:
                message = {
                    "customerIsMobileConfirm": user.get("customerIsMobileConfirm"),
                    "customerIsConfirm": user.get("customerIsConfirm"),
                    "hasRegistered": True,
                    "message": "برای ورود نیاز به تایید شماره موبایل دارید. لطفا از طریق کد یک بار مصرف وارد شوید",
                }
                return {"success": False, "status_code": 406, "error": message}
        else:
            password = TempPassword(customer_phone_number)
            if password.get_password() and password.get_password(customer_phone_number) == customer_password:
                password.delete_password()
                if user.get("customerIsMobileConfirm"):
                    log.save_login_log(customer_phone_number)
                    user_info = customer.get_customer()
                    message = {
                        "message": f"{user_info.get('customerFirstName')} {user_info.get('customerLastName')} عزیز به آسود خوش آمدید",
                        "data": user_info
                    }
                    return dict({"success": True, "status_code": 202}, **message)
                else:
                    message = {
                        "customerIsMobileConfirm": user.get("customerIsMobileConfirm"),
                        "customerIsConfirm": user.get("customerIsConfirm"),
                        "hasRegistered": True,
                        "message": "برای ورود نیاز به تایید شماره موبایل دارید. لطفا از طریق کد یک بار مصرف وارد شوید",
                    }
                    return {"success": False, "status_code": 406, "error": message}
            return {"success": False, "status_code": 401, "error": "رمز وارد شده نادرست است"}
    else:
        message = {
            "hasRegistered": False,
            "error": "شما قبلا ثبت نام نکرده اید",
            "redirect": "register"
        }
        return {"success": False, "status_code": 401, "error": message}


def save_logout(username: dict):
    customer_id = username.get("user_id")
    if result := log.save_logout_log(customer_id):
        # redirect to home page
        return {"success": True, "status_code": 202, "message": {"message": "خروج با موفقیت انجام شد"}}
    else:
        return {"success": False, "status_code": 417, "error": "خطایی رخ داده است. لطفا مجددا تلاش کنید"}


def forget_password(customer_phone_number: str, password: str):
    customer = Customer(phone_number=customer_phone_number)
    if customer.is_exists_phone_number():
        if customer.change_customer_password(password):
            return {"success": True, "status_code": 200,
                    "message": {"message": "رمز عبور با موفقیت تغییر کرد"}}
        return {"success": False, "status_code": 417, "error": "خطایی رخ داده است"}
    return {"success": False, "status_code": 404, "error": "اطلاعات کاربر وجود ندارد"}
