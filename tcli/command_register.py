"""Register core TCLI command handlers."""

from absl import flags
from tcli import command_parser

# Values for flags that are an enum.
COLOR_SCHEMES = ['light', 'dark', 'gross']
DISPLAY_FORMATS = ['raw', 'csv', 'tbl', 'nvp']
MODE_FORMATS = ['cli', 'gated', 'http', 'shell']

# Flag help string indentation.
I = '\n' + ' '*4

# Commands that can be populated at invocation, as well as during execution.
FLAGS = flags.FLAGS
flags.DEFINE_boolean(
  'color', True,
  f'{I}Toggle using color when displaying results.')

flags.DEFINE_enum(
  'color_scheme', 'light', COLOR_SCHEMES,
  f"{I}Use 'light' scheme on dark background or 'dark' otherwise.")

flags.DEFINE_enum(
  'display', 'raw', DISPLAY_FORMATS,
  f'{I}Extensible set of routines used for formatting command output.'
  f'{I}Available display formats are: {DISPLAY_FORMATS}'
  f"{I}Shortname: 'D'.", short_name='D')

flags.DEFINE_enum(
  'filter', 'default_index', ['default_index', ''],
  f'{I}File name that maps templates for extracting data from output.'
  f"{I}Is disabled if display is in 'raw' mode."
  f"{I}Shortname: 'F'.", short_name='F')

flags.DEFINE_boolean(
  'linewrap', False,
  f'{I}Override default line wrap behavior.')

flags.DEFINE_enum(
  'mode', 'cli', MODE_FORMATS, 
  f'{I}Extensible set of routines used for formatting command output.'
  f'{I}Available display formats are: {DISPLAY_FORMATS}'
  f"{I}Shortname: 'D'.",
  short_name='M')

flags.DEFINE_integer(
  'timeout', 45,
  f'{I}Period (in seconds) to wait for outstanding command responses.',
  short_name='O')

flags.DEFINE_boolean('sorted', False, 'Sort device entries in output.')

