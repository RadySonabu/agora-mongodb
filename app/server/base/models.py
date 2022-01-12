from fastapi import  Request

def PaginatedResponseModel(data, message, count, offset, limit, route, request: Request ):
    client_host = request.client.host
    deployment_host = 'agora-web-api.herokuapp.com'
    if offset == 0:
        prev_page = None
    else:
        if client_host == '127.0.0.1':
            prev_page = f'http://{client_host}/{route}/?offset={offset}&limit={limit}'
        else:
            prev_page = f'https://{deployment_host}/{route}/?offset={offset}&limit={limit}'


    if int(count) > limit:
        if client_host == '127.0.0.1':
            next_page = f'http://{client_host}/{route}/?offset={offset}&limit={limit}'
        else:
            next_page = f'https://{deployment_host}/{route}/?offset={offset}&limit={limit}'
    else:
        next_page =None
    return {
        "count": count,
        "prev": prev_page,
        "next": next_page,
        "results": data,
    }

def ResponseModel(data, message):
    return data

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}