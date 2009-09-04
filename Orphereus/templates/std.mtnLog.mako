# -*- coding: utf-8 -*-
<table width="100%" class="hlTable">
    <tr>
        <td>Type</td>
        <td>Message</td>
    </tr>
%for u in c.mtnLog:
    <tr>
        <td>${u.type}</td>
        <td>${u.message}</td>
    </tr>
%endfor
</table>