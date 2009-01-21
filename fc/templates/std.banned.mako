# -*- coding: utf-8 -*-
<%inherit file="std.main.mako" />

<div class="errorMessage">
<table width="100%">
<tr>
<td width="425">
<object width="425" height="344">
<param name="movie" value="http://www.youtube.com/v/dZBU6WzBrX8&hl=ru&fs=1"></param>
<param name="allowFullScreen" value="false"></param>
<embed src="http://www.youtube.com/v/dZBU6WzBrX8&hl=ru&fs=1&autoplay=1" type="application/x-shockwave-flash" allowfullscreen="false" width="425" height="344"></embed>
</object>
</td>
<td>
<h1>${_('You are banned!')}</h1>
${_('You are banned for %s days for following reason:<br/>%s') % (c.userInst.bantime(),c.userInst.banreason())}
<br/><br/>
${_('Your UID Number: %d') % (c.userInst.uidNumber())}
<br/>
Your UID:<br/>
<input type="text" value="${_('%s') % (c.userInst.uid())}">
<br/>

<form action="/logout">
<p><input type="submit" value="${_('Logout')}"></p>
</form>

</td>
</table>
</div>


