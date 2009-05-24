<html>
<head>
<title>Oekaki drawing process</title>
</head>
<body bgcolor="#CFCFFF" text="#800000" link="#003399" vlink="#808080" alink="#11FF11">
<table cellpadding="0" cellspacing="0" width="100%" style="height: 100%;"><tr><td width="100%">
<applet
 name="pch"
 code="pch2.PCHViewer.class"
 codebase="./"
 archive="${g.OPT.staticPathWeb}pch.jar"
 width="100%"
 height="100%"
>

<param name="pch_file" value="${g.OPT.filesPathWeb + c.pchPath}" />

<param name="tt.zip" value="${g.OPT.staticPathWeb}res/tt.zip" />
<param name="res.zip" value="${g.OPT.staticPathWeb}res/res.zip" />
<param name="speed" value="0" />
<param name="buffer_canvas" value="true" />
<param name="buffer_progress" value="true" />
</applet>
</td></tr></table>

</body>
</html>
