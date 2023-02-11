from ctypes import windll


class WinAPIError(Exception):
    def __init__(self, error_code=None, func_name=None):
        if error_code is None:
            self.error_code = windll.kernel32.GetLastError()
        else:
            self.error_code = error_code
        if func_name:
            message = f'Windows api error at calling {func_name}, error_code: {self.error_code:#X}'
        else:
            message = f'Windows api error, error_code: {self.error_code:#X}'
        super(WinAPIError, self).__init__(message)
