<html>
<head>
<title>Shi-Painter</title>
<script language="javascript" type="text/javascript" src="${g.OPT.filesPathWeb}../sp.js"></script>
</head>
<body>
<applet code="c.ShiPainter.class" name="paintbbs" archive="${g.OPT.filesPathWeb}../spainter.jar,/res/${c.oekakiToolString}.zip" WIDTH="100%" height="90%" MAYSCRIPT>
<param name="image_width" value="${c.width}">
<param name="image_height" value="${c.height}">
%if c.canvas:
  <param name="image_canvas" value="${g.OPT.filesPathWeb + c.canvas}" />
%endif

<param name="image_size" value="200" />
<param name="compress_level" value="15" />
<param name="url_save" value="/${c.url}/oekakiSave/${c.tempid}" />
<param name="url_exit" value="/${c.url}/${c.tempid}" />

<param name="send_header_image_type" value="true" />
<param name="send_header_timer" value="true" />


<param name="dir_resource" value="/res/">
<param name="tt.zip" value="/res/tt.zip">

<param name="res.zip" value="/res/res_${c.oekakiToolString}.zip">
<param name="tools" value="${c.oekakiToolString}">

<param name="layer_count" value="3">
<param name="quality" value="1">

<param name="undo_in_mg" value="15">
<param name="undo" value="30">
<param name="MAYSCRIPT" value="true">
<param name="scriptable" value="true">


<param name="color_text" value="0">
<param name="color_bk" value="#FFFF0">
<param name="color_bk2" value="#FF00FF">
<param name="color_icon" value="#0FFFF">
<param name="color_frame" value="0xff">

<param name="color_iconselect" value="#112233">
<param name="color_bar" value="0">
<param name="color_bar_hl" value="#665544">
<param name="color_bar_shadow" value="#778899"> 

<param name="tool_color_bk" value="#aabbcc">
<param name="tool_color_button" value="#ddeeff">
<param name="tool_color_button_hl" value="#9900ff">
<param name="tool_color_button_dk" value="#ff0099">

<param name="tool_color_button2" value="#ffffff">
<param name="tool_color_text" value="0">
<param name="tool_color_bar" value="#00ff00">
<param name="tool_color_frame" value="#ff0000">



<param name=pro_menu_color_text value="#FFFFFF">
<param name=pro_menu_color_off value="#222233">
<param name=pro_menu_color_off_hl value="#333344">
<param name=pro_menu_color_off_dk value="0">
<param name=pro_menu_color_on value="#ff0000">
<param name=pro_menu_color_on_hl value="#ff8888">
<param name=pro_menu_color_on_dk value="#660000">

<param name=bar_color_bk value="#ffffff">
<param name=bar_color_frame value="#ffffff">
<param name=bar_color_off value="#ffffff">
<param name=bar_color_off_hl value="#ffffff">
<param name=bar_color_off_dk value="#ffffff">
<param name=bar_color_on value="#777777">
<param name=bar_color_on_hl value="#ffffff">
<param name=bar_color_on_dk value="#ffffff">
<param name=bar_color_text value="0">

<param name="window_color_text" value="#ff0000">
<param name="window_color_frame" value="#ffff00">
<param name="window_color_bk" value="#000000">
<param name="window_color_bar" value="#777777">
<param name="window_color_bar_hl" value="#888888">
<param name="window_color_bar_text" value="#000000">

<param name="dlg_color_bk" value="#ccccff">
<param name="dlg_color_text" value="0">

<param name=color_bk value="#ccccff">
<param name=color_bk2 value="#f0f0f0">

<param name=l_m_color value="#ffffff">
<param name=l_m_color_text value="#0000ff">
</applet>



</body>
</html>
