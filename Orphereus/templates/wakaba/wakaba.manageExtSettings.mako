# -*- coding: utf-8 -*-
<%inherit file="wakaba.management.mako" />

<script>
var sections = [${', '.join(map(lambda str: "'%s'" %str,c.cfg.iterkeys()))}, 'settingsDump'];
var active = 'lolz';
function showSect(sect) {
if (sect != active) {
	$('#'+active).slideToggle('fast');
	$('#'+sect).slideToggle('fast');
	}
active = sect;
}
function resetPrompt() {
if (confirm('${_("This will delete ALL configuration data drom the database. Continue?")}')) 
	{ window.location='${h.url_for('hsCfgReset')}'; }
}
</script>

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
    <table width="100%">
    	<tbody>
    		<tr>
				<td width="150px" valign="top">
				%for sect in sorted(c.cfg.iterkeys()):
				<div class="theader"><a style="cursor:pointer; display: block;" onclick="showSect('${sect}');">${sect}</a></div>
				%endfor
				<hr />
				<div class="theader"><a style="cursor:pointer; display: block;" onclick="resetPrompt();">${_("Reset settings")}</a></div>
				<div class="theader"><a style="cursor:pointer; display: block;" onclick="showSect('settingsDump');">${_("Dump settings")}</a></div>
				</td>    	
				<td valign="top">
<div class="postarea">
	<form id="postform" method="post" action="${h.url_for('hsCfgManage')}">					
	%for (sect, settings) in c.cfg.iteritems():
	<div id="${sect}" style="display:none" align="center">
        <table width="70%">
            <tbody>
				<td colspan=2>
					<h2>${sect}</h2>
				</td>
                %for (key,val) in sorted(settings.iteritems()):
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
${'\r\n'.join(val.split(','))}
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
<div id="settingsDump" style="display:none" align="center">
<textarea style="overflow-x: scroll; overflow-y: scroll;" rows="20" cols="80">
${'\r\n'.join(sorted(map(lambda (key,val): "%s = %s" %(key,val),c.allSettings.iteritems())))}
</textarea>
<br /><i>${_('(pastable into .ini file)')}</i>
</div>
				</td>
    		</tr>
    	</tbody>
    </table>
<script>showSect(sections[0]);</script>