from firebase_admin import db


def get_supported_coins(path):
    ref = db.reference(path)
    return ref.get()


def get_supported_coins_ids(path):
    ref = db.reference(path)
    return list(ref.get().values())


def get_supported_coins_sym(path):
    ref = db.reference(path)
    return list(ref.get().keys())
