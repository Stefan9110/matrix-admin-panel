# Define cli options
def arg_define(arg_parser):
    arg_parser.add_argument("-u", "--url",
                            type=str, nargs=1, metavar="URL", default=None,
                            help="Your matrix homeserver URL")