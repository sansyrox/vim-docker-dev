# app.py
from __future__ import annotations

from typing import TYPE_CHECKING

import rich.box
from rich.panel import Panel
from textual.app import App
from textual.reactive import Reactive
from textual.widgets import  Static
from vim_remote_dev.docker_controller import setup_environment

from vim_remote_dev.header import CustomHeader
from vim_remote_dev.footer import CustomFooter

from textual_inputs import TextInput

if TYPE_CHECKING:
    from textual.message import Message

class SimpleForm(App):

    current_index: Reactive[int] = Reactive(-1)

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.tab_index = ["config_directory", "plugin_manager", "env_variables_file", "vim_or_neovim", "docker_compose_service_name", "editor_install_command", "language_server_install_command"]

    async def on_load(self) -> None:
        await self.bind("ctrl+c", "quit", "Quit")
        await self.bind("ctrl+s", "submit", "Submit")
        await self.bind("escape", "reset_focus", "Reset Focus")
        await self.bind("ctrl+i", "next_tab_index", show=False)
        await self.bind("shift+tab", "previous_tab_index", "Previous Tab")

    async def on_mount(self) -> None:

        self.header = CustomHeader()
        await self.view.dock(self.header, edge="top")
        await self.view.dock(CustomFooter(), edge="bottom")

        self.config_directory = TextInput(
            name="config_directory",
            placeholder="enter your config_directory(local path/git repo)",
            title="Vim/NeoVim Source directory",
        )
        self.config_directory.on_change_handler_name = "handle_config_directory_on_change"

        self.plugin_manager = TextInput(
            name="plugin_manager",
            title="Plugin Manager(VimPlug/Packer/Plug)",
            placeholder="Enter the installation command of your plugin manager"
        )

        self.env_variables_file = TextInput(
            name="env_variables_file",
            placeholder="Path to your env_variables_file. (leave empty if none)",
            title="Environment Variables Files",
        )

        self.env_variables_file.on_change_handler_name = "handle_env_variables_file_on_change"

        self.vim_or_neovim = TextInput(
            name="vim_or_neovim",
            placeholder="Vim/NeoVim",
            title="Editor of Choice",
        )
        self.vim_or_neovim.on_change_handler_name = "handle_env_variables_file_on_change"

        self.docker_compose_service_name = TextInput(
            name="docker_compose_service_name",
            placeholder="Service Name",
            title="docker-compose service name",
        )
        self.docker_compose_service_name.on_change_handler_name = "handle_env_variables_file_on_change"

        self.editor_install_command = TextInput(
            name="editor_install_command",
            placeholder="Command to Install NeoVim/Vim",
            title="Editor Installation Command",
        )
        self.editor_install_command.on_change_handler_name = "handle_env_variables_file_on_change"

        self.language_server_install_command = TextInput(
            name="language_server_install_command",
            placeholder="Command to Install the language server",
            title="Language Server Installation Command",
        )
        self.language_server_install_command.on_change_handler_name = "handle_env_variables_file_on_change"


        self.output = Static(
            renderable=Panel(
                "", title="Neo/Vim Remote Development Config", border_style="blue", box=rich.box.SQUARE
            )
        )
        await self.view.dock(self.output, edge="left", size=40)
        await self.view.dock(
            self.config_directory, self.plugin_manager, self.env_variables_file, self.vim_or_neovim, self.docker_compose_service_name, self.editor_install_command, self.language_server_install_command, edge="top"
        )

    async def action_next_tab_index(self) -> None:
        """Changes the focus to the next form field"""
        if self.current_index < len(self.tab_index) - 1:
            self.current_index += 1
            await getattr(self, self.tab_index[self.current_index]).focus()

    async def action_previous_tab_index(self) -> None:
        """Changes the focus to the previous form field"""
        if self.current_index > 0:
            self.current_index -= 1
            await getattr(self, self.tab_index[self.current_index]).focus()

    async def action_submit(self) -> None:
        formatted = f"""
    Vim Config Source: {self.config_directory.value}
    plugin_manager: {self.plugin_manager.value}
    env_variables_file: {self.env_variables_file.value}
    vim_or_neovim: {self.vim_or_neovim.value}
    docker_compose_service_name: {self.docker_compose_service_name.value}
    editor_install_command: {self.editor_install_command.value}
    language_server_install_command: {self.language_server_install_command.value}
        """
        await self.output.update(
            Panel(formatted, title="Neo/Vim Remote Development Config", border_style="blue", box=rich.box.SQUARE)
        )
        await setup_environment(self.docker_compose_service_name.value, self.config_directory.value, self.env_variables_file.value, self.editor_install_command.value, self.language_server_install_command.value, self.vim_or_neovim.value, self.plugin_manager.value)

    async def action_reset_focus(self) -> None:
        self.current_index = -1
        await self.header.focus()

    async def handle_config_directory_on_change(self, message: Message) -> None:
        self.log(f"Config Directory Field Contains: {message.sender.value}")

    async def handle_env_variables_file_on_change(self, message: Message) -> None:
        self.log(f"Environment Variables File Field Contains: {message.sender.value}")

    async def handle_input_on_focus(self, message: Message) -> None:
        self.current_index = self.tab_index.index(message.sender.name)


if __name__ == "__main__":
    SimpleForm.run(title="Textual-Inputs Simple Form", log="textual.log")
