import os
import os.path
import ConfigParser


class AppConfig():

    _Verbose = False

    def __init__(self, default_filename = 'default.cfg', local_filename = 'local.cfg'):
        self.filename = default_filename
        self.local_filename = local_filename
        self.local_overides = False

        self.read()
        if self.config.has_option('general', 'show_config') and self.config.getboolean('general', 'show_config'):
            self.print_()

    def read(self):
        '''
        Read the config file for the app. This should keep all the program options in data so we can
        easily debug without changing code.
        '''
        default_name = self.filename 
        local_override = self.local_filename

        default_file = os.path.abspath(os.path.join(os.path.dirname(__file__), default_name))

        if not os.path.isfile(default_file):
            raise IOError('[{}] configuration file not found.'.format(default_file))

        config = ConfigParser.ConfigParser()
        config.readfp(open(default_file))

        if config.has_section('general'):
            if config.has_option('general', 'local_conf'):
                local_override = config.get('general', 'local_conf')

        local_file = os.path.abspath(os.path.join(os.path.dirname(__file__), local_override))

        # Local configuration - do not check in to .git
        if os.path.isfile(local_file):
            local_config = ConfigParser.ConfigParser()
            local_config.readfp(open(local_file))

            self.local_overides = True

            sections = local_config.sections()

            for section in sections:
                options = local_config.options(section)

                for option in options:
                    value = local_config.get(section, option)
                    config.set(section, option, value)
                    if self.__class__._Verbose:
                        print "{}:{} -> {}".format(section, option, value)

        self.config = config

    def print_(self):
        '''
        Print out the sections, options and values from a configparser object.
        '''

        print "*" * 80
        if  self.local_overides:
            print "* {} and {}".format(self.filename, self.local_filename)
        else:
            print "* {}".format(self.filename)
        print "*" * 80

        sections = self.config.sections()
        for section in sections:
            options = self.config.options(section)
            print "[{}]".format(section)

            for option in options:
                value = self.config.get(section, option)
                print "\t> {}:{}".format(option, value)

        print "*" * 80

    def get(self, section, option, default = None):
        if self.config.has_option(section, option):
            return self.config.get(section, option)
        return default
