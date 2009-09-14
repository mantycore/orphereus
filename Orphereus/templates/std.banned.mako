# -*- coding: utf-8 -*-
<%inherit file="std.main.mako" />

<div class="errorMessage">
<h1>${_('You are banned!')}</h1>
</div>
<br /><div align="center">
<table width="90%">
<tr>
<td width="425">
<object type="application/x-shockwave-flash"
        data="http://www.youtube.com/v/dZBU6WzBrX8&hl=ru&fs=1&autoplay=1"
        width="425" height="344">
  <param name="movie" value="http://www.youtube.com/v/dZBU6WzBrX8&hl=ru&fs=1&autoplay=1"></param>
  <param name="allowFullScreen" value="false"></param>
</object>
</td>
<td>
<div align="center">
${_('You are banned for %s days for the following reason:<br/><b>%s</b>') % (c.userInst.bantime(),c.userInst.banreason())}
<br /><br />${_('This ban expires on %s' %(c.userInst.banexpire()))}
<br/><br/>
${_('Your UID Number: %d') % (c.userInst.uidNumber)}
<br/>
<input type="text" value="${c.userInst.uid}" readonly="readonly" />
<br/><br/>
<form action="${h.url_for('logout')}">
<p><input type="submit" value="${_('Logout')}" /></p>
</form>
</div>

</td>
</table>
</div>
