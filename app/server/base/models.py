from fastapi import  Request

def PaginatedResponseModel(data, message, count, offset, limit, request: Request ):
    client_host = str(request.url)
    host = client_host.rsplit('/',1)[0]
    prev_current_offset = offset
    next_current_offset = offset
    if prev_current_offset == 0:
        prev_page = None
    else:
        if prev_current_offset:
            prev_current_offset -= 10
        prev_page = f'{host}/?offset={prev_current_offset}&limit={limit}'

    if int(count) > limit:
        if int(count) > next_current_offset:
            next_current_offset += 10
        next_page = f'{host}/?offset={next_current_offset}&limit={limit}'
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