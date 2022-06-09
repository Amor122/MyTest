import uuid
from django.db import models
from django.contrib.auth.hashers import make_password


class HumanCommon(models.Model):
    """虚拟公共模型类"""
    objects = models.Manager()
    id = models.UUIDField(primary_key=True, verbose_name='ID')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """ 重写保存方法，将UUID形式的id保存"""
        if self.id is None:
            self.id = uuid.uuid4().hex
        super().save()

    class Meta:
        abstract = True


class Permission(HumanCommon):
    class Meta:
        db_table = 'permissions'
        verbose_name = verbose_name_plural = '权限类型'

    permission_name = models.CharField(max_length=30, verbose_name='权限名称')
    permission_number = models.IntegerField(default=0, verbose_name='权限量级')

    def __str__(self):
        return self.permission_name


class OrganizationType(HumanCommon):
    class Meta:
        db_table = 'organization_type'
        verbose_name = verbose_name_plural = '组织类型'

    organization_type_name = models.CharField(max_length=30, verbose_name='组织类型名称')
    # 组织有对应的权限，多对多关系
    permissions = models.ManyToManyField(Permission, db_table='organization_permission',
                                         related_name='organization_types', verbose_name='组织权限列表', null=True)

    def __str__(self):
        return self.organization_type_name


class Organization(HumanCommon):
    class Meta:
        db_table = 'organization'
        verbose_name = verbose_name_plural = '组织信息'

    # 自关联
    up_organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='down_organization', verbose_name='上级组织')
    organization_type = models.ForeignKey(OrganizationType, on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name='down_organization', verbose_name='组织类型')

    organization_name = models.CharField(max_length=30, verbose_name='组织名称',unique=True)

    def __str__(self):
        return self.organization_name


class HumanPost(HumanCommon):
    class Meta:
        db_table = 'human_post'
        verbose_name = verbose_name_plural = '职务信息'

    post_name = models.CharField(max_length=20, unique=True, verbose_name='职位名称')
    is_primary = models.BooleanField(verbose_name='是否主导所在组织', default=False)

    def __str__(self):
        return self.post_name


class Human(HumanCommon):
    class Meta:
        db_table = 'human_beings'
        verbose_name = verbose_name_plural = '人员信息'

    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='members', verbose_name='所属组织')
    user_id = models.CharField(max_length=18, unique=True, verbose_name='唯一识别编号、账号')
    user_name = models.CharField(max_length=50, verbose_name='姓名')
    # 在输入上控制密码小于16位，保存其md5 De hash值作为密码
    password = models.CharField(max_length=128, verbose_name='密码', default='abc123456', blank=True)
    post = models.ForeignKey(HumanPost, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='职务')

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.password and len(self.password) < 50:
            self.password = make_password(self.password)
        super().save()

    def __str__(self):
        return f'{self.user_id}:{self.user_name}'
