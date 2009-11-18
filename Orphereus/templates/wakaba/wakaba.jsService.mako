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

