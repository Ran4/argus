import xmlwikiparser2


def testFixWikiLists(inValues, correctValues):
    ib = xmlwikiparser2.InfoBox("","",[],0, verbose=False)
    for inValue, correctValue in zip(inValues, correctValues):
        retValue = ib.fixWikiLists(inValue, verbose=True)
        print "retInfoBoxStringList:"
        print retValue
        assert(retValue == correctValue)
    
    print "Successfully tested fixWikiLists"
    
if __name__ == "__main__":
    inValues = [
        ["| name = albert}}"],
        ["| citizenships = {{unbulleted list | germany | switzerland}}}}"],
        ["| citizenships = {{unbulleted list | germany | switzerland}}", "}}"],
        ["| citizenships = {{unbulleted list | ger", "many | switzerland}}", "}}"],
        ["{{flowlist |", "* [[cat]]", "* [[dog]]", "* [[horse]]", "* [[cow]]", "* [[sheep]]", "* [[pig]]", "}}", "}}"]
    ]

    outValues = [
        ["| name = albert}}"],
        ["| citizenships = {{unbulleted list | germany | switzerland}}}}"],
        ["| citizenships = {{unbulleted list | germany | switzerland}}", "}}"],
        ["| citizenships = {{unbulleted list | germany | switzerland}}", "}}"],
        ["{{flowlist |* [[cat]]* [[dog]]* [[horse]]* [[cow]]* [[sheep]]* [[pig]]}}", "}}"]
    ]
    
    testFixWikiLists(inValues, outValues)
