# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
	<head>
		<title>${c.Strings.ChanTitle} - ${c.Strings.BoardTitle}</title>
		<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
		<link rel="stylesheet" type="text/css" href="/css/photon.css" title="Photon" />
	</head>
	<body>
		<%include file="wakaba.menu.mako">
		<%include file="wakaba.logo.mako">
		<hr />
		${self.body()}
		<%include file="wakaba.menu.mako">
		<%include file="wakaba.footer.mako">
	</body>
</html>