def RegisterCommands(
    command_object, cli_parser:command_parser.CommandParser) -> None:
  """Register TCLI CLI commands.
  
  Attributes:
    command_object: The object that has callable methods for the commands.
    cli_parser: Object that does the registering.
    indent: str, indentation level, after first line of help string.
"""

  cli_parser.RegisterCommand(
    'buffer',
    f'{I}Show contents of buffer.', min_args=1,
    handler=command_object._CmdBuffer)
  
  cli_parser.RegisterCommand(
    'bufferlist',
    f'{I}Show buffers currently in use (written to and not cleared).',
    max_args=0, handler=command_object._CmdBufferList)
  
  cli_parser.RegisterCommand(
    'clear',
    f'{I}Deletes contents of named buffer.', min_args=1,
    handler=command_object._CmdClear)
  
  cli_parser.RegisterCommand(
    'color',
    FLAGS['color'].help, inline=True, toggle=True,
    default_value=FLAGS['color'].value,
    handler=command_object._CmdToggleValue, completer=lambda: ['on', 'off'])
  
  cli_parser.RegisterCommand(
    'color_scheme',
    FLAGS['color_scheme'].help, inline=True,
    default_value=FLAGS['color_scheme'].value,
    handler=command_object._CmdColorScheme, completer=lambda: COLOR_SCHEMES)
  
  cli_parser.RegisterCommand(
    'command', 
    f"{I}Submit command to target device's. Safe mode enforces use of "
    f"{I}'command' for sending input to targets."
    f"{I}Shortname: 'C'.",
    short_name='C', min_args=1, raw_arg=True,
    handler=command_object._CmdCommand)
  
  cli_parser.RegisterCommand(
    'defaults', 
    f'{I}Returns environment to startup/factory defaults.'
    f'{I}Supply argument to set a specific value back to default,'
    f"{I}or 'all' to return everything to the defaults.",
    handler=command_object._CmdDefaults)
  
  cli_parser.RegisterCommand(
    'display',
    FLAGS['display'].help, short_name='D', inline=True,
    default_value=FLAGS['display'].value, handler=command_object._CmdDisplay,
    completer=lambda: DISPLAY_FORMATS)
  
  cli_parser.RegisterCommand(
    'env', 
    f'{I}Display current escape command settings.',
    max_args=0, handler=command_object._CmdEnv)
  
  cli_parser.RegisterCommand(
    'exec', 
    f'{I}Execute command in shell.'
    f"{I}Shortname: '!'.",
    short_name='!', min_args=1, raw_arg=True,
    handler=command_object._CmdExecShell)
  
  cli_parser.RegisterCommand(
    'exit',
    f'{I}Exit tcli.',
    inline=True, max_args=0, handler=command_object._CmdExit)
  
  cli_parser.RegisterCommand(
    'expandtargets',
    f"{I}Displays the expanded list of devices matched by 'targets' and"
    f"{I}not matched by 'xtargets'.",
    max_args=0, handler=command_object._CmdExpandTargets)
  
  cli_parser.RegisterCommand(
    'filter', FLAGS['filter'].help,
    short_name='F', inline=True,
    default_value=FLAGS['filter'].value,
    handler=command_object._CmdFilter)
  
  cli_parser.RegisterCommand(
    'help', f'{I}Display escape command online help.',
    max_args=0, inline=True, handler=command_object._CmdHelp)
  
  cli_parser.RegisterCommand(
    'inventory',
    f'{I}Displays attributes of matched targets.'
    f"{I}Shortname: 'V'.",
    short_name='V',
    max_args=0, handler=command_object._CmdInventory)
  
  cli_parser.RegisterCommand(
    'linewrap', FLAGS['linewrap'].help,
    inline=True, toggle=True,
    default_value=FLAGS['linewrap'].value,
    handler=command_object._CmdToggleValue, completer=lambda: ['on', 'off'])
  
  cli_parser.RegisterCommand(
    'log', 
    f'{I}Record commands and device output to buffer.'
    f'{I}Does not include escape commands or output from these commands.',
    append=True, inline=True,
    handler=command_object._CmdLogging)
  
  cli_parser.RegisterCommand(
    'logall',
    f'{I}Record both commands and escape commands and output to buffer.',
    append=True, inline=True, handler=command_object._CmdLogging)
  
  cli_parser.RegisterCommand(
    'logstop',
    f"{I}Stop recording or logging to named buffer (same as 'recordstop'.",
    inline=True, min_args=1, handler=command_object._CmdLogStop)
  
  cli_parser.RegisterCommand(
    'mode',
    FLAGS['mode'].help, short_name='M', inline=True,
    default_value=FLAGS['mode'].value, 
    handler=command_object._CmdMode)
  
  cli_parser.RegisterCommand(
    'play',
    f'{I}Play out recorded keystrokes from named buffer to target '
    f"device/s.{I}Shortname: 'P'.",
    short_name='P', min_args=1, handler=command_object._CmdPlay)
  
  cli_parser.RegisterCommand(
    'quit',
    f'{I}Exit by another name.',
    inline=True, max_args=0, handler=command_object._CmdExit)
  
  cli_parser.RegisterCommand(
    'read',
    f'{I}Read contents of file and store in buffer.'
    f'{I}File name is specified at a subsequent prompt.',
    append=True, min_args=1, max_args=2, handler=command_object._CmdRead)
  
  cli_parser.RegisterCommand(
    'record',
    f'{I}Record commands to named <buffer>.'
    f'{I}If command is appended with {command_parser.APPEND} then'
    ' append to buffer.',
    append=True, inline=True, handler=command_object._CmdLogging)
  
  cli_parser.RegisterCommand(
    'recordall',
    f'{I}Record commands and escape commands to named <buffer>.'
    f'{I}If command is appended with {command_parser.APPEND} then'
    ' append to buffer.',
    append=True, inline=True, handler=command_object._CmdLogging)
  
  cli_parser.RegisterCommand(
    'recordstop',
    f"{I}Stop recording or logging to named buffer (same as 'logstop').",
    inline=True, min_args=1, handler=command_object._CmdLogStop)
  
  cli_parser.RegisterCommand(
    'safemode',
    f"{I}Do not forward input to 'targets' unless using 'command'."
    f"{I}Shortname: 'S'.",
    short_name='S', inline=True, toggle=True,
    handler=command_object._CmdToggleValue, completer=lambda: ['on', 'off'])
  
  cli_parser.RegisterCommand(
    'timeout', FLAGS['timeout'].help,
    default_value=FLAGS['timeout'].value,
    handler=command_object._CmdTimeout)
  
  cli_parser.RegisterCommand(
    'write',
    f'{I}Dumps contents of buffer to file.'
    f'{I}File name is specified at a subsequent prompt.',
    append=True, min_args=1, max_args=2, handler=command_object._CmdWrite)
  
  cli_parser.RegisterCommand(
    'verbose',
    f'{I}Display extra data columns in output (for csv mode).',
    inline=True, toggle=True, handler=command_object._CmdToggleValue,
    completer=lambda: ['on', 'off'])
  
  cli_parser.RegisterCommand(
    'vi', f'{I}Opens buffer in vi editor.', min_args=1, 
    handler=command_object._CmdEditor)

def SetFlagDefaults(cli_parser:command_parser.CommandParser) -> None:
  """Parses command line flags ad sets default attributes.

    Commands here affect data representation/presentation but are otherwise
    harmless.
  """

  # Called against each flag declared in this module.
  for command_name in ('color', 'color_scheme', 'display', 'filter',
                        'linewrap', 'mode', 'timeout'):
    # Calling the handlers directly will not be logged.
    cli_parser.ExecWithDefault(command_name)
