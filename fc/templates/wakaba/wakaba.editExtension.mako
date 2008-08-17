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
                    <td class="postblock">${_('Extension')}</td>
                    <td>
                        <input type="text" name="ext" size="35" value="${c.ext.ext}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Thumbnail path')}</td>
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
                    <td class="postblock">${_('Type')}</td>
                    <td>
                        <input type="text" name="type" size="35" value="${c.ext.type}" />
                    </td>
                </tr>
                <tr>
                    <td colspan='2'><input type='submit' value='${_('Update')}'></td>
                </tr>                           
            </tbody>
        </table>
    </form>                 
</div>
