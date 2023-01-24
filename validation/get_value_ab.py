def get_value_ab(ab, phone, birthday, email, address):
    if not birthday and not email and not address:
        ab.phone = phone
    elif birthday is not None and not email and not address:
        ab.phone = phone
        ab.birthday = birthday
    elif birthday is not None and email != '' and not address:
        ab.phone = phone
        ab.birthday = birthday
        ab.email = email
    else:
        ab.phone = phone
        ab.birthday = birthday
        ab.email = email
        ab.address = address