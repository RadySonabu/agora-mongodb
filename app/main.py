import uvicorn
from server.app import *
# from mangum import Mangum
# handler = Mangum(app)
if __name__ == "__main__":
    uvicorn.run('server.app:app', host="0.0.0.0", port=8000, reload=True)