# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

<table  width="100%" class="hlTable">
<thead>
<tr>
<td>${_("Id")}</td>
<td>${_("Description")}</td>
<td>${_("Dependencies")}</td>
<td>${_("Namespace")}</td>
<td>${_("File name")}</td>
</tr>
</thead>
<tbody>
%for plugin in c.plugins:
<tr>
<td>${plugin.pluginId()}</td>
<td>${plugin.pluginName()}</td>
<td>${plugin.deps()}</td>
<td>${plugin.namespaceName()}</td>
<td>${plugin.fileName()}</td>
</tr>
%endfor
</tbody>
</table>

${_("%d plugins are active now") % len(c.plugins)}
<hr/>
