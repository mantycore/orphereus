# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

<div class="postarea">
    <form id="postform" method="post" action="${h.url_for('hsBoardEdit', tag=c.tag.tag)}">
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
                    <td class="postblock">${_('Tag')}</td>
                    <td>
                        <input type="text" name="tag" size="35"
                        %if c.tag.tag:
                            value="${c.tag.tag}"
                        %endif
                        />
                        <a href="${h.url_for('boardBase', board=c.tag.tag)}" target="_blank">Show board</a>
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Title')}</td>
                    <td>
                        <input type="text" name="comment" size="35" value="${c.tag.comment}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Special board rules (split with ";")')}</td>
                    <td>
                        <input type="text" name="specialRules" size="35" value="${c.tag.specialRules}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Section')}</td>
                    <td>
                        <input type="text" name="sectionId" size="35" value="${c.tag.sectionId}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Weight in section')}</td>
                    <td>
                        <input type="text" name="sectionWeight" size="35" value="${c.tag.sectionWeight}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Persistent')}</td>
                    <td>
                        <input type="checkbox" name="persistent" ${c.tag.persistent and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Service')}
                    <div style="font-size: 60%; font-style:italic;">${_('(Disable deletion during maintenance, place into special group)')}</div>
                    </td>
                    <td>
                        <input type="checkbox" name="service" ${c.tag.service and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Allow OPs without image')}</td>
                    <td>
                        <input type="checkbox" name="imagelessThread" ${c.tag.imagelessThread and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Allow replies without image')}</td>
                    <td>
                        <input type="checkbox" name="imagelessPost" ${c.tag.imagelessPost and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Allow files')}</td>
                    <td>
                        <input type="checkbox" name="images" ${c.tag.images and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Allow spoilers')}</td>
                    <td>
                        <input type="checkbox" name="spoilers" ${c.tag.enableSpoilers and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Allow OP to delete his threads')}</td>
                    <td>
                        <input type="checkbox" name="canDeleteOwnThreads" ${c.tag.canDeleteOwnThreads and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Allow OP to moderate thread')}</td>
                    <td>
                        <input type="checkbox" name="selfModeration" ${c.tag.selfModeration and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Max filesize (bytes)')}</td>
                    <td>
                        <input type="text" name="maxFileSize" size="35" value="${c.tag.maxFileSize}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Minimal size for images (pixels)')}</td>
                    <td>
                        <input type="text" name="minPicSize" size="35" value="${c.tag.minPicSize}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Thumbnail size (pixels)')}</td>
                    <td>
                        <input type="text" name="thumbSize" size="35" value="${c.tag.thumbSize}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Show tag in overview')}</td>
                    <td>
                        <input type="checkbox" name="showInOverview" ${c.tag.showInOverview and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Bumplimit')}
                    <div style="font-size: 60%; font-style:italic;">${_('(0 for unlimited)')}</div>
                    </td>
                    <td>
                        <input type="text" name="bumplimit" size="35" value="${c.tag.bumplimit and c.tag.bumplimit or "0"}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Additional files allowed')}
                    <div style="font-size: 60%; font-style:italic;">${_('(Any non-integer value for default, 0 for none)')}</div>
                    </td>
                    <td>
                        <input type="text" name="allowedAdditionalFiles" size="35" value="${(c.tag.allowedAdditionalFiles is None) and "Default" or c.tag.allowedAdditionalFiles}" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock" style="color: red;">${_('Tag for admins only')}</td>
                    <td>
                        <input type="checkbox" name="adminOnly" ${c.tag.adminOnly and 'checked="checked"' or ""} />
                    </td>
                </tr>
                <tr>
                    <td class="postblock" style="color: red;">${_('DELETE BOARD')}</td>
                    <td>
                        <input type="checkbox" name="deleteBoard" />
                    </td>
                </tr>
                <tr>
                    <td colspan='2'><input type='submit' value='${_('Update')}' /></td>
                </tr>
            </tbody>
        </table>
    </form>
</div>
