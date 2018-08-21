import re
import robot.parsing.populators as pop
import robot.parsing.model as mod


def convert(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def stringize(arg):
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    if "=" in arg:
        arg_split = arg.split("=")
        arg_name, arg_val = [item.rstrip().lstrip() for item in arg_split]
        pre_template = '{}='.format(arg_name)
        arg = arg_val
    else:
        pre_template = ''

    if not is_number(arg):
        template = '"{}"'
    else:
        template = '{}'

    return pre_template+template.format(arg)


file = mod.TestCaseFile()
filepop = pop.FromFilePopulator(file)
filepop.populate("Acceleration.robot", resource=True)


# IMPORTS
# Import modules to each resource file own namespace
# Then each function that imports a resource file inherits the whole namespace


for _import in file.imports.data:
    print(_import.type)
    print(_import.name)


# TEST CASES


for test in file.testcase_table.tests:
    for step in test.steps:
        func = convert(step.name)
        args = map(stringize, step.args)
        args = ", ".join(args)
        src = "{}({})".format(func, args)
        print(src)