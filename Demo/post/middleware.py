import time

from django.utils.deprecation import MiddlewareMixin


def check_request_rate(request):
    '''检查访问频率'''
    request_time = request.session.get('request_time', [0, 0])
    now = time.time()
    if (now - request_time[0]) < 1:
        time.sleep(10)  # 访问太频繁，阻塞
        # 更新时间列表
        request_time = [request_time[1], time.time()]
    else:
        # 更新时间列表
        request_time = [request_time[1], now]

    request.session['request_time'] = request_time  # 将时间列表存回 session


class BlockMiddleware(MiddlewareMixin):
    '''
        2018-03-23 15:29:1.02
        2018-03-23 15:29:1.21
        2018-03-23 15:29:2.42
        2018-03-23 15:29:2.52 <- 当前时刻
        记录在哪？                session
        以什么形式记录？数据结构？   [1.82, 2.42, 2.52]
        保留多少记录？             count
    '''
    def process_request(self, request):
        check_request_rate(request)


def block_middleware(get_response):
    '''装饰器形式'''
    def wrap(request, *args, **kwrags):
        check_request_rate(request)
        response = get_response(request, *args, **kwrags)  # 调用 View 函数
        return response
    return wrap
