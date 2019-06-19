#encodeing:utf-8

#用于初始化用户分组
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,ContentType,Permission
from Apps.Alter_management.models import Alter_managment
from Apps.Alter_execute.models import Alter_execute
#必须有一个类叫Command让其继承BaseCommand
class Command(BaseCommand):
    def handle(self, *args, **options):
        #1.编辑审核组
        Review_editor_content_type={
            ContentType.objects.get_for_model(Alter_managment)
        }
        Review_editor_permissions=Permission.objects.filter(content_type__in=Review_editor_content_type)
        Review_editor_Group=Group.objects.create(name="编辑审核")
        Review_editor_Group.permissions.set(Review_editor_permissions)
        Review_editor_Group.save()
        self.stdout.write(self.style.SUCCESS("编辑审核组创建成功"))


       # 2、执行组、
        execute_content_type = {
            ContentType.objects.get_for_model(Alter_execute)
        }
        execute_permissions=Permission.objects.filter(content_type__in=execute_content_type)
        executeGroup=Group.objects.create(name="执行组")
        executeGroup.permissions.set(execute_permissions)
        executeGroup.save()
        self.stdout.write(self.style.SUCCESS("执行组创建成功"))


        #3、管理员组
        admin_permissions=Review_editor_permissions.union(execute_permissions)
        adminGroup=Group.objects.create(name='管理员组')
        adminGroup.permissions.set(admin_permissions)
        adminGroup.save()
        self.stdout.write(self.style.SUCCESS("管理员组创建成功"))