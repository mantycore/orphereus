# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

<div class="postarea">
    <form id="postform" method="post" action="${h.url_for('hsUsers')}">
        <table>
            <tbody>
                %if c.message:
                    <tr id="trmessage">
                        <td colspan=2>${c.message}</td>
                    </tr>
                %endif
                <tr>
                    <td class="postblock">${_('UID or uidNumber')}</td>
                    <td>
                        <input type="text" name="uid" size="35" value="" />
                        <input type="submit" value="${_('View')}" />
                    </td>
                </tr>
            </tbody>
        </table>
    </form>
</div>
