# Template-This
`template-this` is a tool to help you quickly create python projects from templates.

## Dependencies

- Python 3.11
- [poetry](https://github.com/python-poetry/poetry)

## Usage
### Basic usage
To create a new project:
```shell
tt path/to/project-name
```
### Options
- `--github` : ssh url to your github repository. If empty, project is created locally without a remote repository.
- `--cli-name` : specify if you want a cli alias in your pyproject.toml. If none are specified, no cli alias nor cli config will be generated.
```shell
tt path/to/project-name --github ssh://github-project-uri --cli-name short-name-command
```

## Setup
To configure the beahviour of the tool, you will need a configuration folder located `~/.cache/template-this`. Minimal setup will look like this:
```shell
~
├───.cache
│     └──template-this
│        │   poetry.yml
│        │   pyproject.toml
```
This folder will contain all the configuration files needed to run the tool.

### `poetry.yml`
You can find an example of a `poetry.yml` in the [`examples` folder](https://github.com/nyx-hemera/template-this/blob/main/examples/poetry.yml).
- `librairies` : list of libraries to install in the project
    - `name` : name of the library
    -  `config` : path to the config file if any you want to add as default
- `vscode_config` : configuration for vscode and Makefile. Should be in a folder named `.vscode`
    - `settings_config` : path to the vscode settings default file. Can be templated with the `cli_name` attribute specified when the command `--cli-name` is used
    - `launch_config` : path to the vscode launch default file
    - `makefile_config` : list of makefile files to add. Can be templated with the `"project_src"` attribute which is the name of the source project folder (aka. project name with '-' replaced by '_')

### `pyproject.toml`
Everything in this file will be added at the end of the file `pyproject.toml` that will be created by poetry. Can be templated with the `cli_name` attribute specified when the command `--cli-name` is used.
You can find an example of a `pyproject.toml` in the [`examples` folder](https://github.com/nyx-hemera/template-this/blob/main/examples/pyproject.toml).

## Example with librairies
Here is an example of the stucture of your `template_this` folder and the `poetry.yml` file using flake8, mypy and pytest.
### Structure
```shell
~
├───.cache
│     └──template-this
│        │   poetry.yml
│        │   pyproject.toml
│        │   .flake8
│        │   mypy.ini
│        │
│        └───.vscode
│                launch.json
│                settings.json
```
### `poetry.yml`
In this case, your `poetry.yml` will look like this:
```toml
librairies:
  - name: "flake8"
    config: ".flake8" 
  - name: "mypy"
    config: "mypy.ini"
  - name: "pytest"
vscode_config:
    settings_config: ".vscode/settings.json"
    launch_config: ".vscode/launch.json"
    makefile_config:
      - "Makefile"
      - "check.ps1"
```


