import subprocess

async def return_config_setup_command(config_directory_path):
    if config_directory_path.startswith("http"):
        return f"git clone {config_directory_path}"
    else:
        return f"cp -R {config_directory_path} ."

def process_env_variables_files(file_path):
    lines = []
    with open(file_path) as f:
        lines = f.readlines()

    return f'export { " ".join(lines) }'

async def setup_environment(service_name, config_directory_path, env_variables_file, editor_install_command, language_server_install_command, editor_choice, plugin_manager_install_command):
    subprocess.call(["docker-compose", "build"])
    subprocess.call(["docker-compose", "run", service_name, await return_config_setup_command(config_directory_path)])
    # export commands here
    subprocess.call(["docker-compose", "run", service_name, f"bash {env_variables_file}"])

    subprocess.call(["docker-compose", "run", service_name, editor_install_command])
    subprocess.call(["docker-compose", "run", service_name, language_server_install_command])

    subprocess.call(["docker-compose", "run", service_name, f"{editor_choice} -c '{plugin_manager_install_command}' -c 'q'"])





