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

var createdRowsField = $("#createdRows");
if (createdRowsField){
  createdRowsField.attr("value", 0);
}
var nextRowIdField = $("#nextRowId");
if (nextRowIdField){
  nextRowIdField.attr("value", 0);
}
var addFileBtn = $("#addFileBtn");
if (addFileBtn){
addFileBtn.attr("disabled", "");
}

</script>

