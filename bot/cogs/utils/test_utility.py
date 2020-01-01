from discord_arg_parser import arg_parser

import asyncio
import sys
loop = asyncio.get_event_loop()


args = ' '.join(sys.argv[1:])
if args == '':
    args = None

argument_dict = {
    "B switch": {
        'default': None,
        'flags': ['-b', '--bitch'],
        'switch': False,
        'required': True
    },
    "J Switch": {
        'default': False,
        'flags': ['-j', '--jay'],
        'switch': True,
        'switch_action': True,
        'required': False
    },
    "G switch": {
        'default': False,
        'flags': ['-g'],
        'required': False
    }
}
try:
    res = loop.run_until_complete(arg_parser(argument_dict, args))
    print(res)
except RuntimeError as e:
    print(e)

'''
                    if arg == dictionary['flags'][0]:
                        index = arg_list.index(dictionary['flags'][0])
                arg_index = arg_list.index()
            # Check any strings match flags list
            if any(i in dictionary['flags'] for i in arg_list):
                if dictionary['flags'][0] in arg_list:
                    index = arg_list.index(dictionary['flags'][0])
                else:
                    index = arg_list.index(dictionary['flags'][1])
                if (index + 1) < len(arg_list):
                    arg = arg_list.pop(index + 1)
                    arg_list.pop(index)
                    parsed_args[flag] = arg
                else:
                    parsed_args[flag] = dictionary['default']
            else:
                parsed_args[flag] = dictionary['default']
'''