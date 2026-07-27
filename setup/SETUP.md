## Setup for Linux
**1. Zsh and OMZ**

``` sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" ```

OR

``` sh -c "$(wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh -O -)" ```


**2. uv**

``` curl -LsSf https://astral.sh/uv/install.sh | sh ```

**3. VS Code**

Python: add extensions for ruff, pyrefly and disable pylance. Make changes to settings in JSON.

```
{
    "python.languageServer": "None",
    "python.pyrefly.displayTypeErrors": "force-on",
    "editor.defaultFormatter": "charliermarsh.ruff",
    "[python]": {
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.formatOnSave": true
    },
    "files.autoSave": "afterDelay"
}

```

**4. Desktop File template**

```
[Desktop Entry]
Name=AppName
Exec=/home/username/path-to-appImage
Icon=/home/local/.local/share/icons/appName.svg
Type=Application
Categories=Category;
```

**5. Venv alias**

```
function sv {
   local VENV_NAME="${1:-.venv}"
   local ACTIVATE_SCRIPT="${VENV_NAME}/bin/activate"
   if [ -f "${ACTIVATE_SCRIPT}" ]; then
     source "${ACTIVATE_SCRIPT}"
     echo " Activated virtual environment: ${VENV_NAME}"
   else
     echo "Error: Virtual environment script not found at ${ACTIVATE_SCRIPT}"
     echo "Usage: sv [venv_directory_name]"
     return 1
   fi
 }

```