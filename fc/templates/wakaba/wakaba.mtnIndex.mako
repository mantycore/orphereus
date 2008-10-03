# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />
${_('Available actions:')}
<table width="100%" class="hlTable">

<tr>
<td>
<form method="post" action="service/all">
<span style="color: red; font-weight: bold;">${_('Run all actions (without auto bans)')}</span>
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="service/clearOekaki">
${_('Destroy unused oekaki IDs (older than one day)')}
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="service/destroyInvites">
${_('Destroy unused invites (older than one week)')}
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="service/destroyTrackers">
${_('Destroy IP trackers (older than one day)')}
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="service/banRotate">
${_('Remove old bans')}
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="service/updateCaches">
${_('Update caches')}
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="service/banInactive">
${_('Ban ALL users without posts')}
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="service/integrityChecks">
<span style="color: red;">${_('Integrity checks')}</span>
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

</table>
