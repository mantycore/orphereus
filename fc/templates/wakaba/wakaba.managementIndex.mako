# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />
${_('Current members of Holy Synod')}
<table class="hlTable">
<tr>
<td width="10%" align="center">Number</td>
<td width="10%" align="center"><b>Rights</b></td>
<td width="10%" align="center">Mod</td>
<td width="10%" align="center">Invites</td>
<td width="10%" align="center">Opt</td>
<td width="10%" align="center">Boards</td>
<td width="10%" align="center">Users</td>
<td width="10%" align="center">Ext</td>
<td width="10%" align="center">Mapping</td>
<td width="10%" align="center">Maint</td>
</tr>
%for u in c.admins:
    <tr>
        <td
            %if u.uidNumber == c.userInst.uidNumber:
            class="highlight"
            %endif
        ><div class="hovblock"><a style="display: block;" href='/holySynod/manageUsers/edit/${u.uidNumber}'>${u.uidNumber}</a></div></td>
        <td align="center">${u.canChangeRights() and "&#8226;" or ""}</td>
        <td align="center">${u.canDeleteAllPosts() and "&#8226;" or ""}</td>
        <td align="center">${u.canMakeInvite() and "&#8226;" or ""}</td>
        <td align="center">${u.canChangeSettings() and "&#8226;" or ""}</td>
        <td align="center">${u.canManageBoards() and "&#8226;" or ""}</td>
        <td align="center">${u.canManageUsers() and "&#8226;" or ""}</td>
        <td align="center">${u.canManageExtensions() and "&#8226;" or ""}</td>
        <td align="center">${u.canManageMappings() and "&#8226;" or ""}</td>
        <td align="center">${u.canRunMaintenance() and "&#8226;" or ""}</td>
    </tr>
%endfor
</table>
