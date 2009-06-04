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

%for action in c.obligatoryActions:
<tr>
<td>
<form method="post" action="${h.url_for('hsMaintenance', actid=action)}">
${c.descriptions.get(action, action)}
<br/>
<input type="submit" value="Launch" />
</form>
</td>
</tr>
%endfor

</table>


<h3>${_('Optional actions')}</h3>
<table width="100%" class="hlTable">

%for action in c.optionalActions:
<tr>
<td>
<form method="post" action="${h.url_for('hsMaintenance', actid=action)}">
${c.descriptions.get(action, action)}
<br/>
<input type="submit" value="Launch" />
</form>
</td>
</tr>
%endfor

</table>

