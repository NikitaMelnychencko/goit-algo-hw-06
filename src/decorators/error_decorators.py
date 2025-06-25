from helper.color_loger import  log_warning, log_error
from functools import wraps

def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            log_error(f"{e}")
        except Warning as e:
            error_data = e.args[0]
            massage = error_data.get('massage')
            callback = error_data.get('callback')
            log_warning(massage)
            if callback:
                callback()


    return inner