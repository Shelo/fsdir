import fsdir
import sys

# SFSCL: Structured File System Config Language

director = fsdir.fsdirector.FSDirector()

# load plugins.
director.load_directive(fsdir.directives.Edit)
director.load_directive(fsdir.directives.Create)
director.load_directive(fsdir.directives.Read)
director.load_directive(fsdir.directives.Remove)
director.load_directive(fsdir.directives.File)

director.load_procedure(fsdir.procedures.Append)
director.load_procedure(fsdir.procedures.CopyTo)
director.load_procedure(fsdir.procedures.Replace)
director.load_procedure(fsdir.procedures.Set)
director.load_procedure(fsdir.procedures.ChMod)

# EXAMPLE AS TERMINAL COMMAND:
# load the fsdir script from argv.
# this will automatically run the validation and sandbox.
director.load_argv()

# load the script form file.
# director.load("dev.fsdir")

# load the script form string.
# director.load("FILE 'target/ch_file.md' 'target/dummy_file.md' CHMOD (777)")

try:
    pass
    # validate the script.
    # director.validate()

    # sandbox run it.
    # director.sandbox_run()

    # apply the sandbox.
    # director.apply()
except ValueError as e:
    print e.message
