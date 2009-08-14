<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">
<html>
<head>
        <title>
${c.title}
%if c.boardName:
    &mdash; ${c.boardName}
    %if c.page and isinstance(c.page, int):
      (${c.page})
    %endif
%endif
        </title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
        <meta name="robots" content="noarchive">
        <link rel="shortcut icon" type="image/x-icon" href="${g.OPT.staticPathWeb+g.OPT.favicon}">
        <link rel="icon" type="image/x-icon" href="${g.OPT.staticPathWeb+g.OPT.favicon}">
        <link rel="stylesheet" type="text/css" href="${h.staticFile(c.userInst.style + ".css")}" title="${c.userInst.style}">
</head>
<frameset cols="200,*">
        <frame src="${h.url_for('frameMenu')}" name="list" noresize="noresize" scrolling="auto" frameborder="1">
        <frame src="${c.frameTarget}" name="board" noresize="noresize">
</frameset>
</html>
