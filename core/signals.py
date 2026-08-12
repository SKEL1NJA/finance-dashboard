from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_delete, post_save

from .middleware import get_current_user
from .models import AuditLog

TRACKED_MODELS = [
    'accounts.Account',
    'transactions.Transaction',
    'transactions.CategorizationRule',
    'budgets.Budget',
    'goals.SavingsGoal',
]


def resolve_user():
    user = get_current_user()
    if user is not None and getattr(user, 'is_authenticated', False):
        return user
    return None


def log_save(sender, instance, created, **kwargs):
    if created:
        action = 'create'
    elif getattr(instance, 'is_deleted', False):
        action = 'delete'
    else:
        action = 'update'

    AuditLog.objects.create(
        user=resolve_user(),
        action=action,
        content_type=ContentType.objects.get_for_model(sender),
        object_id=str(instance.pk),
    )


def log_hard_delete(sender, instance, **kwargs):
    AuditLog.objects.create(
        user=resolve_user(),
        action='delete',
        content_type=ContentType.objects.get_for_model(sender),
        object_id=str(instance.pk),
    )


def register_audit_signals():
    from django.apps import apps

    for label in TRACKED_MODELS:
        model = apps.get_model(label)
        post_save.connect(log_save, sender=model, weak=False)
        post_delete.connect(log_hard_delete, sender=model, weak=False)