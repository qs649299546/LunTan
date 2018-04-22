from django.db import models

from user.models import User


class Post(models.Model):
    uid = models.IntegerField()
    title = models.CharField(max_length=64)
    content = models.TextField()
    create = models.DateTimeField(auto_now_add=True)

    @property
    def auth(self):
        if not hasattr(self, '_auth'):
            self._auth = User.objects.get(id=self.uid)
        return self._auth

    def comments(self):
        return Comment.objects.filter(pid=self.id)

    def tags(self):
        post_tag_relations = PostTags.objects.filter(pid=self.id).only('tid')  # 查找关系表中与当前post相关的记录
        tag_id_list = [pt.tid for pt in post_tag_relations]                    # 取出相关联的 tag 的 id
        return Tag.objects.filter(id__in=tag_id_list)                          # 根据查到的 tag id 取出当前 post 的 tag

    def delete(self):
        from post.helper import rds
        rds.zrem('ReadRank', self.id)
        self.comments().delete()                       # 删除文章评论
        PostTags.objects.filter(pid=self.id).delete()  # 删除 Tag 关系
        super().delete()                               # 删除自身


class Comment(models.Model):
    pid = models.IntegerField()
    name = models.CharField(max_length=64)
    content = models.TextField()
    create = models.DateTimeField(auto_now_add=True)

    @property
    def post(self):
        if not hasattr(self, '_post'):
            self._post = Post.objects.get(id=self.pid)
        return self._post


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    @classmethod
    def ensure_tags(cls, tag_names):
        '''确保 Tags 存在'''
        tags = Tag.objects.filter(name__in=tag_names)
        new_names = set(tag_names) - set(t.name for t in tags)
        Tag.objects.bulk_create([Tag(name=n) for n in new_names])
        return Tag.objects.filter(name__in=tag_names)

    def posts(self):
        pid_list = [pt.pid for pt in PostTags.objects.filter(tid=self.id).only('pid')]
        return Post.objects.filter(id__in=pid_list)


class PostTags(models.Model):
    '''
    Post 和 Tag 的关系表

        Post    Tag
           1      1
           1      2
           1      3
           3      1
           3      4
    '''
    pid = models.IntegerField()
    tid = models.IntegerField()

    @classmethod
    def update_post_tags(cls, post_id, tag_names):
        tags = Tag.ensure_tags(tag_names)
        tid_list = [t.id for t in tags]

        # 取出旧的关系
        post_tags = cls.objects.filter(pid=post_id)

        # 删除不在需要的 Tag 关系
        for pt in post_tags:
            if pt.tid not in tid_list:
                pt.delete()

        # 新关系
        new_post_tag_ids = set(tid_list) - set(pt.tid for pt in post_tags)
        new_post_tags = [PostTags(pid=post_id, tid=tid) for tid in new_post_tag_ids]
        cls.objects.bulk_create(new_post_tags)
