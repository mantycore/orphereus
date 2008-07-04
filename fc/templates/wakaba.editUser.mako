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
                    <td colspan=2>${_('Access')}</td>
                </tr>
                <tr>
                    <td class="postblock">${_('Can delete posts')}</td>
                    <td>
                        <input type="checkbox" name="canDeleteAllPosts" ${not c.userInst.canChangeRights() and "disabled" or ""} ${c.user.options.canDeleteAllPosts and "checked" or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Admin')}</td>
                    <td>
                        <input type="checkbox" name="isAdmin" ${not c.userInst.canChangeRights() and "disabled" or ""} ${c.user.options.isAdmin and "checked" or ""} />
                    </td>
                </tr>     
                <tr>
                    <td class="postblock">${_('Can make invite')}</td>
                    <td>
                        <input type="checkbox" name="canMakeInvite" ${not c.userInst.canChangeRights() and "disabled" or ""} ${c.user.options.canMakeInvite and "checked" or ""} />
                    </td>
                </tr>  
                <tr>
                    <td class="postblock">${_('CAN CHANGE USER RIGHTS')}</td>
                    <td>
                        <input type="checkbox" name="canChangeRights" ${not c.userInst.canChangeRights() and "disabled" or ""} ${c.user.options.canChangeRights and "checked" or ""} />
                    </td>
                </tr>                
                <tr>
                    <td colspan='2'><input type='submit' name='access' value='${_('Update')}' ${not c.userInst.canChangeRights() and "disabled" or ""}></td>
                </tr>
                <tr>
                    <td colspan=2>${_('Ban')}</td>
                </tr>                
                %if c.user.options.bantime:
                <tr>
                    <td class="postblock">${_('Bantime (days)')}</td>
                    <td>
                        ${c.user.options.bantime}
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Ban reason')}</td>
                    <td>
                        ${c.user.options.banreason}
                    </td>
                </tr>
                <tr>
                    <td colspan='2'><input type='submit' name='unban' value='${_('Unban')}'></td>
                </tr>
                %else:
                <tr>
                    <td class="postblock">${_('Bantime (days)')}</td>
                    <td>
                        <input type="text" name="bantime" size="35" value="0" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Ban reason')}</td>
                    <td>
                        <input type="text" name="banreason" size="35" value="" />
                    </td>
                </tr>
                <tr>
                    <td colspan='2'><input type='submit' name='ban' value='${_('Ban')}'></td>
                </tr>
                %endif
                <tr>
                    <td colspan=2>${_('Look up posts')}</td>
                </tr>
                <tr>
                    <td class="postblock">${_('Quantity')}</td>
                    <td>
                        <input type="text" name="quantity" size="35" value="100" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Reason')}</td>
                    <td>
                        <input type="text" name="lookupreason" size="35" value="" />
                    </td>
                </tr>                
                <tr>
                    <td colspan='2'><input type='submit' name='lookup' value='${_('Look up')}'></td>
                </tr>
                <tr>
                    <td colspan=2>${_('Delete user')}</td>
                </tr>
                <tr>
                    <td class="postblock">${_('Reason')}</td>
                    <td>
                        <input type="text" name="deletereason" size="35" value="" />
                    </td>
                </tr>
                <tr>
                    <td colspan='2'><input type='submit' name='delete' value='${_('Delete')}'></td>
                </tr>                
            </tbody>
        </table>
    </form>                 
</div>