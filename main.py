import fsdir

director = fsdir.FSDirector.FSDirector()

director.load_directive(fsdir.directives.Edit)
director.load_directive(fsdir.directives.Touch)
director.load_directive(fsdir.directives.Read)
director.load_directive(fsdir.directives.Remove)

director.load_procedure(fsdir.procedures.Append)
director.load_procedure(fsdir.procedures.CopyTo)
director.load_procedure(fsdir.procedures.SetTo)

director.load("example/dev.fsdir")
cached = director.cached

for directive in cached:
    print directive[0].keyword()
    print "  " + str(directive[2].tokens)

    if directive[1]:
        print "  " + directive[1].keyword()
        print "  " + str(directive[2].sub_extract.tokens)

    print
