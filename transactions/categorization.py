from .models import CategorizationRule


def suggest_category(user, description):
    if not description:
        return None

    description_lower = description.lower()
    rules = CategorizationRule.objects.filter(user=user).select_related('category')
    matches = [rule for rule in rules if rule.keyword.lower() in description_lower]

    if not matches:
        return None

    matches.sort(key=lambda rule: (rule.priority, len(rule.keyword)), reverse=True)
    return matches[0].category