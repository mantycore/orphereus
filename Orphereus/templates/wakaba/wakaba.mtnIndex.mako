# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

<h3>${_('Obligatory actions')}</h3>
<table width="100%" class="hlTable">

<tr>
<td>
<form method="post" action="${h.url_for('hsMaintenance', actid='all')}">
<span style="color: red; font-weight: bold;">${_('Run all actions')}</span>
<br/>
<input type="submit" value="Launch" />
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="${h.url_for('hsMaintenance', actid='clearOekaki')}">
${_('Destroy unused oekaki IDs (older than one day)')}
<br/>
<input type="submit" value="Launch" />
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="${h.url_for('hsMaintenance', actid='destroyInvites')}">
${_('Destroy unused invites (older than one week)')}
<br/>
<input type="submit" value="Launch" />
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="${h.url_for('hsMaintenance', actid='destroyTrackers')}">
${_('Destroy IP trackers (older than one day)')}
<br/>
<input type="submit" value="Launch" />
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="${h.url_for('hsMaintenance', actid='banRotate')}">
${_('Remove old bans')}
<br/>
<input type="submit" value="Launch" />
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="${h.url_for('hsMaintenance', actid='integrityChecks')}">
<span style="color: red;">${_('Integrity checks')}</span>
<br/>
<input type="submit" value="Launch" />
</form>
</td>
</tr>

</table>


<h3>${_('Optional actions')}</h3>
<table width="100%" class="hlTable">

<tr>
<td>
<form method="post" action="${h.url_for('hsMaintenance', actid='updateCaches')}">
${_('Update caches')}
<br/>
<input type="submit" value="Launch" />
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="${h.url_for('hsMaintenance', actid='updateStats')}">
${_('Update statistics')}
<br/>
<input type="submit" value="Launch" />
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="${h.url_for('hsMaintenance', actid='removeEmptyTags')}">
${_('Remove empty tags')}
<br/>
<input type="submit" value="Launch" />
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="${h.url_for('hsMaintenance', actid='banInactive')}">
${_('Ban ALL users without posts')}
<br/>
<input type="submit" value="Launch" />
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="${h.url_for('hsMaintenance', actid='reparse')}">
${_('Reparse posts which can be reparsed')}
<br/>
<input type="submit" value="Launch" />
</form>
</td>
</tr>

<tr>
<td>
<form method="post" action="${h.url_for('hsMaintenance', actid='sortUploads')}">
${_('Sort uploads')}
<br/>
<input type="submit" value="Launch" />
</form>
</td>
</tr>

</table>

