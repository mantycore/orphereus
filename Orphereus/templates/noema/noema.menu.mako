# -*- coding: utf-8; -*-
<div id="topBar">
    <a id="logo" href="/">Anoma</a>
    <ul class="board-links">
        %for tag, title in (('~', u'Обзор'), ('@', u'Связанные треды'), ('*', u'Мои треды'), ('!', u'Главная')):
        <li>
            %if (tag in c.tagLine.split('+')) or (tag == c.board):
            <a title="${title}" href="${h.url_for('boardBase', board=tag)}" class="current-board">
            %else:
            <a title="${title}" href="${h.url_for('boardBase', board=tag)}">
            %endif
            /<span class="board-tag">${tag}</span>/</a>
        </li>
        %endfor
    </ul>
    <ul class="board-links">
        %for tag, title in (('b', u'Бред'), ('d', u'Обсуждение сайта'), ('mu', u'Музыка'), ('dg', u'Разговоры'), ('s', u'Программы'), (u'Ψ', u'Психология'), ('vg', u'Видеоигры'), ('p', u'Политика')):
        <li>
            %if (tag in c.tagLine.split('+')) or (tag == c.board):
            <a title="${title}" href="${h.url_for('boardBase', board=tag)}" class="current-board">
            %else:
            <a title="${title}" href="${h.url_for('boardBase', board=tag)}">
            %endif
            /<span class="board-tag">${tag}</span>/</a>
        </li>
        %endfor
    </ul>
    <ul>
        <li><a href="${h.url_for('userProfile')}">профиль</a></li>
    </ul>
    <ul>
        <li><a href="${h.url_for('logout')}">выход</a></li>
    </ul>
</div>
