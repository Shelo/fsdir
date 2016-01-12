import fsdir

# SFSCL: Structured File System Config Language

director = fsdir.fsdirector.FSDirector()

director.load_directive(fsdir.directives.Edit)
director.load_directive(fsdir.directives.Create)
director.load_directive(fsdir.directives.Read)
director.load_directive(fsdir.directives.Remove)

director.load_procedure(fsdir.procedures.Append)
director.load_procedure(fsdir.procedures.CopyTo)
director.load_procedure(fsdir.procedures.SetTo)

director.load("example/dev.fsdir")
cached = director.cache

try:
    director.validate()
    director.run()
except ValueError as e:
    print e.message
