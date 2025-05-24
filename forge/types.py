from typing import TypedDict


ApiIntegrations = dict[str, str]


class Env(TypedDict, total=False):
    domain: str
    api_base_url: str
    api_integrations: "ApiIntegrations"


class Font(TypedDict):
    font: str
    use_google_fonts: bool


class ColourVariations(TypedDict):
    DEFAULT: str
    light: str
    dark: str


class Colours(TypedDict, total=False):
    primary: ColourVariations
    secondary: ColourVariations


class ConfigArgs(TypedDict):
    font: str
    use_google_fonts: bool
    colours: Colours
    env: Env


class ForgeConfigs(TypedDict):
    fonts: Font
    colours: Colours
    env: Env
