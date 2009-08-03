# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

%if c.showAttemptForm:
<div class="postarea">
    <form id="userEditReasonForm" method="post" action="${h.url_for('hsIpBanAttempt', pid=c.pid)}">
<table>
    <tr>
        <td>${_('Reason:')}</td>
        <td><input type='text' name='IpViewReason'></td>
    </tr>
    <tr>
        <td>&nbsp;</td>
        <td><input type='submit' name='editUser' value='${_('Show IP info')}'></td>
    </tr>
</table>
    </form>
</div>

%else:

<div class="postarea">
    <form id="postform" method="post" action="${h.url_for('hsBanEdit')}">
    <input type="hidden" name="id" value="${c.ban.id}" />
        <table>
            <tbody>
                %if c.message:
                    <tr id="trmessage">
                        <td colspan=2>
                            <span class="theader">
                                ${c.message}
                            </span>
                        </td>
                    </tr>
                %endif
                <tr>
                    <td class="postblock">${_('Enable')}</td>
                    <td>
                        <input type="checkbox" name="enabled" ${c.ban.enabled and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('IP')}</td>
                    <td>
                        <input type="text" name="ip" size="35" value="${h.intToIp(int(c.ban.ip))}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Mask')}</td>
                    <td>
                        <input type="text" name="mask" size="35" value="${h.intToIp(int(c.ban.mask))}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Reason')}</td>
                    <td>
                        <input type="text" name="reason" size="35" value="${c.ban.reason}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('No access at all')}</td>
                    <td>
                        <input type="checkbox" name="type" ${c.ban.type and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Date')}</td>
                    <td>
                        <input type="text" name="date" size="35" value="${c.ban.date}" readonly="readonly" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Period')}</td>
                    <td>
                        <input type="text" name="period" size="35" value="${c.ban.period}" />
                    </td>
                </tr>
                <tr>
                    <td colspan="2">
                        %if c.exists:
                            <input type="submit" value="${_('Update')}" />
                            <input type="submit" value="${_('Delete')}" name="delete" />
                        %else:
                            <input type="submit" value="${_('Create')}" />
                        %endif
                    </td>
                </tr>
            </tbody>
        </table>
    </form>
</div>

%endif