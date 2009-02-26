<script type="text/javascript">
%if c.userInst.useAjax():
    popup_posts({ajax: true});
%endif
%if c.userInst.expandImages():
    click_expands({max_width: ${c.userInst.maxExpandWidth()},
                   max_height: ${c.userInst.maxExpandHeight()},
                   loading_icon_path: "${g.OPT.staticPathWeb}images/loading.gif"
                   });
%endif
</script>
