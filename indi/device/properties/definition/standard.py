from indi.message import const
from ... import properties

"""
Standard property vector factory as defined in http://indilib.org/develop/developer-manual/101-standard-properties.html
"""

_STANDARD_VECTORS = {

    # GENERAL

    'CONNECTION': {
        'class': properties.SwitchVector,
        'elements': dict(
            connect='CONNECT',
            disconnect='DISCONNECT',
        ),
        'kwargs': {
            'rule': const.SwitchRule.ONE_OF_MANY,
            'default_on': 'DISCONNECT',
        },
    },

    'UPLOAD_MODE': {
        'class': properties.SwitchVector,
        'elements': dict(
            client='UPLOAD_CLIENT',
            local='UPLOAD_LOCAL',
            both='UPLOAD_BOTH',
        ),
        'kwargs': {
            'rule': const.SwitchRule.ONE_OF_MANY,
        },
    },

    'ACTIVE_DEVICES': {
        'class': properties.TextVector,
        'elements': {},
        'kwargs': {
            'perm': const.Permissions.READ_ONLY,
        },
    },

    # CCD

    'CCD_EXPOSURE': {
        'class': properties.NumberVector,
        'elements': dict(
            time='CCD_EXPOSURE_VALUE',
        ),
    },

    'CCD_COMPRESSION': {
        'class': properties.SwitchVector,
        'elements': dict(
            compress='CCD_COMPRESS',
            raw='CCD_RAW',
        ),
        'kwargs': {
            'rule': const.SwitchRule.ANY_OF_MANY,
        },
    },

    # FOCUSER

    'ABS_FOCUS_POSITION': {
        'class': properties.NumberVector,
        'elements': dict(
            position='FOCUS_ABSOLUTE_POSITION',
        ),
    },

}


def Standard(name, **kwargs):
    definition = _STANDARD_VECTORS[name]

    def_kwargs = definition['kwargs'] if 'kwargs' in definition else {}
    def_kwargs['elements'] = {k: definition['class'].element_class(n) for k, n in definition['elements'].items()}

    kwargs = {
        **def_kwargs,
        **kwargs,
    }

    return definition['class'](name, **kwargs)
