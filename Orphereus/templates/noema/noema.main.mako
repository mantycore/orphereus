# -*- coding: utf-8 -*-

<!DOCTYPE html>

<html>

    <head>
        <title>
        Anoma
        %if c.tagLine:
        / ${c.tagLine}
        %if c.page and isinstance(c.page, int):
          (${c.page})
        %endif
        %endif
        </title>

        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="robots" content="noarchive">
        <link rel="shortcut icon" type="image/x-icon" href="${g.OPT.staticPathWeb+g.OPT.favicon}">
        <link rel="icon" type="image/x-icon" href="${g.OPT.staticPathWeb+g.OPT.favicon}" />
        <link rel="stylesheet" type="text/css" href="${h.staticFile(c.userInst.style + ".css")}" title="${c.userInst.style}">
        <link rel="stylesheet" type="text/css" href="${h.staticFile("highlight.css")}" />
        <style type="text/css">
            body {
                background-image: url('${g.OPT.staticPathWeb}images/noema-texture.png');
            }
        </style>

        %for jsFile in c.jsFiles:
        <script type="text/javascript" src="${h.staticFile(jsFile)}"></script>
        %endfor
        
        <%include file="noema.redirector.mako" />
    </head>
    
    <body>
        <%include file="noema.jsTest.mako" />
        %if not c.suppressMenu:
        <%include file="noema.menu.mako" />
        %endif
        
        %if c.suppressMenu or c.suppressFooter:
        <div id="workspace" class="slim">
        %else:
        <div id="workspace" class="full">
        %endif
        
        %if not c.disableLogo:
        <%include file="noema.logo.mako" />
        %endif
        
        ${self.body()}
        </div>
        
        %if not c.suppressFooter:
        <%include file="noema.footer.mako" />
        %endif
    </body>
    
</html>
