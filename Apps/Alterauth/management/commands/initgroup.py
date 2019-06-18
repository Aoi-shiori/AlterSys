#encodeing:utf-8

#用于初始化用户分组
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,ContentType,Permission
from Apps.Alter_management.models import Alter_managment
from Apps.Alter_execute.models import Alter_execute
#必须有一个类叫Command让其继承BaseCommand
class Command(BaseCommand):
    def handle(self, *args, **options):
        #1.提交编辑组 2.审核组 3执行组、4、超级管理员组
        editorandrevirce_group={
            ContentType.objects.get_for_model(Alter_managment)
        }
        e

        execute_group = {
            ContentType.objects.get_for_model(Alter_execute)
        }
        self.stdout.write(self.style.SUCCESS("hello word"))
