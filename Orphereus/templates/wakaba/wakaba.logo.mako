<div class="logo">
    %if g.OPT.devMode:
        [DEV]
    %endif
	%if (g.OPT.useFrameLogo and not(c.boardName)):
		<div align="center"><a href="${h.url_for('boardBase', board=g.OPT.defaultBoard)}" target="board"><img src="${g.OPT.staticPathWeb}images/${g.OPT.frameLogo}" alt="${c.title}" /></a></div>
	%endif
	%if not(g.OPT.useFrameLogo and not(c.boardName)):
		${c.title}
		%if c.boardName:
			&mdash; ${c.boardName}
			%if c.page and isinstance(c.page, int):
			  (${c.page})
			%endif
		%endif
	%endif
</div>
