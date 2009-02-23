# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />
${_('Current members of Holy Synod')}
<table class="hlTable">
<tr>
<td>Number</td>
<td colspan>Mod</td>
<td colspan>Invites</td>
<td colspan>Opt</td>
<td colspan>Boards</td>
<td colspan>Users</td>
<td colspan>Ext</td>
<td colspan>Mapping</td>
<td colspan>Maint</td>
</tr>
%for u in c.admins:
    <tr
    %if u.uidNumber == c.userInst.uidNumber():
    style="font-weight: bold;"
    %endif
    >
        <td><div class="hovblock"><a style="display: block;" href='/holySynod/manageUsers/edit/${u.uidNumber}'>${u.uidNumber}</a></div></td>
        <td>${u.canDeleteAllPosts() and "+" or ""}</td>
        <td>${u.canMakeInvite() and "+" or ""}</td>
        <td>${u.canChangeSettings() and "+" or ""}</td>
        <td>${u.canManageBoards() and "+" or ""}</td>
        <td>${u.canManageUsers() and "+" or ""}</td>
        <td>${u.canManageExtensions() and "+" or ""}</td>
        <td>${u.canManageMappings() and "+" or ""}</td>
        <td>${u.canRunMaintenance() and "+" or ""}</td>
    </tr>
%endfor
</table>
