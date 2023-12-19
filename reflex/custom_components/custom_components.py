"""CLI for creating custom components."""
from __future__ import annotations

import os
from typing import Optional

import typer

from reflex import constants
from reflex.config import get_config
from reflex.constants import CustomComponents
from reflex.utils import console

config = get_config()
custom_components_cli = typer.Typer()


def _create_package_config(module_name: str, package_name: str):
    """Create a package config pyproject.toml file.

    Args:
        module_name: The name of the module.
        package_name: The name of the package.
    """
    from reflex.compiler import templates

    with open(CustomComponents.PYPROJECT_TOML, "w") as f:
        f.write(
            templates.CUSTOM_COMPONENTS_PYPROJECT_TOML.render(
                module_name=module_name, package_name=package_name
            )
        )


def _create_readme(module_name: str):
    """Create a package README file.

    Args:
        module_name: The name of the module.
    """
    from reflex.compiler import templates

    with open(CustomComponents.PACKAGE_README, "w") as f:
        f.write(templates.CUSTOM_COMPONENTS_README.render(module_name=module_name))


def _write_source_py(
    custom_component_src_dir: str,
    component_class_name: str,
    module_name: str,
):
    """Write the source code template for the custom component.

    Args:
        custom_component_src_dir: The name of the custom component source directory.
        component_class_name: The name of the component class.
        module_name: The name of the module.
    """
    from reflex.compiler import templates

    with open(
        os.path.join(
            custom_component_src_dir,
            f"{module_name}.py",
        ),
        "w",
    ) as f:
        f.write(
            templates.CUSTOM_COMPONENTS_SOURCE.render(
                component_class_name=component_class_name, module_name=module_name
            )
        )


@custom_components_cli.command(name="init")
def _init(
    library_name: Optional[str] = typer.Option(
        None,
        help="The name of your library. On PyPI, package will be published as `reflex-{library-name}`.",
    ),
    loglevel: constants.LogLevel = typer.Option(
        config.loglevel, help="The log level to use."
    ),
):
    from reflex.utils import exec, prerequisites

    """Initialize a custom component."""
    console.set_log_level(loglevel)

    # TODO: define pyproject.toml as constants
    if os.path.exists(CustomComponents.PYPROJECT_TOML):
        console.error(f"A {CustomComponents.PYPROJECT_TOML} already exists. Aborting.")
        typer.Exit(code=1)

    # Show system info
    exec.output_system_info()

    # TODO: check the picked name follows the convention

    # if not specified, use the current directory name to form the module name
    if library_name is None:
        raise NotImplementedError(
            "TODO: use the current directory name to form the module name"
        )

    name_parts = library_name.split("-")

    component_class_name = "".join([part.capitalize() for part in name_parts])
    console.info(f"Component class name: {component_class_name}")
    package_name = f"reflex-{library_name}"
    console.info(f"Package name: {package_name}")
    module_name = "_".join(name_parts)
    custom_component_src_dir = f"rx_{module_name}"
    console.info(f"Custom component source directory: {custom_component_src_dir}")
    demo_app_dir = f"{custom_component_src_dir}_demo"
    console.info(f"Demo app directory: {demo_app_dir}")

    console.info(f"Populating pyproject.toml with package name: {package_name}")
    # write pyproject.toml, README.md, etc.
    _create_package_config(module_name=library_name, package_name=package_name)
    _create_readme(module_name=library_name)

    console.info(
        f"Initializing the component source directory: custom_components/{custom_component_src_dir}"
    )
    os.makedirs(custom_component_src_dir)
    _write_source_py(
        custom_component_src_dir=custom_component_src_dir,
        component_class_name=component_class_name,
        module_name=module_name,
    )

    console.info(f"Creating app for testing: {demo_app_dir}")

    # TODO: maybe subprocess to run reflex init in the new folder?

    # Initialize the .gitignore.
    prerequisites.initialize_gitignore()


@custom_components_cli.command(name="build")
def _build(
    loglevel: constants.LogLevel = typer.Option(
        config.loglevel, help="The log level to use."
    ),
):
    """Build a custom component.

    Args:
        loglevel: The log level to use.
    """
    console.set_log_level(loglevel)
    console.print("Building custom component...")


@custom_components_cli.command(name="publish")
def _publish(
    loglevel: constants.LogLevel = typer.Option(
        config.loglevel, help="The log level to use."
    ),
):
    """Publish a custom component.

    Args:
        loglevel: The log level to use.
    """
    console.set_log_level(loglevel)


@custom_components_cli.command(name="test")
def _test(
    loglevel: constants.LogLevel = typer.Option(
        config.loglevel, help="The log level to use."
    ),
):
    """Test a custom component.

    Args:
        loglevel: The log level to use.
    """
    console.set_log_level(loglevel)
    console.print(
        "Testing custom component by running the reflex app in dev mode. or do we even need this command?"
    )
