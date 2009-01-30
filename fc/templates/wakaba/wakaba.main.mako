# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <title>
${c.title}
%if c.boardName:
    &#151; ${c.boardName}
    %if c.page and isinstance(c.page, int):
      (${c.page})
    %endif
%endif        
        </title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
        <meta name="robots" content="noarchive" />
        <link rel="stylesheet" type="text/css" href="${g.OPT.staticPathWeb}css/${c.userInst.style()}.css" title="Photon" />
        <link rel="shortcut icon" type="image/x-icon" href="/favicon.ico" />
		<script type="text/javascript" src="${g.OPT.staticPathWeb}js/ui.js"></script>
		<script type="text/javascript" src="${g.OPT.staticPathWeb}js/utils.js"></script>
		<script type="text/javascript" src="${g.OPT.staticPathWeb}js/jquery-1.2.6.js"></script>
    </head>
    <body>
        <%include file="wakaba.menu.mako" />
        <%include file="wakaba.logo.mako" />
        <hr />     
        ${self.body()}
        <%include file="wakaba.menu.mako" />
        <%include file="wakaba.footer.mako" />
    </body>
</html>
