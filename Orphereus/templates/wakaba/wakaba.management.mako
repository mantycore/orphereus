# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <title>${c.title} - ${_('Holy Synode')} - ${c.boardName}</title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
        <meta name="robots" content="noarchive" />
        <link rel="shortcut icon" type="image/x-icon" href="${g.OPT.staticPathWeb+g.OPT.favicon}" />
        <link rel="stylesheet" type="text/css" href="${h.staticFile(c.userInst.style + ".css")}" title="${c.userInst.style}" />
%for jsFile in c.jsFiles:
        <script type="text/javascript" src="${h.staticFile(jsFile)}"></script>
%endfor
    </head>
    <body>
        %if not c.serviceOut:
		%if g.OPT.useZMenu:
			<%include file="wakaba.z-menu.mako" />
		%else:
            ${c.menuRender}
		%endif
            <%include file="wakaba.logo.mako" />
            <hr />
            <table cellpadding="5" width="100%">
                <tbody>
                    <tr>
                    <td class="adminMenu" style="width: 200px;">
                        <%include file="wakaba.simpleMenu.mako" args="menuId='managementMenu', menuSource=c.builtMenus, currentItemId = c.currentItemId" />
                    </td>
                    <td style="vertical-align: top;">
        %endif
        ${self.body()}
        %if not c.serviceOut:
                    </td>
                    </tr>
                </tbody>
            </table>
            ${c.menuRender}
            <%include file="wakaba.footer.mako" />
        %endif
    </body>
</html>
