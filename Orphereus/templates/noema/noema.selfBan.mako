# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
%if g.OPT.spiderTrap:
<body>
<div style="display: none"><a href="${h.url_for('botTrap1', confirm=c.userInst.secid())}">...</a></div>
<div style="display: none"><a href="${h.url_for('botTrap2', confirm=c.userInst.secid())}">.</a></div>
</body>
</html>
%endif

