def filterText(text):
    return text.replace('<','&lt;').replace('>','&gt;').replace("'",'&#39;').replace('"','&quot;').replace('(c)','&copy;').replace('---','&#151;').replace('--','&#8722;').replace('(tm)','&#153;').replace('...','&#8230;')
