# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>

<title> \
${c.title} \
%if c.boardName:
&mdash; ${c.boardName} \
%if c.page and isinstance(c.page, int):
  (${c.page}) \
%endif
%endif
</title>

<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
<meta name="robots" content="noarchive" />
<link rel="shortcut icon" type="image/x-icon" href="/favicon.ico" />
<link rel="icon" type="image/x-icon" href="/favicon.ico" />
<link rel="stylesheet" type="text/css" href="${h.staticFile(c.userInst.style + ".css")}" title="${c.userInst.style}" />

%for jsFile in c.jsFiles:
<script type="text/javascript" src="${h.staticFile(jsFile)}"></script>
%endfor

${h.headCallback(c)}

<%include file="wakaba.redirector.mako" />
</head>

<body>
<%include file="wakaba.jsTest.mako" />

%if not c.disableMenu:
	%if g.OPT.useZMenu:
		<%include file="wakaba.z-menu.mako" />
	%else:
		<%include file="wakaba.menu.mako" />
	%endif
%endif

%if not c.disableLogo:
<%include file="wakaba.logo.mako" />
%endif

%if not (c.disableLogo and c.disableMenu):
<hr />
%endif

${self.body()}

%if not c.disableMenu:
<%include file="wakaba.menu.mako" />
%endif

%if not c.disableFooter:
<%include file="wakaba.footer.mako" />
%endif
</body>
</html>
