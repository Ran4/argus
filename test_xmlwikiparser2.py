import xmlwikiparser2


def testFixWikiLists(inValues, correctValues):
    inValues = [
        ["| name = albert}}"],
        ["| citizenships = {{unbulleted list | germany | switzerland}}}}"],
        ["| citizenships = {{unbulleted list | germany | switzerland}}", "}}"],
        ["| citizenships = {{unbulleted list | ger", "many | switzerland}}", "}}"],
        ["{{flowlist |", "* [[cat]]", "* [[dog]]", "* [[horse]]", "* [[cow]]", "* [[sheep]]", "* [[pig]]", "}}", "}}"],
        ["{{flowlist}}", "* [[cat]]", "* [[dog]]", "* [[horse]]", "* [[cow]]", "* [[sheep]]", "* [[pig]]", "{{endflowlist}}", "}}"],
    ]

    outValues = [
        ["| name = albert}}"],
        ["| citizenships = {{unbulleted list | germany | switzerland}}}}"],
        ["| citizenships = {{unbulleted list | germany | switzerland}}", "}}"],
        ["| citizenships = {{unbulleted list | germany | switzerland}}", "}}"],
        ["{{flowlist |* [[cat]]* [[dog]]* [[horse]]* [[cow]]* [[sheep]]* [[pig]]}}", "}}"],
        ["{{flowlist}}* [[cat]]* [[dog]]* [[horse]]* [[cow]]* [[sheep]]* [[pig]]{{endflowlist}}", "}}"],
    
    ib = xmlwikiparser2.InfoBox("","",[],0, verbose=False)
    for inValue, correctValue in zip(inValues, correctValues):
        retValue = ib.fixWikiLists(inValue, verbose=True)
        print inValue
        print "->"
        print retValue
        print
        assert(retValue == correctValue)
    
    print "Successfully tested fixWikiLists"
    
if __name__ == "__main__":
    ]
    
    testFixWikiLists(inValues, outValues)
