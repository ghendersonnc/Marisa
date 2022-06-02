import lightbulb


class CustomHelp(lightbulb.BaseHelpCommand):
    async def send_bot_help(self, ctx):
        # Override this method to change the message sent when the help command
        # is run without any arguments.
        res = f"```ini\n"
        res += f"This is the help response.\n\n"
        res += f"[COMMANDS]\n"
        for command in self.bot.slash_commands:
            if lightbulb.checks.owner_only in self.bot.slash_commands[command].checks:
                continue
            res += f"{command}\n"

        res += f"\nType /help <command> to get usage info for a command"
        res += f"\nCheck out the source code at https://github.com/ghendersonnc/Marisa"
        res += f"```"
        await ctx.respond(res)

    async def send_plugin_help(self, ctx, plugin):
        # Override this method to change the message sent when the help command
        # argument is the name of a plugin.
        ...

    async def send_command_help(self, ctx, command):
        if not command:
            await ctx.respond("Command does not exist. Type `/help` for a list of usable commands.")
            return

        response = f"```ini\n"
        response += f"this is the help response for the {command.name} command\n\n"
        response += f"Description: {command.description}\n\n"
        response += f"[OPTIONS]\n"
        for option in command.options:
            if command.options[option].required:
                response += f"{option} (Required): {command.options[option].description}\n"
                continue
            response += f"{option}: {command.options[option].description}\n"
        response += "\nType /help for a list of usable commands"
        response += "```"
        await ctx.respond(response)

    async def send_group_help(self, ctx, group):
        # Override this method to change the message sent when the help command
        # argument is the name or alias of a command group.
        ...

    async def object_not_found(self, ctx, obj):
        # Override this method to change the message sent when help is
        # requested for an object that does not exist
        ...
