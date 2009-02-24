# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />
<div class="theader">${_('Profile')}</div>

<form id="postform" action="/userProfile/" method="post">
    <div class="postarea">
        <table>
            <tbody>
                %if c.profileChanged:
                    <tr>
                        <td colspan="2" style="text-align: center;">
                          <span class="theader">
                            ${c.profileMsg}
                          </span>
                        </td>
                    </tr>
                %endif
                <tr>
                    <td colspan="2" style="text-align: center; font-weight: bold;">${_('Security')}</td>
                </tr>
                <tr id="truid">
                    <td class="postblock">${_('UID')}</td>
                    <td><input value="${c.userInst.uid}" readonly /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Current Security Code')}</td>
                    <td><input name="currentKey" value="" type="password" /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('New Security Code')}</td>
                    <td><input name="key" value=""  type="password" /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Repeat Security Code')}</td>
                    <td><input name="key2" value=""  type="password" /></td>
                </tr>
                <tr>
                    <td colspan="2" style="font-size: 70%; font-style:italic;">
                      ${_('Security code should be at least %d symbols') % g.OPT.minPassLength}<br/>
                      ${_("Leave this fields empty if you don't wish to change your security code and UID")}
                    </td>
                </tr>
                <tr>
                    <td colspan="2" style="text-align: center; font-weight: bold;">${_('Customization')}</td>
                </tr>
                <tr id="trtpp">
                    <td class="postblock">${_('Threads per page')}</td>
                    <td><input name="threadsPerPage" value="${c.userInst.threadsPerPage()}" /></td>
                </tr>
                <tr id="trrpt">
                    <td class="postblock">${_('Replies per thread')}</td>
                    <td><input name="repliesPerThread" value="${c.userInst.repliesPerThread()}" /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Mix old threads into boards')}</td>
                    <td><input type="checkbox" name="mixOldThreads" ${c.userInst.mixOldThreads() and "checked" or ""} /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Hide long comments')}</td>
                    <td><input type="checkbox" name="hideLongComments" ${c.userInst.hideLongComments() and "checked" or ""} /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Use AJAX hints')}</td>
                    <td><input type="checkbox" name="useAjax" ${c.userInst.useAjax() and "checked" or ""} /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Expand images in threads')}</td>
                    <td><input type="checkbox" name="expandImages" ${c.userInst.expandImages() and "checked" or ""} /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Max size to expand')}
                    <div style="font-size: 60%; font-style:italic;">(Max side will be used)</div>
                    </td>
                    <td>
                    <input name="maxExpandWidth" value="${c.userInst.maxExpandWidth()}" size="5"/>
                    &#215;
                    <input name="maxExpandHeight" value="${c.userInst.maxExpandHeight()}"  size="5" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Max height to expand')}</td>
                    <td></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Home filter exclusions')}</td>
                    <td><input name="homeExclude" value="${c.homeExclude}" /></td>
                </tr>
                <tr id="trstyle">
                    <td class="postblock">${_('By default Go To')}</td>
                    <td>
                    <select name="defaultGoto" style="width: 170px;">
                            %for dest in c.destinations.keys():
                               <option value="${dest}"
                                 %if dest == c.userInst.defaultGoto():
                                    selected
                                 %endif
                               >

                              ${_(c.destinations[dest])}</option>
                            %endfor
                    </select>
                    </td>
                </tr>
                <tr id="trtempl">
                    <td class="postblock" style="width: 170px;">${_('Template')}</td>
                    <td>
                        <select name name="template">

                            %for t in c.templates:
                               <option value="${t}"
                                 %if t == c.userInst.template():
                                    selected
                                 %endif
                               >

                              ${t}</option>
                            %endfor
                        </select>
                    </td>
                </tr>
                <tr id="trstyle">
                    <td class="postblock" style="width: 170px;">${_('Style')}</td>
                    <td>
                        <select name="style">
                            %for style in c.styles:
                               <option value="${style}"
                                 %if style == c.userInst.style():
                                    selected
                                 %endif
                               >

                              ${style}</option>
                            %endfor
                        </select>
                    </td>
                </tr>
                <tr>
                    <td colspan="2"><input name="update" type="submit" value="${_('Update')}" /></td>
                </tr>
                <tr>
                    <td colspan="2" style="text-align: center; font-weight: bold;">${_('User filters')}</td>
                </tr>
                %for f in c.userInst.filters:
                <tr id="filterId${f.id}">
                    <td class="postblock">[<a href="" onclick="userFiltersEdit(event,${f.id});">Edit</a>] [<a href='' onClick="userFiltersDelete(event,${f.id});">Del</a>]</td>
                    <td><input id='filterId${f.id}Input' name='filterId${f.id}' value='${f.filter}' /></td>
                </tr>
                %endfor
                <tr id="newFilterTR">
                    <td class="postblock">${_('New filter')}</td>
                    <td><input id="newFilterInput" name="newFilter" value="" /></td>
                </tr>
                <tr>
                    <td colspan="2"><input name="update" type="button" value="${_('Add')}" onclick="userFiltersAdd(event)" /></td>
                </tr>
                <tr>
                    <td colspan="2" style="text-align: center; font-weight: bold;">${_('Hidden threads')}</td>
                </tr>
                %for t in c.hiddenThreads:
                <tr>
                    <td>${_('Thread <a href=/%s>#%s</a> (%s replies) posted in %s') % (t.id, t.id, t.replyCount, t.tagLine)}</td>
                    <td><a href="/ajax/showThread/${t.id}/userProfile">${_('Unhide')}</a></td>
                </tr>
                %endfor
            </tbody>
        </table>
    </div>
</form>
<br clear="all" />
