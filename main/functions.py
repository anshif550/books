def generate_form_errors(form):
    message =""
    for feld in form:
        if feld.errors:
            message += feld.errors
    for err in form.non_field_errors():
        message += str(err)
        
        return message