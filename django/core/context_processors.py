from website import settings

def siteconfig (context):
    data = {
        'piwiki':   settings.PIWIKI,
        'debug':    settings.DEBUG,
    }
    return {'config': data}
