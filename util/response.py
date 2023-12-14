class Response:

    def __init__(self, status: bool, msg: str):
        self.msg = msg
        self.status = status

    # Getter method
    @property
    def get_msg(self):
        return self.msg

    @property
    def get_status(self):
        return self.status

    @property
    def get_response(self):
        res_dic = {'status': self.status, 'msg': self.msg}
        return res_dic

    # Setter method
    def set_msg(self, value):
        self.msg = value

    def set_status(self, value):
        self.status = value

    def __str__(self):
        return f'{self.get_response}'
