<%inherit file="wakaba.main.mako" />

<script type="text/javascript">
    parent.top.list.location.reload(true);
    parent.top.board.window.location="${c.currentURL}";
</script>

<div class="theader">
<h1>${_('Successfully logged in')}</h1>
<h2><a href="${c.currentURL}">Continue</a></h2>
</div>
