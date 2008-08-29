# -*- coding: utf-8 -*-
<%inherit file="std.main.mako" />

<div class="errorMessage">
<h1>${_('You are banned!')}</h1>
${_('You are banned for %s days for following reason : %s') % (c.userInst.bantime(),c.userInst.banreason())}
<br/><br/>
<object width="425" height="344"><param name="movie" value="http://www.youtube.com/v/dZBU6WzBrX8&hl=ru&fs=1"></param><param name="allowFullScreen" value="true"></param><embed src="http://www.youtube.com/v/dZBU6WzBrX8&hl=ru&fs=1" type="application/x-shockwave-flash" allowfullscreen="true" width="425" height="344"></embed></object>
</div>

