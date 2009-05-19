# -*- coding: utf-8 -*-
<%inherit file="wakaba.main.mako" />
<div class="theader">${_('Profile')}</div>

<form id="postform" action="${h.url_for('userProfile')}" method="post">
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

                %if not c.userInst.Anonymous:
                    <tr>
                        <td colspan="2" style="text-align: center; font-weight: bold;">${_('Security')}</td>
                    </tr>
                    <tr id="truid">
                        <td class="postblock">${_('UID')}</td>
                        <td><input value="${c.userInst.uid}" readonly="readonly" /></td>
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
                %else:
                    <tr>
                        <td colspan="2" style="text-align: center; font-weight: bold;">${_('You are in anonymous mode now. Settings will be saved in cookies')}</td>
                    </tr>
                %endif
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
                    <td><input type="checkbox" name="mixOldThreads" ${c.userInst.mixOldThreads() and 'checked="checked"' or ""} /></td>
                </tr>
                %if g.OPT.framedMain: 
                <tr>
                    <td class="postblock">${_('Use frames')}</td>
                    <td><input type="checkbox" name="useFrame" ${c.userInst.useFrame() and 'checked="checked"' or ""} /></td>
                </tr>
                %endif
                <tr>
                    <td class="postblock">${_('Hide long comments')}</td>
                    <td><input type="checkbox" name="hideLongComments" ${c.userInst.hideLongComments() and 'checked="checked"' or ""} /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Use AJAX hints')}</td>
                    <td><input type="checkbox" name="useAjax" ${c.userInst.useAjax() and 'checked="checked"' or ""} /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Expand images in threads')}</td>
                    <td><input type="checkbox" name="expandImages" ${c.userInst.expandImages() and 'checked="checked"' or ""} /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Use initial title shrinking')}</td>
                    <td><input type="checkbox" name="useTitleCollapse" ${c.userInst.useTitleCollapse() and 'checked="checked"' or ""} /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Max size to expand')}
                    <div style="font-size: 60%; font-style:italic;">${_('(Stricter condition will be used)')}</div>
                    </td>
                    <td>
                    <input name="maxExpandWidth" value="${c.userInst.maxExpandWidth()}" size="5"/>
                    &#215;
                    <input name="maxExpandHeight" value="${c.userInst.maxExpandHeight()}"  size="5" />
                    </td>
                </tr>
                <tr>
                    <td class="postblock">${_('Home filter exclusions')}
                    <div style="font-size: 60%; font-style:italic;">${_('(You can ignore only existing tags)')}</div>
                    </td>
                    <td><input name="homeExclude" value="${c.homeExclude}" /></td>
                </tr>
                <tr id="trgoto">
                    <td class="postblock">${_('By default Go To')}</td>
                    <td>
                    <select name="defaultGoto" style="width: 170px;">
                            %for dest in c.destinations.keys():
                               %if dest != 3 or g.OPT.allowOverview:
                                   <option value="${dest}"
                                     %if dest == c.userInst.defaultGoto():
                                        selected="selected"
                                     %endif
                                   >

                                  ${_(c.destinations[dest])}</option>
                               %endif
                            %endfor
                    </select>
                    </td>
                </tr>
                <tr id="trtempl">
                    <td class="postblock">${_('Template')}</td>
                    <td>
                        <select name="template" style="width: 170px;">

                            %for t in c.templates:
                               <option value="${t}"
                                 %if t == c.userInst.template():
                                    selected="selected"
                                 %endif
                               >

                              ${t}</option>
                            %endfor
                        </select>
                    </td>
                </tr>
                <tr id="trstyle">
                    <td class="postblock">${_('Style')}</td>
                    <td>
                        <select name="style" style="width: 170px;">
                            %for style in c.styles:
                               <option value="${style}"
                                 %if style == c.userInst.style():
                                    selected="selected"
                                 %endif
                               >

                              ${style}</option>
                            %endfor
                        </select>
                    </td>
                </tr>
                <tr id="trlang">
                    <td class="postblock">${_('Board language')}</td>
                    <td>
                        <select name="lang" style="width: 170px;">
                            %for lang in c.langs:
                               <option value="${lang}"
                                 %if lang == c.userInst.lang():
                                    selected="selected"
                                 %endif
                               >

                              ${lang}</option>
                            %endfor
                        </select>
                    </td>
                </tr>
                %if c.userInst.Anonymous:
                <tr id="captlang">
                    <td class="postblock">${_('Captcha language')}</td>
                    <td>
                        <select name="cLang" style="width: 170px;">
                            %for lang in c.langs:
                               <option value="${lang}"
                                 %if lang == c.userInst.cLang():
                                    selected="selected"
                                 %endif
                               >

                              ${lang}</option>
                            %endfor
                        </select>
                    </td>
                </tr>
                %endif
                <tr>
                    <td colspan="2" style="text-align: center; font-weight: bold;">${_('Oekaki defaults')}</td>
                </tr>
                <tr>
                    <td class="postblock">${_('Use Selfy')}</td>
                    <td><input type="checkbox" name="oekUseSelfy" ${c.userInst.oekUseSelfy() and 'checked="checked"' or ""} /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Record animation')}</td>
                    <td><input type="checkbox" name="oekUseAnim" ${c.userInst.oekUseAnim() and 'checked="checked"' or ""} /></td>
                </tr>
                <tr>
                    <td class="postblock">${_('Use Shi Pro')}</td>
                    <td><input type="checkbox" name="oekUsePro" ${c.userInst.oekUsePro() and 'checked="checked"' or ""} /></td>
                </tr>
                <tr>
                    <td colspan="2"><input name="update" type="submit" value="${_('Update')}" /></td>
                </tr>
                %if not c.userInst.Anonymous:
                    <tr>
                        <td colspan="2" style="text-align: center; font-weight: bold;">${_('User filters')}</td>
                    </tr>
                    %for f in c.userInst.filters:
                    <tr id="filterId${f.id}">
                        <td class="postblock">[<a href="" onclick="userFiltersEdit(event,${f.id});">${_('Edit')}</a>] [<a href="" onclick="userFiltersDelete(event,${f.id});">${_('Delete')}</a>]</td>
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
                %endif
                    <tr>
                        <td colspan="2" style="text-align: center; font-weight: bold;">${_('Hidden threads')}</td>
                    </tr>
                    %for t in c.hiddenThreads:
                    <tr>
                        <td>${_('Thread <a href="%s">#%s</a> (%s replies) posted in %s') % (h.url_for('thread', post=t.id), t.id, t.replyCount, t.tagLine)}</td>
                        <td><a href="${h.url_for('ajShowThread', post=t.id, redirect='userProfile')}">${_('Unhide')}</a></td>
                    </tr>
                    %endfor
            </tbody>
        </table>
    </div>
</form>
<br clear="all" />
