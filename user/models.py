from django.db import models


class Promission(models.Model):
    p_name = models.CharField(max_length=20, verbose_name='权限名称')

    class Meta:
        db_table = 'ttsx_promission'


class Role(models.Model):
    r_name = models.CharField(max_length=20)
    r_p = models.ManyToManyField(Promission)

    class Meta:
        db_table = 'ttsx_role'


class User(models.Model):
    username = models.CharField(max_length=20, verbose_name='用户名', unique=True)
    password = models.CharField(max_length=255, verbose_name='密码')
    email = models.CharField(max_length=255, verbose_name='邮箱', unique=True)
    r = models.ForeignKey(Role, default=1)

    class Meta():
        db_table = 'ttsx_user'


class UserAddress(models.Model):
    tel = models.CharField(max_length=50, verbose_name='电话', unique=True)
    address = models.CharField(max_length=255, verbose_name='地址')
    zcpde = models.CharField(max_length=20, verbose_name='姓名')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta():
        db_table = 'ttsx_address'


class UserTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 关联用户
    ticket = models.CharField(max_length=256)  # 密码
    out_time = models.DateTimeField()  # 过期时间

    class Meta:
        db_table = 'ttsx_ticket'
