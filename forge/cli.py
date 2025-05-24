import sys
import re

from typing import Dict, Any
from forge import utils
from forge import path


HEX_REGEX = "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"


def configure():
    utils.prln("🔧 Configure your Vite project")
    config = ConfigFactory()
    args: Dict = config.get()
    config.set(args)


def main():
    if len(sys.argv) < 2:
        print("Usage: forge <command>")
        return

    command = sys.argv[1]
    if command == "configure":
        configure()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()


class ConfigFactory:
    def __init__(self) -> None:
        self.font: str = ""
        self.primary: str = ""
        self.secondary: str = ""

    def get(self):
        args = {}

        use_google_fonts, font = self.configure_font()
        colours: Dict = self.configure_colours()

        args["font"] = font
        args["use_google_fonts"] = use_google_fonts
        args["colours"] = colours

        return args

    def set(self, args):
        self.write_font(args["use_google_fonts"], args["font"])
        self.write_colours(args["colours"])

    # <================ Get Methods ================>

    def configure_font(self, font_choice: str = "") -> tuple[bool, str]:
        if not font_choice:
            font_choice = input("\n🖊️  Use Google fonts? (y/N): ")
        font = input("\n-> Font name: ")

        if utils.cli_string_to_bool(font_choice):
            use_google_fonts: bool = True
        else:
            use_google_fonts: bool = False

        if not font:
            utils.prln("Please enter a font.")
            self.configure_font(font_choice)

        return use_google_fonts, font

    def configure_colours(self) -> Dict:
        colours = {}
        primary = "#" + input("\nPrimary colour (hex): #")
        secondary = "#" + input("\nSecondary colour (hex): #")

        if not re.fullmatch(HEX_REGEX, primary) or re.fullmatch(HEX_REGEX, secondary):
            utils.prln("Please enter valid hexademical colours.")
            self.configure_colours()

        colours["primary"] = utils.generate_shades(primary)
        colours["secondary"] = utils.generate_shades(secondary)

        return colours

    def configure_env(self):
        env: dict[str, Any] = {}
        api_integrations: Dict[str, str] = {}  # {"API_KEY": "abc123"}

        # Get/set domain
        domain: str = "https://" + input("\nDomain: https://").replace("www.", "")
        if not domain:
            domain = "https://example.com"

        use_subdomain_api_base = input(
            f"\nUse https://api.{domain[8:]} as API base URL? (Y/n): "
        )
        if use_subdomain_api_base:
            api_base_url = f"https://api.{domain[8:]}"
        else:
            api_base_url = f"{domain}/api"

        def prompt_api_keys():
            while True:
                env_var_name = input("\nEnvironment variable name: ")
                env_var_value = '"' + input(f"Value for '{env_var_name}': ") + '"'

                api_integrations[env_var_name] = env_var_value
                utils.prln(f"✅ API key '{env_var_name}' added")

                add_another = input("Add another API key? (y/N): ")
                if not utils.cli_string_to_bool(add_another):
                    break

        add_api = input("\nAdd API integration? (y/N): ")
        if utils.cli_string_to_bool(add_api):
            prompt_api_keys()

        env["domain"] = domain
        env["api_base_url"] = api_base_url
        env["api_integrations"] = api_integrations

        return env

    # <================ Set Methods ================>

    def write_font(self, use_google_fonts: bool, font: str):
        if use_google_fonts:
            utils.write_config(
                file_path=path.TW_CONFIG_PATH,
                example="<font>",
                new_setting=font.replace(" ", "+").capitalize(),
            )
        else:
            utils.write_config(
                file_path=path.TW_CONFIG_PATH,
                example="<font>",
                new_setting=font.replace(" ", "-").lower(),
            )

        utils.write_config(
            file_path=path.INDEX_CSS_PATH, example="<font>", new_setting=font
        )

    def write_colours(self, colours: Dict):
        utils.write_config(
            file_path=path.TW_CONFIG_PATH,
            example="<colors>",
            new_setting=utils.to_tailwind_js(colours),
        )
