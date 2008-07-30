# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />
${_('Available actions:')}
<table width="100%" class="hlTable">

<tr>
<td>
<form method="post" action="service/clearOekaki/">
${_('Destroy orphaned oekaki (except last 30)')}
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="service/destroyInvites/">
${_('Destroy <b>ALL</b> unused invites')}
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="service/integrityChecks/">
<span style="color: red;">${_('Integrity checks')}</span>
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

</table>
