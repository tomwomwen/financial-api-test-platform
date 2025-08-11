from fastapi import FastAPI

app = FastAPI(title="Financial API",version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Hello World"}
@app.get("/account/balance")
def get_account_balance(account_no: str):
    if account_no == "123456789":
        return {
            "code" : "0000",
            "message" : "success",
            "data": {
                "account_no": account_no,
                "balance": "10000.00",
                "currency": "CNY"
            }
        }
    else:
        return {
            "code" : "1001",
            "message" : "error",
            "data": {}
        }
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)