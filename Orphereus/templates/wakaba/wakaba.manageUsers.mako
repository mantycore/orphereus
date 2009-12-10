# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

<div class="postarea">
    <form id="postform" method="post" action="${h.url_for('hsUsers')}">
        <table>
            <tbody>
                %if c.message:
                <tr id="trmessage">
                    <td colspan="2">${c.message}</td>
                </tr>
                %endif
                <tr>
                    <td  colspan="2" class="postblock">${_('UID or uidNumber')}</td>
                </tr>
                <tr>
                    <td>
                        <input type="text" name="uid" size="35" value="" />
                    </td>
                    <td>
                        <input type="submit" name="view" value="${_('View')}" />
                    </td>
                </tr>
                <tr>
                    <td><a href="${h.url_for("hsBans")}">${_("Banned:")}</a></td>
                    <td>${c.ustats[1]}</td>
                </tr>
                <tr>
                    <td><a href="${h.url_for("hsUsers", showRO=True)}">${_("Read-only:")}</a></td>
                    <td>${c.ustats[2]} <input type="submit" name="deactivateRO" value="${_('Deactivate all')}" /></td>
                </tr>
                <tr>
                    <td>${_("Total:")}</td>
                    <td>${c.ustats[0]}</td>
                </tr>
%if c.roActive:
%endif
            </tbody>
        </table>
    </form>
</div>
