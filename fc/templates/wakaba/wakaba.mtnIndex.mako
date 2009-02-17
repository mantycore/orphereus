# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />

<h3>${_('Obligatory actions')}</h3>
<table width="100%" class="hlTable">

<tr>
<td>
<form method="post" action="service/all">
<span style="color: red; font-weight: bold;">${_('Run all actions')}</span>
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
<form method="post" action="service/integrityChecks">
<span style="color: red;">${_('Integrity checks')}</span>
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

</table>


<h3>${_('Optional actions')}</h3>
<table width="100%" class="hlTable">

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
<form method="post" action="service/updateStats">
${_('Update statistics')}
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="service/removeEmptyTags">
${_('Remove empty tags')}
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
<form method="post" action="service/reparse">
${_('Reparse posts which can be reparsed')}
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="service/sortUploads">
${_('Sort uploads')}
<br/>
<input type="submit" value="Launch">
</form>
</td>
</tr>

</table>

