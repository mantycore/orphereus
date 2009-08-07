# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

<div class="postarea">
    <form id="postform" method="post" enctype="multipart/form-data"  action="${h.url_for('hsImportThread')}">
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
                    <td class="postblock">${_('Thread archive')}</td>
                    <td>
						<input type="file" name="file" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Preserve post IDs')}</td>
                    <td>
                    	<input type="checkbox" name="useIds" checked="checked" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Preserve dates')}</td>
                    <td>
                    	<input type="checkbox" name="useDate" checked="checked" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Tagline')}</td>
                    <td>
                        <input type="text" name="tagline" size="35"/>
                    </td>
                </tr>
                <tr>
                	<td>
		            	<input type="submit" value="${_('Import')}" />
                    </td>
                </tr>
            </tbody>
        </table>
    </form>
</div>
