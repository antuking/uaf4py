<div align="center">
<img src="images/uaf.svg" width="600" height="500"/>

# `UAF`
<p class="align center">

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
![Build](https://github.com/suneel944/uaf/actions/workflows/tests.yml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

A universal automation framework to handle mobile testing, web testing, api testing in a single powerful python package with capabilities like device farming and so on.

## Features

- Web automation
- API automation
- Mobile automation
- Device farming
- ChatGpt integration
- Allure docker service integration

## Prerequisites
 - knowledge of appium
 - knowledge of selenium
 - knowledge of python
 - knowledge of api testing

## Installation

There are two ways in which the framework can be utilised:
- Build the package and install it to current working directory
- Or, utilise the framework as is by creating a testing layer

### Steps:
- **Prep the system:**
    - Install [docker](https://www.docker.com/products/docker-desktop/)
        - [Windows installation](https://docs.docker.com/desktop/install/windows-install/)
        - [Linux installation](https://docs.docker.com/desktop/install/linux-install/)
        - [Mac installation](https://docs.docker.com/desktop/install/mac-install/)

    - Install `libq` dependency for `psycopg` which caters the postgres requirement usig below commands

        ```bash
        # ubuntu
        sudo apt-get update
        sudo apt-get install libpq-dev

        # mac
        brew install libpq
        brew link --force libpq
        ```
    
    - Install [appium](https://appium.io/downloads.html)

    - Install [appium inspector](https://github.com/appium/appium-inspector/releases)

    - Install [android studio](https://developer.android.com/studio)
        - cli tools and sdkmanager need to be properly installed and configured, as in the later part these are required in automatic creation of emulators for testing using device farming
        - avdmanager, sdkmanager command availability in the terminal/cmd/powershell

    - Install [xcode](https://apps.apple.com/us/app/xcode/id497799835?mt=12) - **Optional - applicable only to mac device users**

    - Install [Python](https://www.python.org/downloads/) **(version >= 3.11 and < 3.12)**

    - Install [Make](https://formulae.brew.sh/formula/make)

    - Install [Pip](https://pip.pypa.io/en/stable/cli/pip_install/)

    - Install [Tox](https://pypi.org/project/tox/)

    - Install [Pre-commit](https://pypi.org/project/pre-commit/)

    - Install IDE of your choice, (recommended: [VSCode](https://code.visualstudio.com/) or [Cursor](https://cursor.sh/))

- **Prep project:**
    - The `.env` file is created at the root of the project and contains the following environment variables:
      
      ```bash
      MONGO_INITDB_ROOT_USERNAME=admin
      MONGO_INITDB_ROOT_PASSWORD=admin123
      RABBITMQ_DEFAULT_USER=admin
      RABBITMQ_DEFAULT_PASS=admin123
      UID=1000
      GID=1000
      ```

    - Adjust the `UID` and `GID` to match your system user (check using `id` command).

    - There is an inbuilt device farming capability, and for this, we need to execute the below command:
        - The command invokes two dashboards and two databases to manage device farming activities:
            - **RabbitMQ** 
                - Username: `admin`
                - Password: `admin123`
                - [URL](http://localhost:15672/)
            - **Mongo Express**
                - [URL](http://localhost:8081/)
                - Initial login credentials:
                    - Username: `admin`
                    - Password: `pass`
    - Once the Docker containers are up, the next step is to prep MongoDB and add some data so that it starts working:
        - Execute the below docker command:
            
            ```bash
            sudo docker compose up --build
            # OR
            sudo docker compose -d --build
            ```

        - To provide proper read write permissions for the `allure-reports` and `allure-results` folder execute the below command

            ```bash
            sudo chown -R $(whoami):$(whoami) ./allure-results ./allure-reports
            ```

        - Create a database called **appium_device_stats**
    
        - In the created database, create two collections:
            - **device_stats**: Holds data pertaining to device availability
            - **device_sessions**: Holds data pertaining to device sessions

    - Make sure you have the following installed before diving into the action

    - To prepare your project python dependencies, execute the following commands in order:

        ```bash
        make tox PYTHON_VERSION="3114" # supported versions: [3114 => python 3.11.4, 3115 => python 3.11.5, 3116 => python 3.11.6, 3117 => python 3.11.7, 3118 => python 3.11.8, 3119 => python 3.11.9]. Make sure to check that your installed Python version matches one from the list.
        ```

    - To activate the Tox environment, use the following commands:
        
        ```bash
        # Ensure the .tox folder exists in the root project directory.
        # On macOS/Linux:
        source .tox/<envname>/bin/activate
        # On Windows:
        .\.tox\<envname>\Scripts\activate
        ```

    - Replace `<envname>` with the environment name, typically 'py'. If Tox is configured for different environments, it might be 'py31xx'.

    - When using your preferred IDE, update the interpreter path. Here's how to do it:

        ```bash
        which python3
        ```

    - This command outputs the path of the active interpreter, but ensure the Tox environment is activated first.

    - For [VSCode](https://code.visualstudio.com/) or [Cursor](https://cursor.sh/):

        1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS).
        2. In the drop-down, type `Python: Select Interpreter` and choose the first option.
        3. In the next drop-down, select `Enter interpreter path...` and input the path from `which python3`.
        4. Hit enter, and your IDE should now be configured correctly.

    - For [PyCharm](https://www.jetbrains.com/pycharm/), refer to their documentation for setting the interpreter path, as the process may differ.

    - Now the project setup is done, lets proceed to next step

## Invoke Celery

- Invoke Celery to check if everything is working fine:
      
    ```bash
    celery -A uaf.device_farming.device_tasks worker -B -E -O fair --loglevel=INFO
    ```

    - **Celery**: The command-line tool for managing Celery tasks.
        - **-A uaf.device_farming.device_tasks**: The app instance to use, where `uaf.device_farming.device_tasks` is the Python module containing the Celery application.
        - **worker**: Starts a worker process that will process tasks.
        - **-B**: Enables the Celery beat scheduler, allowing the worker to manage periodic tasks defined in the Celery configuration.
        - **-E**: Enables event monitoring, allowing you to track tasks in real-time, useful for monitoring and debugging.
        - **-O fair**: Optimizes the worker to schedule tasks in a "fair" manner, meaning each worker gets an equal number of tasks over time.
        - **--loglevel=INFO**: Sets the log level to INFO, providing general information about the worker's activity.

## Encrypt/decrypt sensitive information
- Currently the project hosts sensitive data, which is encrypted using in house encryption using cryptography lib and since the file is encrypted and will remain encrypted indefinetly. Below is the template that needs to be followed for the same, at least initially to make the scripts and the project work. Later it can be modified according to the taste of individuals/ teams
    
    ```yaml
    info:
        name: Common

    ports:
        appipum_service_min_port_band: <min_port_number>
        appium_service_max_port_band: <max_port_number>

    appium:
        appium_base_url_local: http://localhost:${port}/wd/hub
        appium_base_url_remote: http://localhost:${port}/wd/hub

    celery:
        broker_url: amqp://<username>:<password>@localhost:5672
        result_backend: rpc://<username>>:<password>@localhost:5672

    mongodb:
        connection_string: mongodb://<username>>:<password>@localhost:27017/appium_device_stats?authSource=admin&authMechanism=SCRAM-SHA-256
        device_stat_collection: device_stats
        device_session_collection: device_sessions

    chatgpt:
        api_key: <chat_gpt_api_key>
        engine: <chat_gpt_model>
        max_tokens: <max_token>
        temperature: <temperature>

    waits:
        max_time_out: <max_time_out_time_in_seconds_for_webdriver_wait>
    ```

- To encrypt/decrypt sensitive information, use the generated AES-256 key
  - If there is no AES-256 key present or if it is the first time that a script is being run then follow the below steps
    - Open a python console which is pointing to project root and type the below
        
        ```bash
        python cli.py --mode generate_key
        ```

    - Copy the generated key and store it in the project directory inside a .env file for reference, create one if not present
  - Now that we have a key handy, we can proceed with the sensitive data file encryption or decryption depending on the scenario
    - To encrypt the data file
      
        ```bash
        python cli.py --mode encrypt --key <generated_secret_key> --data_file <relative_file_path>
        ```

    - To decrypt the data file
        
        ```bash
        python cli.py --mode decrypt --key <generated_secret_key> --data_file <relative_file_path>
        ```

## Contributing

We welcome contributions to this project! Before you start, please read our [CONTRIBUTING.md](CONTRIBUTING.md) file. It contains important information about our development process, coding standards, and how to submit pull requests.

Key points:
- We use [Conventional Commits](https://www.conventionalcommits.org/) for our commit messages.
- Our version bumping is automated based on these commit messages.
- Please ensure your code follows our style guide and passes all tests.

Your contributions help make this project better for everyone. Thank you for your support!

## Running Tests
- Now everything is setup and running fine, one final thing to test if things are really working. To run tests, run the following command

    ```bash
    pytest
    # OR
    pytest -v <relative_path_testclass_py_file>
    # OR
    pytest -v <relative_path_testclass_py_file>::<testcase_method_name>
    # OR
    pytest -v -m <tag_name>
    ```

- To run the test parallelly

    ```bash
    pytest -n <number_of_parallel_threads>
    # OR
    pytest -v <relative_path_testclass_py_file> -n <number_of_parallel_threads>
    # OR
    pytest -v -m <tag_name> -n <number_of_parallel_threads>
    ```

- To run the test and visualise report using allure
  - The allure reports will be available in the allure-reports which can be found in the project root 
      
      ```bash
        pytest -n <number_of_parallel_threads> --alluredir=allure-results
        # OR
        pytest -v <relative_path_testclass_py_file> -n <number_of_parallel_threads> --alluredir=allure-results
        # OR
        pytest -v -m <tag_name> -n <number_of_parallel_threads> --alluredir=allure-results
        ```

 - For more information on pytest, feel free to read the [docs](https://docs.pytest.org/en/7.1.x/contents.html)
