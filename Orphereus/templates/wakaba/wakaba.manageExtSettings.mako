# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

%if c.message:
    <table>
    <tr id="trmessage">
        <td colspan=2>
            <span class="theader">
                ${c.message}
            </span>
        </td>
    </tr>
    </table>
%endif
<input type="button" 
onclick="if (prompt('This will delete ALL configuration data drom the database. Continue?\n(Type \'yes\' to agree.)')=='yes') { window.location='${h.url_for('hsCfgReset')}'; }" value="Reset settings" />
<div class="postarea">
    <form id="postform" method="post" action="${h.url_for('hsCfgManage')}">
	%for (sect, settings) in c.cfg.iteritems():
	<div class="theader"><a style="cursor:pointer; display: block;" onclick="toggle_div('${sect}');">${sect}</a></div>
	<div id="${sect}" style="display:none">
        <table>
            <tbody>
			<!---- <tr>
				<td colspan=2>
					<p align="center"><span class="theader">${sect}</span></p>
				</td>
			</tr> ---->
                %for (key,val) in settings.iteritems():
                <tr>
                    <td class="postblock">${key}</td>
                    <td>
                        %if g.OPT.getValueType(key) == 0x01:
                        <select name="${sect}.${key}">
                               <option value="true"
                                 %if val == "true":
                                    selected="selected"
                                 %endif
                               >
                               True
                              </option>
                               <option value="false"
                                 %if val != "true":
                                    selected="selected"
                                 %endif
                               >
                               False
                              </option>
                        </select>
                        %elif g.OPT.getValueType(key) == 0x08:
<textarea style="overflow-x: scroll; overflow-y: scroll;" rows="5" cols="35" name="${sect}.${key}">
%for line in val.split(','):
${line}
%endfor
</textarea>
                        %else:
                            <input type="text" name="${sect}.${key}" size="40" value="${val}" />
                        %endif
                    </td>
                </tr>
                %endfor
                <tr>
                    <td colspan='2'>
                        <p align="center">
                        <input type="submit" name="update" value="${_('Update')}"
                          %if not c.userInst.canChangeSettings():
                            disabled="disabled"
                          %endif
                        />
                        <br /><br />
                        </p>
                    </td>
                </tr>
            </tbody>
        </table>
     </div>
    %endfor    
    </form>
</div>
