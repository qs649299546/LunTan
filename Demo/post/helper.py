from redis import Redis
from django.core.cache import cache
from django.conf import settings

from post.models import Post

rds = Redis(**settings.REDIS)


def page_cache(timeout):
    def wrap1(view_func):
        def wrap2(request, *args, **kwargs):
            key = 'Response-%s' % request.get_full_path()
            response = cache.get(key)
            print('get from cache:', response)

            # 添加阅读计数
            if response and view_func.__name__ == 'read_post':
                rds.zincrby('ReadRank', int(request.GET.get('post_id')))

            if response is None:
                response = view_func(request, *args, **kwargs)
                cache.set(key, response, timeout)
                print('get from view:', response)

            return response
        return wrap2
    return wrap1


def get_top_n(n):
    '''获取 Top N'''
    # zrevrange 数据格式
    #   [
    #    (b'9',  64.0),
    #    (b'5',  37.0),
    #    (b'12', 34.0),
    #    ...
    #   ]
    rank_data = rds.zrevrange('ReadRank', 0, n - 1, withscores=True)

    # 第一次类型转换
    #   [
    #    [9,  64],
    #    [5,  37],
    #    [12, 34],
    #    ...
    #   ]
    rank_data = [[int(post_id), int(num)] for post_id, num in rank_data]

    post_id_list = [d[0] for d in rank_data]                                      # 取出每一项的 post_id
    posts = {post.id: post for post in Post.objects.filter(id__in=post_id_list)}  # 取出每一项对应的 post 实例

    # 第二次类型转换
    # [
    #     [<Post: Post object>, 64],
    #     [<Post: Post object>, 37],
    #     [<Post: Post object>, 34],
    #     ...
    # ]
    rank_data = [[posts[post_id], num] for post_id, num in rank_data]
    return rank_data
