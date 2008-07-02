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
                <tr id="trtag">
                    <td class="postblock">${_('Tag')}</td>
                    <td>
                        <input type="text" name="tag" size="35" value="${c.tag.tag}" />
                    </td>
                </tr>
                <tr id="trtitle">
                    <td class="postblock">${_('Title')}</td>
                    <td>
                        <input type="text" name="comment" size="35" value="${c.tag.options.comment}" />
                    </td>
                </tr>
                <tr id="trsection">
                    <td class="postblock">${_('Section')}</td>
                    <td>
                        <input type="text" name="sectionId" size="35" value="${c.tag.options.sectionId}" />
                    </td>
                </tr>
                <tr id="trsection">
                    <td class="postblock">${_('Persistent')}</td>
                    <td>
                        <input type="checkbox" name="persistent" ${c.tag.options.persistent and "checked" or ""} />
                    </td>
                </tr>
                <tr id="trsection">
                    <td class="postblock">${_('Allow OPs without image')}</td>
                    <td>
                        <input type="checkbox" name="imagelessThread" ${c.tag.options.imagelessThread and "checked" or ""} />
                    </td>
                </tr>
                <tr id="trsection">
                    <td class="postblock">${_('Allow replies without image')}</td>
                    <td>
                        <input type="checkbox" name="imagelessPost" ${c.tag.options.imagelessPost and "checked" or ""} />
                    </td>
                </tr>
                <tr id="trsection">
                    <td class="postblock">${_('Allow files')}</td>
                    <td>
                        <input type="checkbox" name="images" ${c.tag.options.images and "checked" or ""} />
                    </td>
                </tr>
                <tr id="trsection">
                    <td class="postblock">${_('Allow spoilers')}</td>
                    <td>
                        <input type="checkbox" name="spoilers" ${c.tag.options.enableSpoilers and "checked" or ""} />
                    </td>
                </tr>                
                <tr id="trsection">
                    <td class="postblock">${_('Max filesize (bytes)')}</td>
                    <td>
                        <input type="text" name="maxFileSize" size="35" value="${c.tag.options.maxFileSize}" />
                    </td>
                </tr>
                <tr id="trsection">
                    <td class="postblock">${_('Minimal size for images (pixels)')}</td>
                    <td>
                        <input type="text" name="minPicSize" size="35" value="${c.tag.options.minPicSize}" />
                    </td>
                </tr>
                <tr id="trsection">
                    <td class="postblock">${_('Thumbnail size (pixels)')}</td>
                    <td>
                        <input type="text" name="thumbSize" size="35" value="${c.tag.options.thumbSize}" />
                    </td>
                </tr>
                <tr>
                    <td colspan='2'><input type='submit' value='${_('Update')}'></td>
                </tr>                           
            </tbody>
        </table>
    </form>                 
</div>
