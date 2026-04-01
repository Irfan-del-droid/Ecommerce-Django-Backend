class DatabaseRouter:
    """
    A router to control all database operations on models in the
    built-in Django apps and our custom apps.
    """
    built_in_apps = {'admin', 'auth', 'contenttypes', 'sessions', 'messages', 'staticfiles'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.built_in_apps:
            return 'default'
        return 'mongodb'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.built_in_apps:
            return 'default'
        return 'mongodb'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.built_in_apps:
            return db == 'default'
        return db == 'mongodb'
