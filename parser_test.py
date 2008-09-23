from wakabaparse import WakabaParser
import os
import sys
import time
testlist = ['test_sanity','test_symbols','test_links','test_all_inline','test_all_inline_complex','test_marksymbols','blocks'
       ,'test_spoiler_inline','test_spoiler_block','test_spoiler_mixed','all','test_links_complex']

t1 = time.time()
parser = WakabaParser()
print "Parser loaded in %s seconds" % (time.time() - t1)

if len(sys.argv) > 1:
	mode = sys.argv[1]
else:
	mode = 'testall'

if mode == 'test':
	if len(sys.argv) > 2:
		test = sys.argv[2]
		testtxt = open('wakabaparse/' + test).read()
		print "Trying test %s" % test
		print testtxt
		t1 = time.time()
		taglist = parser.getTagList(testtxt)
		print "Done test %s in %s seconds" % (test,(time.time() - t1))
		print taglist
		parser.PrintTree(taglist[1], 0)
elif mode == 'testall':
	for test in testlist:
	    testtxt = open('wakabaparse/' + test).read()
	    testres = open('wakabaparse/%s.res' % test).read()
	    t1 = time.time()
	    taglist = parser.getTagList(testtxt)
	    if str(taglist) == testres:
	    	print "Passed test %s in %s seconds" % (test,(time.time() - t1))
	    else:
	    	print "Test %s failed!" % test
	    	print taglist
	    	parser.PrintTree(taglist[1], 0)
elif mode == 'build':
	for test in testlist:
	    testtxt = open('wakabaparse/' + test).read()
	    t1 = time.time()
	    taglist = parser.getTagList(testtxt)
	    print "Passed test %s in %s seconds" % (test,(time.time() - t1))
	    print taglist
	    parser.PrintTree(taglist[1], 0)
	    isok = raw_input('Is it correct? (y/n) : ')
	    if isok == 'y':
	    	testres = open('wakabaparse/%s.res' % test,'w')
	    	testres.write(str(taglist))
	    	testres.close()
	    	print "Saved."
elif mode == 'buildnew':
        for test in testlist:
            if not os.path.isfile('wakabaparse/%s.res' % test):
                testtxt = open('wakabaparse/' + test).read()
                t1 = time.time()
                taglist = parser.getTagList(testtxt)
                print "Passed test %s in %s seconds" % (test,(time.time() - t1))
                print taglist
                parser.PrintTree(taglist[1], 0)
                isok = raw_input('Is it correct? (y/n) : ')
                if isok == 'y':
                    testres = open('wakabaparse/%s.res' % test,'w')
                    testres.write(str(taglist))
                    testres.close()
                    print "Saved."
                    
