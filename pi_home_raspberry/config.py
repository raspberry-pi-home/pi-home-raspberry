import json
import logging
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

BASE_PATH = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(BASE_PATH, '../config.json')

flatten = lambda l: [item for sublist in l for item in sublist]

# required props
PIN_SETTINGS_REQUIRED_PROPERTIES = ('label', 'pin', 'type')
PIN_DEPENDENCIES_REQUIRED_PROPERTIES = ('input_pin', 'output_pin', 'type')

# available pins
GPIO2 = 2
GPIO3 = 3
GPIO4 = 4
GPIO5 = 5
GPIO6 = 6
GPIO7 = 7
GPIO8 = 8
GPIO9 = 9
GPIO10 = 10
GPIO11 = 11
GPIO12 = 12
GPIO13 = 13
GPIO14 = 14
GPIO15 = 15
GPIO16 = 16
GPIO17 = 17
GPIO18 = 18
GPIO19 = 19
GPIO20 = 20
GPIO21 = 21
GPIO22 = 22
GPIO23 = 23
GPIO24 = 24
GPIO25 = 25
GPIO26 = 26
GPIO27 = 27

# available pin types
PIN_TYPE_INPUT_DIGITAL = 'digital_input'
PIN_TYPE_OUTPUT_DIGITAL = 'digital_output'

# available pin dependency types
PIN_DEPENDENCY_TYPE_TOGGLE = 'toggle'
PIN_DEPENDENCY_TYPE_DIRECT = 'direct'

# available input pin types
AVAILABLE_PIN_TYPE_INPUT = tuple(
    v for k, v in locals().items() if k.startswith('PIN_TYPE_INPUT_'),
)

# available output pin types
AVAILABLE_PIN_TYPE_OUTPUT = tuple(
    v for k, v in locals().items() if k.startswith('PIN_TYPE_OUTPUT_'),
)

# available dependency types
AVAILABLE_PIN_DEPENDENCY_TYPE = tuple(
    v for k, v in locals().items() if k.startswith('PIN_DEPENDENCY_TYPE_'),
)

# available pins
AVAILABLE_PINS = tuple(
    v for k, v in locals().items() if k.startswith('GPIO'),
)

# available pin types
AVAILABLE_PIN_TYPES = flatten(tuple(
    v for k, v in locals().items() if k.startswith('AVAILABLE_PIN_TYPE_'),
))


def _verify_pin_settings(pin_settings):
    if not pin_settings:
        logger.error('No pin_settings provided')
        return

    # check pin's range
    # check pin's types
    for pin_setting in pin_settings:
        for prop in PIN_SETTINGS_REQUIRED_PROPERTIES:
            if prop not in pin_setting:
                logger.error('Missing \'%s\' property for pin_settings configuration: %s', prop, pin_setting)
                return
        if pin_setting['pin'] not in AVAILABLE_PINS:
            logger.error('Pin \'%s\' out of range for pin_settings configuration: %s', pin_setting['pin'], pin_setting)
            return
        if pin_setting['type'] not in AVAILABLE_PIN_TYPES:
            logger.error('Invalid pin type \'%s\' for pin_settings configuration: %s', pin_setting['type'], pin_setting)
            return

    # check duplicated pins
    pins = {pin_setting['pin'] for pin_setting in pin_settings}
    if len(pin_settings) != len(pins):
        logger.error('Review your \'pin_settings\' configuration, seems there are duplicated pins')
        return

    # check duplicated labels
    labels = {pin_setting['label'] for pin_setting in pin_settings}
    if len(pin_settings) != len(labels):
        logger.error('Review your \'pin_settings\' configuration, seems there are duplicated labels')
        return

    # return True if everythig went ok
    return True


def _verify_pin_dependencies(pin_dependencies, pin_settings):

    # check pin's range
    # check pin's types
    for pin_dependency in pin_dependencies:
        for prop in PIN_DEPENDENCIES_REQUIRED_PROPERTIES:
            if prop not in pin_dependency:
                logger.error('Missing \'%s\' property for pin_dependencies configuration: %s', prop, pin_dependency)
                return
        if pin_dependency['input_pin'] == pin_dependency['output_pin']:
            logger.error('Invalid configuration for pin_dependencies: %s, \'input_pin\' and \'output_pin\' can not contain the same value', pin_dependency)
            return
        if pin_dependency['input_pin'] not in AVAILABLE_PINS:
            logger.error('Pin \'%s\' out of range for pin_dependencies configuration: %s', pin_dependency['input_pin'], pin_dependency)
            return
        if pin_dependency['output_pin'] not in AVAILABLE_PINS:
            logger.error('Pin \'%s\' out of range for pin_dependencies configuration: %s', pin_dependency['output_pin'], pin_dependency)
            return
        if pin_dependency['type'] not in AVAILABLE_PIN_DEPENDENCY_TYPE:
            logger.error('Invalid dependency type \'%s\' for pin_dependencies configuration: %s', pin_dependency['type'], pin_dependency)
            return
        if pin_settings[pin_dependency['input_pin']]['type'] not in AVAILABLE_PIN_TYPE_INPUT:
            logger.error('Input pin \'%s\' is not configured as an input for pin_dependencies configuration: %s', pin_dependency['input_pin'], pin_dependency)
            return
        if pin_settings[pin_dependency['output_pin']]['type'] not in AVAILABLE_PIN_TYPE_OUTPUT:
            logger.error('Output pin \'%s\' is not configured as an output for pin_dependencies configuration: %s', pin_dependency['output_pin'], pin_dependency)
            return

    # return True if everythig went ok
    return True


def get_config():
    try:
        # read config file
        with open(CONFIG_FILE, encoding='utf-8-sig') as json_file:
            try:
                config = json.load(json_file)
            except json.decoder.JSONDecodeError:
                logger.error('Unable to parse \'config.json\' file')
                return
    except Exception:
        logger.error('Error reading \'config.json\' file')
        return

    # verify pin_settings
    pin_settings = config.get('pin_settings')
    if not _verify_pin_settings(pin_settings):
        return

    # build pin_settings from AVAILABLE_PINS
    all_pin_settings = {pin_setting: {'pin': pin_setting} for pin_setting in AVAILABLE_PINS}

    # replace with configured pins
    for pin_setting in pin_settings:
        all_pin_settings[pin_setting['pin']] = pin_setting

    # verify pin_dependencies
    pin_dependencies = config.get('pin_dependencies', [])
    if not _verify_pin_dependencies(pin_dependencies, all_pin_settings):
        return

    # build result object
    result = {}
    result['pin_settings'] = all_pin_settings
    result['pin_dependencies'] = pin_dependencies

    return result
