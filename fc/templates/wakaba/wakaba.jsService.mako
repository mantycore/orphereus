<script type="text/javascript">
 $(YForm.init)
window.loading_icon_path = "${g.OPT.staticPathWeb}images/loading.gif"
%if c.userInst.useAjax():
    popup_posts({ajax: true,
                 loading_icon_path: "${g.OPT.staticPathWeb}images/loading.gif"
               });
%endif
%if c.userInst.expandImages():
    click_expands({max_width: ${c.userInst.maxExpandWidth()},
                   max_height: ${c.userInst.maxExpandHeight()},
                   loading_icon_path: "${g.OPT.staticPathWeb}images/loading.gif"
                   });
%endif
$(expandable_threads)
</script>

