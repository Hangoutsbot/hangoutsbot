import plugins
import shlex

from commands import command

def _initialise(bot):
    if '!!' in bot._handlers.bot_command:
        print("ERROR: Bot is already using !! as a botalias, please disable that before using the lastcommand plugin")
        return []

    plugins.register_handler(_handle_command, "message")
    plugins.register_admin_command(["lastcommand"])

    # use bash-type command !! for recalling last command
    command.register(c, admin=False, final=True, name='!!')
    return []

def _handle_command(bot, event, command):
    # Parse message
    try:
        line_args = shlex.split(event.text, posix=False)
    except Exception as e:
        return

    if line_args[0].lower() in bot._handlers.bot_command and line_args[1].lower() != '!!':
        bot.user_memory_set(event.user.id_.chat_id, 'lastcommand', ' '.join(line_args[1:]))

    if line_args[0].lower() == '!!':
        yield from command.run(bot, event, *(['!!'] + line_args[1:]))

def c(bot, event):
    if bot.memory.exists(["user_data", event.user.id_.chat_id, 'lastcommand']):
        lastcommand = bot.user_memory_get(event.user.id_.chat_id, 'lastcommand')
        yield from bot.coro_send_message(event.conv, '<b>Last command :<br>' + lastcommand , context={ "parser": True })
        if not lastcommand is '!!':
            yield from command.run(bot, event, *lastcommand.split())
    else:
        yield from bot.coro_send_message(event.conv, 'You have no previous command.'  , context={ "parser": True })

def lastcommand(bot, event, *args):
	if not args:
		yield from bot.coro_send_message(event.conv_id, "Please provide a userid!")
		return

	userid = args[0]
	#try:
    try:
    	yield from bot.coro_send_message(event.conv,
            '<b>Last command for ' +
            userid +
            ' :<br>' +
            bot.user_memory_get(userid, 'lastcommand'),
            context={"parser": True})
	except TypeError as e:
        yield from bot.coro_send_message(event.conv, '<b>No last command.<br>', context={ "parser": True })
