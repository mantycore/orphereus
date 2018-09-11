# -*- coding: utf-8 -*-
<%inherit file="noema.main.mako" />

<%include file="noema.lookupList.mako" args="postsList=c.posts" />

<form method="post" enctype="multipart/form-data" action="${h.url_for('hsFileProcess')}">
<input type="hidden" name="pic-${c.pic.id}" value="${c.pic.id}" />
<table class="userdelete">
    <tbody>
			%for tmpl in c.multifileTemplates:
			<tr><td>
        	<%include file="noema.${tmpl}.mako" />
			</tr></td>
			%endfor
    </tbody>
</table>
</form>
              