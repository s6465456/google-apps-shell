# gas_documentation_builder.py
#
# This script builds documentation for GAS. You can then manually upload the documentation to the Google Code Project.
#
# Usage:
#   python gas_docs_builder.py > documentation.txt
# 
# Author:
#   jeffpickhardt@google.com
#

import gas_commands

print "#summary Documentation for GAS version %s\n" % gas_commands.__version__
print '= Documentation ='
print "This page contains a full listing of GAS commands.\n"
command_tuples = [(gas_commands.commands[key]['category'], key) for key in gas_commands.commands.keys()]
command_tuples.sort()
current_category = ''
for command_tuple in command_tuples:
    command = command_tuple[1]
    if str(command)[0] == '_':
        continue # we will skip any example that starts with an underscore, such as _template
    if current_category != gas_commands.commands[command]['category']:
        # we are changing categories
        print "----\n\n"
        print "= %s =\n" % gas_commands.commands[command]['category']
        current_category = gas_commands.commands[command]['category']
    print "== %s `(%s)` ==" % (gas_commands.commands[command]['title'], command)
    print gas_commands.commands[command]['description']
    print "*Usage:*\n"
    print "{{{\n%s\n}}}\n" % gas_commands.commands[command]['usage']
    print "*Example:*\n"
    for example in gas_commands.commands[command]['examples']:
        (syntax, explanation) = example
        print "%s\n" % explanation
        print "{{{\n%s\n}}}\n" % syntax
