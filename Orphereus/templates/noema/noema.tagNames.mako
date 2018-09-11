<table class="hlTable">
<tr>
<td>
<b>${_("Tag")}</b>
</td>
<td>
<b>${_("Description")}</b>
</td>
</tr>

%for id,tag in enumerate(c.tags):
<tr>
<td>
/${tag}/
</td>
<td>
<input type="text" name="tagdef_${id}" size="35" />
<input type="hidden" name="tagname_${id}" value="${tag}" />
</td>
</tr>
%endfor
</table>