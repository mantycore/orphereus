# -*- coding: utf-8 -*-
<%page args="userFilter"/>
<tr id="filterId${userFilter.id}">
    <td><input id="filterId${userFilter.id}Input" name="filterId${userFilter.id}" value="${userFilter.filter}" /></td>
    <td class="postblock">[<a id="changeLinkId${userFilter.id}" href="" onclick="userFiltersEdit(event,${userFilter.id});">${_("Change")}</a>] [<a href="" onclick="userFiltersDelete(event,${userFilter.id});">${_("Del")}</a>]</td>
</tr>