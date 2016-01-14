import fsdir

# SFSCL: Structured File System Config Language

director = fsdir.fsdirector.FSDirector()

director.load_directive(fsdir.directives.Edit)
director.load_directive(fsdir.directives.Create)
director.load_directive(fsdir.directives.Read)
director.load_directive(fsdir.directives.Remove)
director.load_directive(fsdir.directives.File)

director.load_procedure(fsdir.procedures.Append)
director.load_procedure(fsdir.procedures.CopyTo)
director.load_procedure(fsdir.procedures.SetTo)
director.load_procedure(fsdir.procedures.ChMod)

# load the fsdir script.
director.load("dev.fsdir")

try:
    # validate the script.
    director.validate()

    # sandbox run it.
    director.sandbox_run()

    # apply the sandbox.
    # director.apply()
except ValueError as e:
    print e.message
