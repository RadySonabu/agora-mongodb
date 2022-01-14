from fastapi import  Request

def PaginatedResponseModel(data, message, count, offset, limit, request: Request ):
    client_host = str(request.url)
    host = client_host.rsplit('/',1)[0]

    if offset == 0:
        prev_page = None
    else:
            prev_page = f'{host}/?offset={offset}&limit={limit}'

    if int(count) > limit:
            next_page = f'{host}/?offset={offset}&limit={limit}'
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