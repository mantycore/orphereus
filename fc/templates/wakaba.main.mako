# -*- coding: utf-8 -*-
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
    <head>
        <title>${c.title} - ${c.boardName}</title>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
        <link rel="stylesheet" type="text/css" href="/css/photon.css" title="Photon" />
		<script type="text/javascript"><!--
			function getElementsByClass( searchClass, domNode, tagName) {
				if (domNode == null) domNode = document;
				if (tagName == null) tagName = '*';
				var el = new Array();
				var tags = domNode.getElementsByTagName(tagName);
				var tcl = " "+searchClass+" ";
				for(i=0,j=0; i<tags.length; i++) {
					var test = " " + tags[i].className + " ";
					if (test.indexOf(tcl) != -1)
						el[j++] = tags[i];
				}
				return el;
			}

			function showDeleteBoxes() {
				var chboxes = getElementsByClass('delete');
				for(i=0; i<chboxes.length; i++) {
					if(chboxes[i].style.display == 'none') {
						chboxes[i].style.display = 'inline';
					} else {
						chboxes[i].style.display = 'none';
					}
				}
			}
			-->
		</script>
    </head>
    <body>
        <%include file="wakaba.menu.mako" />
        <%include file="wakaba.logo.mako" />
        <hr />
        ${self.body()}
        <%include file="wakaba.menu.mako" />
        <%include file="wakaba.footer.mako" />
    </body>
</html>
