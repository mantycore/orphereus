# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />
<div class="theader">${_('Profile')}</div>

<form id="postform" action="/userProfile/" method="post">
    <div class="postarea">
        <table>
            <tbody>
                %if c.profileChanged:
                    <tr>
                        <td colspan='2'><strong>${_('Profile was updated.')}</strong></td>
                    </tr>                    
                %endif   
                <tr id="truid">
                    <td class="postblock">${_('UID')}</td>
                    <td>${c.userInst.uid()}</td>
                </tr>
                <tr id="trtpp">
                    <td class="postblock">${_('Threads per page')}</td>
                    <td><input name='threadsPerPage' value='${c.userInst.threadsPerPage()}'></td>
                </tr>
                <tr id="trppt">
                    <td class="postblock">${_('Posts per thread')}</td>
                    <td><input name='postsPerThread' value='${c.userInst.postsPerThread()}'></td>
                </tr>
                <tr id="trtempl">
                    <td class="postblock">${_('Template')}</td>
                    <td><input name='template' value='${c.userInst.template()}'></td>
                </tr>
                <tr id="trstyle">
                    <td class="postblock">${_('Style')}</td>
                    <td><input name='style' value='${c.userInst.style()}'></td>
                </tr>
                <tr>
                    <td colspan='2'><input type='submit' value='${_('Update')}'></td>
                </tr>                
            </tbody>
        </table>
    </div>
</form>