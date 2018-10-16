# -*- coding: utf8 -*-

def error_message(name):
    return ValueError("The parameter '{}' is not valid.".format(name))

class RestfulType:
    @staticmethod
    def user_type(value, name):
        if value in ['NOMAL', 'MANAGER', 'ADMIN']:
            return value

        raise ValueError("The parameter '{}' is not valid.".format(name))


    @staticmethod
    def alphanumeric(value, name):
        if str.isalnum(value):
            return value
        
        raise ValueError("The parameter '{}' is not valid.".format(name))