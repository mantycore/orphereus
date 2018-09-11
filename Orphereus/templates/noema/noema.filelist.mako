<%inherit file="noema.management.mako" />

<%include file="noema.paginator.mako" args="routeName='hsFileMod'"/>
<br />
<form method="post" enctype="multipart/form-data" action="${h.url_for('hsFileProcess')}">
<input type="hidden" name="curpage" value="${c.page}">
<table width="100%">
<% cols = 5 %>
%for i in range(len(c.files) / cols):
<tr>
	%for j in range(cols):
		<% 
		file = c.files[i*cols+j] 
		%>
		<td>   
		<input type="checkbox" name="pic-${file.id}" value="${file.id}" /><a href="${h.url_for('hsFileInfo', id=file.id)}">${file.id}</a><br />
		<em><sub>(${'%.2f' % (file.size / 1024.0)} \
            %if file.width and file.height:
                ${_('Kbytes')}, ${file.width}x${file.height})
            %endif
         </em></sub>
                
		## item
		  %if 'image' in file.extension.type:
		      <img src="${g.OPT.filesPathWeb +  file.thumpath}" width="100" class="thumb"  alt="Preview" />
		  %else:
		      <img src="${g.OPT.staticPathWeb +  file.thumpath}" width="100" class="thumb"  alt="Preview" />
		  %endif
		</td>
	%endfor
</tr>
%endfor
</table>

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
<br />
<%include file="noema.paginator.mako" args="routeName='hsFileMod'"/>
