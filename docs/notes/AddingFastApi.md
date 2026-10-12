1. go to root folder
`cd .\backend\`

2. create a new Python project: `uv init --bare`

--bare: create only the minimal pyproject.toml file, without generating a sample main.py, README.md, or other files. You will create the application files yourself in the next steps of this tutorial.

3. Add Fast Api `uv add "fastapi[standard]`

When you run uv add, it selects compatible versions of FastAPI and all the packages FastAPI depends on. It records the exact versions in uv.lock, making it possible to install the same package versions later on another computer or when deploying the application.

4. Running app
- `cd .\backend\src\ledger_flow`
- `uv 1run fastapi dev`