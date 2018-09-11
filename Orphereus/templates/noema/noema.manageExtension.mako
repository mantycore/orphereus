# -*- coding: utf-8 -*-
<%inherit file="noema.management.mako" />

<div class="postarea">
    <form id="postform" method="post" action="${h.url_for('hsExtensionEdit', name=c.ext.ext)}">
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
                    <td class="postblock">${_('Extension')}</td>
                    <td>
                        <input type="text" name="ext" size="35" value="${c.ext.ext}"
                        %if c.exists:
                            readonly="readonly"
                        %endif
                        />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Posting enabled')}</td>
                    <td>
                        <input type="checkbox" name="enabled" ${c.ext.enabled and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Open links in new window')}</td>
                    <td>
                        <input type="checkbox" name="newWindow" ${c.ext.newWindow and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Type')}</td>
                    <td>
                        <input type="text" name="type" size="35" value="${c.ext.type}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">
                        ${_('Thumbnail path')}
                        <div style="font-size: 50%;"><i>${_('Relative to <b>staticPathWeb</b> from config')}</i></div>
                    </td>
                    <td>
                        <input type="text" name="path" size="35" value="${c.ext.path}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Thumbnail width')}</td>
                    <td>
                        <input type="text" name="thwidth" size="35" value="${c.ext.thwidth}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Thumbnail height')}</td>
                    <td>
                        <input type="text" name="thheight" size="35" value="${c.ext.thheight}" />
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
