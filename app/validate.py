def if_empty_string(**data):
    '''method to validate empty string'''
    messages = {}
    for key in data:
        newname = re.sub(r'\s+', '', data[key])
        if not newname:
            message = {'message': key + ' cannot be an empty string'}
            messages.update({key + '-Error:': message})
    return messages

def has_whitespace(data):
    '''method to validate whitespace'''
    newname = re.sub(r'\s+', '', data)
    afterlength = len(newname)
    actuallength = len(data)
    if afterlength != actuallength:
        return True

def value_none(**data):
    '''method to check none for values'''
    messages = {}
    for key in data:
        if data[key] is None:
            message = {'message': key + ' cannot be missing'}
            messages.update({key + '-Error:': message})
    return messages

def pass_length(data):
    """ Function determines if password length is less than 8 digits"""
    if len(data) < 8:
        return True

def validate_email_ptn(data):
    """ Function validates user email to match email pattern"""
    pattern = re.match(
        r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data)
    if not pattern:
        return True
