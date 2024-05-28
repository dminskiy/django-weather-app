import os


cmds = [
    "python /wdir/src/manage.py makemigrations",
    "python /wdir/src/manage.py migrate",
    "python /wdir/src/manage.py runserver 0.0.0.0:8000",
]

if __name__ == "__main__":
    # Execute commands from the list
    for cmd in cmds:
        os.system(cmd)
