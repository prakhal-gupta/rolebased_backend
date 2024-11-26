import pandas as pd


def create_update_record(request, serializer_class, model_class):
    request_data = request.data.copy() if not isinstance(request, dict) else request
    data_id = request_data.pop('id', None)
    if data_id:
        data_obj = model_class.objects.get(id=data_id)
        serializer = serializer_class(instance=data_obj, data=request_data, partial=True, context={"request": request})
    else:
        serializer = serializer_class(data=request_data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    update_object = serializer.save()
    return serializer_class(instance=update_object).data


def create_update_bulk_records(request, serializer_class, model_class):
    request_data = request.data.copy() if not type(request) == type(list()) else request
    save_data, errors, raise_error = [], [], False
    for record in request_data:
        record = dict(record)
        data_id = record.pop('id', None)
        if data_id:
            data_obj = model_class.objects.get(id=data_id)
            serializer = serializer_class(instance=data_obj, data=record, partial=True, context={"request": record})
        else:
            serializer = serializer_class(data=record, context={"request": request})
        validation = serializer.is_valid()
        if validation:
            save_data.append(serializer)
            errors.append({})
        else:
            save_data.append({})
            errors.append(serializer.errors)
            raise_error = True
    if raise_error:
        return {"success": False, "errors": errors}
    else:
        saved_data = []
        for record in save_data:
            update_object = record.save()
            saved_data.append(serializer_class(instance=update_object).data)
        return {"success": True, "data": saved_data}


def validate_serializer_data(record, serializer_class, model_class):
    data_id = record.pop('id', None)
    if data_id:
        data_obj = model_class.objects.get(id=data_id)
        serializer = serializer_class(instance=data_obj, data=record, partial=True)
    else:
        serializer = serializer_class(data=record)
    return serializer.is_valid(raise_exception=True)


def validate_serializer_multiple(data, serializer_class, model_class):
    errors, raise_error = [], False
    for record in data:
        record = dict(record)
        data_id = record.pop('id', None)
        if data_id:
            data_obj = model_class.objects.get(id=data_id)
            serializer = serializer_class(instance=data_obj, data=record, partial=True)
        else:
            serializer = serializer_class(data=record)
        validation = validate_serializer_data(record, serializer_class, model_class)
        if validation:
            errors.append({})
        else:
            errors.append(serializer.errors)
            raise_error = True
    return {"success": False, "errors": errors} if raise_error else {"success": True}


def get_status(item):
    if item.is_approved:
        return "Approved"
    elif item.is_rejected:
        return "Rejected"
    return "Pending"


def get_full_name(user):
    if user and user.middle_name:
        return user.first_name + " " + user.middle_name + " " + user.last_name
    elif user:
        return user.first_name + " " + user.last_name
    return ""


def get_full_name_dict(user_dict):
    if user_dict and "middle_name" in user_dict and user_dict["middle_name"]:
        return user_dict["first_name"] + " " + user_dict["middle_name"] + " " + user_dict["last_name"]
    elif user_dict:
        return user_dict["first_name"] + " " + user_dict["last_name"]
    return "--"


def get_full_name_code_dict(user_dict):
    if user_dict and "middle_name" in user_dict and user_dict["middle_name"]:
        return "(" + user_dict["employee_code_data"] + ") " + user_dict["first_name"] + " " + user_dict[
            "middle_name"] + " " + user_dict["last_name"]
    elif user_dict:
        return "(" + user_dict["employee_code_data"] + ") " + user_dict["first_name"] + " " + user_dict["last_name"]
    return "--"


def get_clean_date(date):
    if date:
        return pd.to_datetime(date).strftime("%d-%m-%Y")
    return "--"


def gb_to_bytes(gb):
    if gb:
        bytes = gb * 1024 * 1024 * 1024
        return bytes
    return 0


def gb_to_mb(gb):
    if gb:
        mb = gb * 1024
        return mb
    return 0


def bytes_to_mb(bytes):
    if bytes:
        mb = bytes / (1024 * 1024)
        return mb
    return 0


def create_update_manytomany_record(request_data, model_class, many_queryset=None):
    values = []
    if many_queryset:
        for record in many_queryset.all():
            record.is_active = False
            record.save()
    for record in request_data:
        record.pop('id', None)
        values.append(model_class.objects.create(**record).id)
    return values
