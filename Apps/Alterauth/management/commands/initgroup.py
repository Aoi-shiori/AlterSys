#encodeing:utf-8

#用于初始化用户分组
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group,ContentType,Permission
from Apps.Alter_management.models import Alter_managment
from Apps.Alter_execute.models import Alter_execute
from Apps.Alter_Dict.models import Alt_Database,Alt_Hospital,Alt_Type
#必须有一个类叫Command让其继承BaseCommand
class Command(BaseCommand):
    def handle(self, *args, **options):
        #1.研發組
        Research_content_type={
            ContentType.objects.get_for_model(Alter_managment)
        }
        Research_permissions=Permission.objects.filter(content_type__in=Research_content_type)
        Research_Group=Group.objects.create(name="研发组")
        Research_Group.permissions.set(Research_permissions)
        pers = Permission.objects.filter(codename__in=['review_alter_managment',])
        for per in pers:
            Research_Group.permissions.remove(per)
        Research_Group.save()
        self.stdout.write(self.style.SUCCESS("研发组创建成功"))


       # 2、實施組、
        execute_content_type = {
            ContentType.objects.get_for_model(Alter_execute)
        }
        execute_permissions=Permission.objects.filter(content_type__in=execute_content_type)
        executeGroup=Group.objects.create(name="实施组")
        executeGroup.permissions.set(execute_permissions)
        executeGroup.save()
        self.stdout.write(self.style.SUCCESS("实施组创建成功"))

        #3、管理員組
        admin_content_type = {
            ContentType.objects.get_for_model(Alter_execute),
            ContentType.objects.get_for_model(Alter_managment),
            ContentType.objects.get_for_model(Alt_Hospital),
            ContentType.objects.get_for_model(Alt_Type),
            ContentType.objects.get_for_model(Alt_Database)

        }
        admin_permissions=Permission.objects.filter(content_type__in=admin_content_type)
        adminGroup=Group.objects.create(name="管理员组")
        adminGroup.permissions.set(admin_permissions)
        adminGroup.save()
        self.stdout.write(self.style.SUCCESS("管理员组创建成功"))

        # #3、超級管理员
        # admin_permissions=Review_editor_permissions.union(execute_permissions)
        # adminGroup=Group.objects.create(name='超級管理員')
        # adminGroup.permissions.set(admin_permissions)
        # adminGroup.save()
        # self.stdout.write(self.style.SUCCESS("超級管理員组创建成功"))