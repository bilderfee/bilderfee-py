from bilderfee.bilderfee import Gravity
from bilderfee.bilderfee import Ext


def bilderfee_ctx(request):
    return {
        'BF_GRAVITY_SMART': Gravity.SMART,
        'BF_GRAVITY_NORTH': Gravity.NORTH,
        'BF_GRAVITY_SOUTH': Gravity.SOUTH,
        'BF_GRAVITY_EAST': Gravity.EAST,
        'BF_GRAVITY_WEST': Gravity.WEST,
        'BF_GRAVITY_CENTER': Gravity.CENTER,
        # File Extension
        'BF_EXT_JPEG': Ext.JPEG,
        'BF_EXT_PNG': Ext.PNG,
        'BF_EXT_GIF': Ext.GIF,
        'BF_EXT_WEBP': Ext.WEBP,
        'BF_EXT_ICO': Ext.ICO,
    }
