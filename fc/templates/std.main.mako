# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <title>${c.boardName}</title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
        <meta name="robots" content="noarchive" />
        <link rel="stylesheet" type="text/css" href="${h.staticFile("std_gray.css")}" title="Anoma std::" />
        <link rel="shortcut icon" type="image/x-icon" href="/favicon.ico" />
    </head>
    <body>
        <%include file="std.logo.mako" />
        <div style="clear: both;">
        ${self.body()}
        </div>
        <%include file="std.footer.mako" />
    </body>
</html>
