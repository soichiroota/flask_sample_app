import hashlib


# 引数で与えられたユーザーのGravatar画像を返す
def gravatar_url_for(user, size=80):
    gravatar_id = hashlib.md5(
        user.email.lower().encode()
    ).hexdigest()
    return f"https://secure.gravatar.com/avatar/{gravatar_id}?s={size}"
