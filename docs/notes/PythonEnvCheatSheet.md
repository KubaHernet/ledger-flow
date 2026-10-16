# Python Virtual Environment Cheat Sheet

## 1. Create a virtual environment

From the project folder:

```powershell
py -3.13 -m venv .venv
```

This creates:

```text
.venv/
```

inside the project.

---

## 2. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

After activation, the terminal should look similar to:

```text
(.venv) PS C:\repos\ledger-flow\backend>
```

To deactivate it:

```powershell
deactivate
```

---

## 3. Install `pip` if it is missing

Usually `pip` is installed automatically with the virtual environment.

If it is missing:

```powershell
python -m ensurepip --upgrade
```

Then update it:

```powershell
python -m pip install --upgrade pip
```

Verify:

```powershell
python -m pip --version
```

---

## 4. Install a package

Example: SQLAlchemy

```powershell
python -m pip install sqlalchemy
```

Example: FastAPI

```powershell
python -m pip install fastapi
```

Verify that a package is installed:

```powershell
python -m pip show sqlalchemy
```

Prefer:

```powershell
python -m pip install <package>
```

over:

```powershell
pip install <package>
```

because it makes sure `pip` belongs to the currently selected Python interpreter.

---

## 5. Install packages from `requirements.txt`

Example `requirements.txt`:

```text
fastapi
uvicorn
sqlalchemy
```

Install all dependencies:

```powershell
python -m pip install -r requirements.txt
```

---

## Useful commands

List installed packages:

```powershell
python -m pip list
```

Save currently installed packages:

```powershell
python -m pip freeze > requirements.txt
```

Check which Python is currently being used:

```powershell
where.exe python
```

When the virtual environment is active, the first result should point to something like:

```text
C:\repos\ledger-flow\backend\.venv\Scripts\python.exe
```