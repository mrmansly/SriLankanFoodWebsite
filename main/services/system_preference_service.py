from ..models import SystemPreference

BOOLEAN_TYPE = "boolean"
STRING_TYPE = "string"
INT_TYPE = "int"
FLOAT_TYPE = "float"


def get_preference(preference_name) -> SystemPreference:
    try:
        preference = SystemPreference.objects.get(name=preference_name)
    except SystemPreference.DoesNotExist:
        raise ValueError(f"System preference: {preference_name} does not exist.")
    return preference


# Use this method for returning a boolean (assuming the preference is a boolean type)
def is_enabled(preference_name) -> bool:
    preference = get_preference(preference_name)
    if preference.type != BOOLEAN_TYPE:
        raise ValueError(f"System preference: {preference_name} is not a boolean value.")
    elif preference.value not in ['True', 'False']:
        raise ValueError(f"System preference: {preference_name} has an invalid boolean value: {preference.value}.")

    return True if preference.value == 'True' else False


# Use this method for returning the value of the system preference, converted to its expected type
def get_value(preference_name) -> bool or str or int or float:
    preference = get_preference(preference_name)

    if preference.type not in [INT_TYPE, FLOAT_TYPE, STRING_TYPE, BOOLEAN_TYPE]:
        raise ValueError(f"System preference: {preference_name} has an invalid type: {preference.type}")

    if preference.type == INT_TYPE:
        return int(preference.value)
    elif preference.type == FLOAT_TYPE:
        return float(preference.value)
    elif preference.type == BOOLEAN_TYPE:
        return is_enabled(preference_name)

    # String
    return preference.value

