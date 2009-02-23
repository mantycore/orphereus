# -*- coding: utf-8 -*-
<%inherit file="wakaba.admin.mako" />

<div class="postarea">
    <form id="postform" method="post">
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
                %for s in g.settingsMap:
                <tr>
                    <td class="postblock">${c.settingsDescription[g.settingsMap[s].name][0]}</td>
                    <td>
                        %if c.settingsDescription[g.settingsMap[s].name][1] == bool:
                        <select name="${g.settingsMap[s].name}">
                               <option value="true"
                                 %if g.settingsMap[s].value == "true":
                                    selected
                                 %endif
                               >
                               True
                              </option>
                               <option value="false"
                                 %if g.settingsMap[s].value != "true":
                                    selected
                                 %endif
                               >
                               False
                              </option>
                        </select>
                        %else:
                            <input type="text" name="${g.settingsMap[s].name}" size="35" value="${g.settingsMap[s].value}" />
                        %endif
                    </td>
                </tr>
                %endfor
                <tr>
                    <td colspan='2'>
                        <input type="submit" name="update" value="${_('Update')}"
                          %if not c.userInst.canChangeSettings():
                            disabled
                          %endif
                        >
                    </td>
                </tr>
            </tbody>
        </table>
    </form>
</div>
