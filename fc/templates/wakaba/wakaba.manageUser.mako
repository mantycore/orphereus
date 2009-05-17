# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

%if c.showAttemptForm:
<div class="postarea">
    <form id="userEditReasonForm" method="post" action="${h.url_for('hsUserEditByPost', pid=c.pid)}">
<table>
    <tr>
        <td>Reason:</td>
        <td><input type='text' name='UIDViewReason'></td>
    </tr>
    <tr>
        <td>&nbsp;</td>
        <td><input type='submit' name='editUser' value='${_('Show user info')}'></td>
    </tr>
</table>
    </form>
</div>

%else:

<div class="postarea">
    <form id="postform" method="post" action="${h.url_for('hsUserEdit', uid=c.user.uidNumber)}">
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
                    <td colspan="2">${_('Access')}</td>
                </tr>
                <tr>
                    <td class="postblock"><u>${_('Admin')}</u></td>
                    <td>
                        <input type="checkbox" name="isAdmin" ${not c.userInst.canChangeRights() and 'disabled="disabled"' or ""}
                        ${c.user.options.isAdmin and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Can delete posts')}</td>
                    <td>
                        <input type="checkbox" name="canDeleteAllPosts" ${not c.userInst.canChangeRights() and 'disabled="disabled"' or ""}
                        ${c.user.options.canDeleteAllPosts and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Can make invite')}</td>
                    <td>
                        <input type="checkbox" name="canMakeInvite" ${not c.userInst.canChangeRights() and 'disabled="disabled"' or ""}
                        ${c.user.options.canMakeInvite and 'checked="checked"' or ""} />
                    </td>
                </tr>

                <tr>
                    <td class="postblock">${_('Can change settings')}</td>
                    <td>
                        <input type="checkbox" name="canChangeSettings" ${not c.userInst.canChangeRights() and 'disabled="disabled"' or ""}
                        ${c.user.options.canChangeSettings and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Can manage boards')}</td>
                    <td>
                        <input type="checkbox" name="canManageBoards" ${not c.userInst.canChangeRights() and 'disabled="disabled"' or ""}
                        ${c.user.options.canManageBoards and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Can manage extensions')}</td>
                    <td>
                        <input type="checkbox" name="canManageExtensions" ${not c.userInst.canChangeRights() and 'disabled="disabled"' or ""}
                        ${c.user.options.canManageExtensions and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Can manage mappings')}</td>
                    <td>
                        <input type="checkbox" name="canManageMappings" ${not c.userInst.canChangeRights() and 'disabled="disabled"' or ""}
                        ${c.user.options.canManageMappings and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Can run maintenance')}</td>
                    <td>
                        <input type="checkbox" name="canRunMaintenance" ${not c.userInst.canChangeRights() and 'disabled="disabled"' or ""}
                        ${c.user.options.canRunMaintenance and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Can manage users')}
                    <div style="font-size: 60%; font-style:italic;">${_('(Suppresses by canChangeRights)')}</div>
                    </td>
                    <td>
                        <input type="checkbox" name="canManageUsers" ${not c.userInst.canChangeRights() and 'disabled="disabled"' or ""}
                        ${c.user.options.canManageUsers and 'checked="checked"' or ""} />
                    </td>
                </tr>

                <tr>
                    <td class="postblock"><u>${_('CAN CHANGE USER RIGHTS')}</u></td>
                    <td>
                        <input type="checkbox" name="canChangeRights" ${not c.userInst.canChangeRights() and 'disabled="disabled"' or ""} ${c.user.options.canChangeRights and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td colspan="2"><input type="submit" name="access" value="${_('Update')}" ${not c.userInst.canChangeRights() and 'disabled="disabled"' or ""}/></td>
                </tr>
                <tr>
                    <td colspan="2">${_('Ban')}</td>
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
                    <td colspan="2"><input type="submit" name="unban" value="${_('Unban')}"></td>
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
                    <td colspan='2'><input type="submit" name="ban" value="${_('Ban')}" /></td>
                </tr>
                %endif
                <tr>
                    <td colspan="2">${_('Delete user')}</td>
                </tr>
                <tr>
                    <td class="postblock">${_('Reason')}</td>
                    <td>
                        <input type="text" name="deletereason" size="35" value="" /><br/>
                        <input type="checkbox" name="deleteLegacy" /> ${_("Remove all users's posts")}
                    </td>
                </tr>
                <tr>
                    <td colspan="2"><input type="submit" name="delete" value="${_('Delete')}" ${not c.userInst.canChangeRights() and 'disabled="disabled"' or ""} /></td>
                </tr>

                <tr>
                    <td colspan="2">${_('Look up posts')}</td>
                </tr>
                <tr>
                    <td class="postblock">${_('Quantity of last posts to view')}</td>
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
                    <td colspan="2"><input type="submit" name="lookup" value="${_('Look up')}" /></td>
                </tr>

                <tr>
                    <td colspan="2">${_('Change security code')}</td>
                </tr>
                <tr>
                    <td class="postblock">${_('New Security Code')}</td>
                    <td><input name="key" value="" size="35" type="password" /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Repeat Security Code')}</td>
                    <td><input name="key2" value="" size="35" type="password" /></td>
                </tr>
                <tr>
                    <td colspan="2"><input type="submit" name="passwd" value="${_('Change')}"/></td>
                </tr>
            </tbody>
        </table>
    </form>
</div>

%endif
