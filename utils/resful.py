#encoding:utf-8
from django.http import  JsonResponse
class Httpcode(object):
    ok = 200
    paramserror = 400
    unauth = 401
    methodeerror = 405
    servererror = 500


#{"code":400,"message":"","date":""}

def result(code=Httpcode.ok,message="",data=None ,kwargs=None):
    json_dict = {"cade":code,"message":message,"data":data }
    if kwargs and isinstance(kwargs,dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)

def OK():
    return result()
def params_error(message="",data=None):
    return result(code=Httpcode.paramserror,message=message,data =data)
def unauth(message="",data=None):
    return result(code=Httpcode.unauth,message=message,data=data)
def method(message="",data =None):
    return result(code=Httpcode.methodeerror,message=message,data=data)
def servererror(message="",data =None):
    return result(code=Httpcode.servererror,message=message,data=data)