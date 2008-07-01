# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />

<div class="postarea">
    <form id="postform" method="post">
        <table>
            <tbody>
                %if c.message:
                    <tr id="trmessage">
                        <td colspan=2>${c.message}</td>
                    </tr>
                %endif
                <tr>
                    <td class="postblock">${_('UID or UID_Number')}</td>
                    <td>
                        <input type="text" name="uid" size="35" value="" /><input type="submit" value="${_('View')}">
                    </td>
                </tr>
            </tbody>
        </table>
    </form>
</div>