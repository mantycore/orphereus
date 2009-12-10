# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <title>${c.title} - ${_('Maintenance panel')} - ${c.boardName}</title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
        <link rel="stylesheet" type="text/css" href="${h.staticFile("photon.css")}" title="Photon" />
%for jsFile in c.jsFiles:
        <script type="text/javascript" src="${h.staticFile(jsFile)}"></script>
%endfor
    </head>
    <body>
        ${c.renderedTopMenu}
        <%include file="wakaba.logo.mako" />
        <hr />
        <table cellpadding=5 width="100%">
            <tbody>
                <tr>
                <td class="adminMenu" width="200px;">
                    <%include file="wakaba.managementMenu.mako" />
                </td>
                <td>
                    ${self.body()}
                </td>
                </tr>
            </tbody>
        </table>
        ${c.renderedBottomMenu}
        <%include file="wakaba.footer.mako" />
    </body>
</html>
