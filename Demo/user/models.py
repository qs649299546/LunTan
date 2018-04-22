from django.db import models


class User(models.Model):
    SEX = (
        ('M', '男'),
        ('F', '女'),
        ('U', '保密'),
    )

    nickname = models.CharField(max_length=64, unique=True, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    icon = models.ImageField()
    age = models.IntegerField()
    sex = models.CharField(max_length=8, choices=SEX)

    def has_perm(self, perm_name):
        perm = Permission.objects.get(name=perm_name)
        try:
            Role.objects.get(uid=self.id, perm_id=perm.id)
            return True
        except Role.DoesNotExist as e:
            return False

    def perms(self):
        perm_id_list = [r.perm_id for r in Role.objects.filter(uid=self.id).only('perm_id')]
        return Permission.objects.filter(id__in=perm_id_list)


class Permission(models.Model):
    '''
    权限表
    ============
    id   name
    --   ----
    1    guest
    5    user
    7    manager
    8    boss
    9    leader
    '''
    name = models.CharField(max_length=16, unique=True)


class Role(models.Model):
    uid = models.IntegerField()
    perm_id = models.IntegerField()

    @classmethod
    def add_perm(cls, uid, perm_name):
        '''给用户增加权限'''
        perm = Permission.objects.get(name=perm_name)
        cls.objects.get_or_create(uid=uid, perm_id=perm.id)

    @classmethod
    def del_perm(cls, uid, perm_name):
        '''删除用户权限'''
        perm = Permission.objects.get(name=perm_name)
        try:
            role = cls.objects.get(uid=uid, perm_id=perm.id)
            role.delete()
        except Role.DoesNotExists as e:
            pass
