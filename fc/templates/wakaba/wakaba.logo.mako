<div class="logo">
    %if g.OPT.devMode:
        [DEV]
    %endif
	${c.title}
	%if c.boardName:
		&#151; ${c.boardName}
	%endif
</div>
