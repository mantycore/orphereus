%if c.currentUserCanPost:
<div class="y_replyform" style="display:none">
<form action="/1" method="post" enctype="multipart/form-data" id="y_replyform" class="y_replyform_anon">
    <div class="hidden">
    <input type="hidden" name="task" value="post" />
    <input type="hidden" name="title" value="" />
    <input type="hidden" name="tagLine" value="b" />
    <input type="hidden" name="curPage" value="0" />
    </div>
    <div><textarea id="y_replyform_text" name="message" rows="5" cols="40" tabindex="10"></textarea></div>

    <div class="y_replyform_fields">
        <p id="y_replyform_captcha">
            <label for="y_replyform_captcha_field">
                <img width="150" height="40" alt="${_("Captcha")}" src="${g.OPT.staticPathWeb}images/placeholder.png"  onclick="update_captcha(this)"/>
            </label>
            <input type="text" size="35" name="captcha" id="y_replyform_captcha_field" class="inactive" value="${_('Captcha required')}" title="${_("Captcha text")}" tabindex="20"/>
            <input type="password" value="_" size="35" name="remPass" id="y_replyform_password" title="${_("You can use this password to remove posts")}"/>
        </p>

        %if c.boardOptions.images:
        <p id="y_replyform_file">
        <input type="file" id="y_replyform_file_field" name="file_0" size="10" tabindex="40" class="y_fileField" onchange="YFormMarkSelected(0);" />

        %if c.boardOptions.allowedAdditionalFiles:
          %for idx in range(1, c.boardOptions.allowedAdditionalFiles):
            <input type="file" style="display: none;" id="y_replyform_file_field_${idx}" name="file_${idx}" size="10" tabindex="40" class="y_fileField"  onchange="YFormMarkSelected(${idx});" />
          %endfor
        %endif
        %if c.boardOptions.allowedAdditionalFiles:
          <span class="filesize">[
          <a id="y_replyform_file_link_0" onclick="YFormActivateFile(0);" class="y_fileLink y_fileLinkActive">1</a>
          %for idx in range(1, c.boardOptions.allowedAdditionalFiles):
            <a id="y_replyform_file_link_${idx}" onclick="YFormActivateFile(${idx});" class="y_fileLink">${idx+1}</a>
          %endfor
          ]</span>
        %endif

        </p>
        %endif

        <p id="y_replyform_sage">
            <label for="y_replyform_sage_field" title="sage">
                <input type="checkbox" id="y_replyform_sage_field" name="sage" tabindex="50"/>${_("sage")}
            </label>
        </p>
        <p id="y_replyform_goto">
            <label for="y_replyform_goto_field" title="goto">${_('Go to')}</label>
            <select name="goto" id="y_replyform_goto_field"  tabindex="60">
                <option value="0">Thread</option>
                <option value="1">First page of current board</option>
                <option value="2">Current page of current board</option>
                <option value="3">Overview</option>
                <option value="4">First page of destination board</option>
                <option value="5">Referrer</option>
            </select>
        </p>
        <p id="y_replyform_buttons"><input type="submit" value="${_('Post')}" tabindex="30"/><input type="button" value="${_('Close')}" class="close" /></p>
    </div>
    <div class="clear"></div>
</form>
<div class="clear"></div>
</div>

<table style="display: none" id="dummyTable">
<tr id="trfile_">
    <td class="postblock">${_('File')}</td>
    <td>
      <input type="file" name="file_" size="35" onchange="addFileRowOnChange(this);" />
%if c.boardOptions.enableSpoilers:
      <span class="tspoiler">&nbsp; <input type="checkbox" name="spoiler_" /> ${_('Spoiler')}</span>
%endif
      <input name="removeRowBtn" type="button" value="${_("Remove")}" onclick="removeRow(this);" />
      <input type="hidden" name="fileRowId" value="" />
    </td>
</tr>
</table>
%endif

<script type="text/javascript">
 $(YForm.init);
window.loading_icon_path = "${g.OPT.staticPathWeb}images/loading.gif";
%if c.userInst.useAjax:
popup_posts({ajax: true,
             loading_icon_path: "${g.OPT.staticPathWeb}images/loading.gif"
           });
%endif
%if c.userInst.expandImages:
click_expands({max_width: ${c.userInst.maxExpandWidth},
               max_height: ${c.userInst.maxExpandHeight},
               loading_icon_path: "${g.OPT.staticPathWeb}images/loading.gif"
               });
%endif
$(expandable_threads);

resetRow("#createdRows", "value", 0);
resetRow("#nextRowId", "value", 0);
resetRow("#addFileBtn", "disabled", "");

%if False:
/*$("#oekakiPreview").hide();*/
%endif

%if g.OPT.memcachedPosts and not(c.userInst.isAdmin()) and c.userPostsToHighlight:
function highlightMyPosts(){
  var myPosts=new Array(${','.join(['"#reply%d"' % x for x in c.userPostsToHighlight])});
  for (var i = 0; i < myPosts.length; i++){
     $(myPosts[i]).addClass("myreply");
  }
}
highlightMyPosts();
%endif
</script>

