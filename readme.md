### This is an example of a async api with FastAPI
#### Has script to run migrate and rollback (manual)
##### The active code send messages to AWS SQS but you can switch to Redis or in memory list
##### The project have a consumer to be used in a lambda function

- Run API
```bash
uvicorn app.main:app --reload
```

## Lambda
- Generate libs path to lambda
```bash
cd lambda
pip install -r requirements.txt -t libs/
```

- Publish lambda
- - Gerenate a zip file from full lambda folder
- - Upload the zip file on AWS Lambda Screen in Code tab
- - Publish

### The documentation is available at /docs and /redoc endpoints