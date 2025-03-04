from django.db import models

# Create your models here.
class SysUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10,unique=True,verbose_name='用户名')
    password = models.CharField(max_length=20,verbose_name='密码')
    avatar = models.CharField(max_length=255,null=True,verbose_name='头像')
    phone_number = models.CharField(max_length=11,null=True,verbose_name='手机号')
    email = models.CharField(max_length=50,null=True,verbose_name='邮箱')
    status = models.IntegerField(null=True,verbose_name='状态,1=启用,0=禁用')
    login_date = models.DateTimeField(null=True,verbose_name='登录时间')
    create_time = models.DateTimeField(null=True,verbose_name='创建时间')
    update_time = models.DateTimeField(null=True,verbose_name='更新时间')
    remark = models.CharField(max_length=20,null=True,verbose_name='备注')

    class Meta:
        db_table = 'sys_user'