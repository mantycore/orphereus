# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <title>${c.title} - ${_('Holy Synode')} - ${c.boardName}</title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
        <meta name="robots" content="noarchive" />
        <link rel="shortcut icon" type="image/x-icon" href="/favicon.ico" />
        <link rel="stylesheet" type="text/css" href="${h.staticFile(c.userInst.style() + ".css")}" title="${c.userInst.style()}" />
        <script type="text/javascript" src="${h.staticFile("jquery.js")}"></script>
        <script type="text/javascript" src="${h.staticFile("ui.js")}"></script>
    </head>
    <body>
        %if not c.serviceOut:
            <%include file="wakaba.menu.mako" />
            <%include file="wakaba.logo.mako" />
            <hr />
            <table cellpadding="5" width="100%">
                <tbody>
                    <tr>
                    <td class="adminMenu" style="width: 200px;">
                        <%include file="wakaba.managementMenu.mako" />
                    </td>
                    <td style="vertical-align: top;">
        %endif
        ${self.body()}
        %if not c.serviceOut:
                    </td>
                    </tr>
                </tbody>
            </table>
            <%include file="wakaba.menu.mako" />
            <%include file="wakaba.footer.mako" />
        %endif
    </body>
</html>
