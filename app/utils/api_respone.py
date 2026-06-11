def success_response(data=None, message="Success", status_code=200):
    return {
        "success": True,
        "message": message,
        "data": data
    }, status_code


def error_response(message="Error", status_code=400):
    return {
        "success": False,
        "message": message
    }, status_code