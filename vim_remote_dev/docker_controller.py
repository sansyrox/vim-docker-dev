import subprocess

async def return_config_setup_command(config_directory_path):
    return f"git clone {config_directory_path} nvim".split()

def process_env_variables_files(file_path):
    lines = []
    with open(file_path) as f:
        lines = f.readlines()

    return f'export { " ".join(lines) }'

async def setup_environment(service_name, config_directory_path, env_variables_file, editor_install_command, language_server_install_command, editor_choice, plugin_manager_install_command):
    subprocess.call(["docker-compose", "build"])
    subprocess.call(["docker-compose", "run", service_name, *await return_config_setup_command(config_directory_path)])

    # initialise the base directory here
    print("Making the directory")
    subprocess.call(["docker-compose", "run", service_name, "mkdir", "-p", "~/.config/nvim"])

    print("Moving the files")
    subprocess.call(["docker-compose", "run", service_name, "mv", "nvim", "~/.config/nvim"])

    # export commands here
    subprocess.call(["docker-compose", "run", service_name, *( f"sh -c '{env_variables_file}'".split() )])

    subprocess.call(["docker-compose", "run", service_name, "sh", "-c", editor_install_command])
    subprocess.call(["docker-compose", "run", service_name, *( language_server_install_command.split() )])

    subprocess.call(["docker-compose", "run", service_name, f"{editor_choice} -c '{plugin_manager_install_command}' -c 'q'"])


