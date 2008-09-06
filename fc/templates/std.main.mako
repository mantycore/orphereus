# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <title>${c.boardName}</title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
        <META NAME="ROBOTS" CONTENT="NOARCHIVE">
        <link rel="stylesheet" type="text/css" href="${g.OPT.filesPathWeb}../css/photon.css" title="Photon" />
        <link rel="shortcut icon" type="image/x-icon" href="/favicon.ico" />
		<script type="text/javascript" src="${g.OPT.filesPathWeb}../js/ui.js"></script>
		<script type="text/javascript" src="${g.OPT.filesPathWeb}../js/utils.js"></script>
		<script type="text/javascript" src="${g.OPT.filesPathWeb}../js/jquery-1.2.6.js"></script>
    </head>
    <body>
        <%include file="std.logo.mako" />
        <hr />
        ${self.body()}
        <%include file="std.footer.mako" />
    </body>
</html>
