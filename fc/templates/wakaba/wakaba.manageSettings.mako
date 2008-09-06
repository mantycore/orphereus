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
                %for s in g.settingsMap:
                <tr>
                    <td class="postblock">${g.settingsMap[s].name}</td>
                    <td>
                        <input type="text" name="${g.settingsMap[s].name}" size="35" value="${g.settingsMap[s].value}" />
                    </td>
                </tr>
                %endfor
                <tr>
                    <td colspan='2'><input type='submit' name='update' value='${_('Update')}'></td>
                </tr>                           
            </tbody>
        </table>
    </form>                 
</div>
