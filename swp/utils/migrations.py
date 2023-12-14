def get_queryset(apps, schema_editor, *model):
    return apps.get_model(*model).objects.using(schema_editor.connection.alias)
