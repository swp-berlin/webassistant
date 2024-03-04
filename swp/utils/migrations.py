from django.db import migrations


def get_queryset(apps, schema_editor, *model):
    return apps.get_model(*model).objects.using(schema_editor.connection.alias)


def get_object(apps, schema_editor, app_label, model, **query):
    return get_queryset(apps, schema_editor, app_label, model).filter(**query).first()


def get_group(apps, schema_editor, name):
    return get_object(apps, schema_editor, 'auth', 'Group', name=name)


def get_permission(apps, schema_editor, app_label, codename):
    return get_object(apps, schema_editor, 'auth', 'Permission', content_type__app_label=app_label, codename=codename)


class AddRolePerm(migrations.RunPython):

    def __init__(self, role, perm, app_label='swp', **kwargs):
        self.role = role
        self.perm = perm
        self.app_label = app_label

        kwargs.setdefault('code', self.add_perm_to_group)
        kwargs.setdefault('reverse_code', self.remove_perm_from_group)

        super().__init__(**kwargs)

    def add_perm_to_group(self, apps, schema_editor):
        group, permission = self.get_objects(apps, schema_editor)

        if group and permission:
            return group.permissions.add(permission)

    def remove_perm_from_group(self, apps, schema_editor):
        group, permission = self.get_objects(apps, schema_editor)

        if group and permission:
            return group.permissions.remove(permission)

    def get_objects(self, apps, schema_editor):
        group = get_group(apps, schema_editor, self.role)
        permission = get_permission(apps, schema_editor, self.app_label, self.perm)

        return group, permission
