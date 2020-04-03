class Plugin:
    def __init__(self, plugin_name, **kwargs):
        """
        Constructs a new plugin with the specified name, validation function,
        and arguments.
        """
        self.name = plugin_name
        self.args = {}
        for key, value in kwargs.items():
            self.args[key] = value
            
    def cmdline(self):
        """
        Renders the plugin's command-line option as to be passed to PANDA.
        """

        arg_str = self.name
        if self.args:
            arg_str += ':'
            args = []
            for key in self.args:
                value = self.args[key]
                args.append('%s=%s' % (key, value))
            arg_str += ",".join(args)

        cmdline = ["-panda", arg_str]
        return cmdline

# These are just some tests I was running.
if __name__ == "__main__":
    plugin = Plugin("stringsearch", str="hello world")
    print(plugin.cmdline())
    plugin = Plugin("stringsearch", name="test")
    print(plugin.cmdline())
    plugin = Plugin("asidstory")
    print(plugin.cmdline())
