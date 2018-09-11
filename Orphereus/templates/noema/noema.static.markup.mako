# -*- coding: utf-8 -*-
<%inherit file="noema.main.mako" />

<!-- ${_("markup")} -->

<div style="text-align: center;">
<h2 style="margin: 0;">Orphie-Mark</h2>
<h3 style="margin: 0;"><i>(Разметка)</i></h3>
<h4 style="margin: 0;">Внутри строк</h4>
</div>
<table width="80%" class="hlTable" align="center">
    <thead>
        <tr>
            <td style="width:50%;"><b>Входит</b></td>
            <td style="width:50%;"><b>Выходит</b></td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left">*курсивная надпись*</td>
            <td align="left"><em>курсивная надпись</em></td>
        </tr>
        <tr>
            <td align="left">**полужирный текст**</td>
            <td align="left"><strong>полужирный текст</strong></td>
        </tr>
        <tr>
            <td align="left">__подчеркнутый текст__</td>
            <td align="left"><span style="text-decoration: underline;">подчеркнутый текст</span></td>
        </tr>
        <tr>
            <td align="left">$$перечеркнутый текст$$</td>
            <td align="left"><span style="text-decoration: line-through">перечеркнутый текст</span></td>
        </tr>
        <tr>
            <td align="left">``код``</td>
            <td align="left"><pre>код</pre></td>
        </tr>
        <tr>
            <td align="left">>>номер</td>
            <td align="left">ссылка на пост</td>
        </tr>
        <tr>
            <td align="left">##номер1 или ##номер1,номер2,...</td>
            <td align="left">Подпись, она же пруфметка.<br/><br/>
            <div style="font-size: 90%">
            <b>Пример использования:</b> <br/>
            Допустим, вы написали посты с номерами 10 и 20, а посты с номерами 40 и 50 написаны другим человеком.<br/>
            В таком случае написав <br/>
            <code>##10,20,40,50</code> <br/>
            вы получите на выходе<br/>

            <p>
            <span class="badsignature">##<a href="#">40</a>,<a href="#">50</a></span>,<span class="signature"><a href="#">10</a>,<a href="#">20</a></span>
            </p>

            <br/>
            Если же авторство поста нельзя ни подтвердить, ни опровергнуть (т.е. если он был анонимизирован, либо оставлен незарегистрированным пользователем),
            то вы получите на выходе нечто вроде
            <p>
            <span class="nonsignature">##<a href="#">40</a></span>
            </p>

            </div>
            </td>
        </tr>
        <tr>
            <td align="left">%%спойлер%%</td>
            <td align="left"><span class="spoiler">спойлер</span></td>
        </tr>
    </tbody>
</table>
<div style="text-align: center;">
<h4 style="margin: 0;">Блоки</h4>
</div>
<table width="80%" class="hlTable" align="center">
    <thead>
        <tr>
            <td style="width:50%;"><b>Входит</b></td>
            <td style="width:50%;"><b>Выходит</b></td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left">**<br/>полужирный<br/>блок<br/>**</td>
            <td align="left">
                <div style="font-weight: bold;">
                <p><br/>полужирный<br/>блок<br/></p>
                </div>
            </td>
        </tr>
        <tr>
            <td align="left">*<br/>курсивный<br/>блок<br/>*</td>
            <td align="left">
                <div style="font-style: italic;">
                <p>курсивный<br/>блок</p>
                </div>
            </td>
        </tr>
        <tr>
            <td align="left">__<br/>подчеркнутый<br/>блок<br/>__</td>
            <td align="left">
                <div style="text-decoration: underline;">
                <p>подчеркнутый<br/>блок</p>
                </div>
            </td>
        </tr>
        <tr>
            <td align="left">$$<br/>перечеркнутый<br/>блок<br/>$$</td>
            <td align="left">
                <div style="text-decoration: line-through;">
                <p>перечеркнутый<br/>блок</p>
                </div>
            </td>
        </tr>
        <tr>
            <td align="left">%%<br/>блок<br/>спойлера<br/>%%</td>
            <td align="left">
                <div class="spoiler">
                <p>блок<br/>спойлера</p>
                </div>
            </td>
        </tr>
        <tr>
            <td align="left">\***<br/>строка<br/>текст<br/>\***</td>
            <td align="left"><ul><li>строка</li><li>текст</li></ul></td>
        </tr>
    <tr>
            <td align="left">\123<br/>строка<br/>текст<br/>\123</td>
            <td align="left"><ol><li>строка</li><li>текст</li></ol></td>
        </tr>
        <tr>
            <td align="left">&gt; текст<br/>или<br/>&gt;&gt; текст</td>
            <td align="left">
                <blockquote class="postbody">
                    <blockquote> &gt; текст
                    </blockquote>
                    или
                    <blockquote>
                    <blockquote>&gt; &gt; текст</blockquote>
                    </blockquote>

                </blockquote>
            </td>
        </tr>
        <tr>
            <td align="left">``<br/>блок<br/>кода<br/>``</td>
            <td align="left"><pre>блок<br/>кода</pre></td>
        </tr>
        <tr>
            <td align="left">``=python<br/>блок кода с подсветкой<br/>``</td>
            <td align="left"><pre>блок кода с подсветкой</pre>
            </td>
        </tr>
  </tbody>
</table>
<div style="text-align: center;">
<h4 style="margin: 0;">Символы</h4>
</div>
<table width="80%" class="hlTable" align="center">
    <thead>
        <tr>
            <td style="width:50%;"><b>Входит</b></td>
            <td style="width:50%;"><b>Выходит</b></td>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left">&amp;#число;<br/>&amp;#265;</td>
            <td align="left">HTML-символ с кодом "число"<br/>&#265;</td>
        </tr>
        <tr>
            <td align="left">&amp;название;<br/>&amp;quot;</td>
            <td align="left">HTML-символ с названием "название"<br/>&quot;</td>
        </tr>
        <tr>
            <td align="left">-</td>
            <td align="left">-</td>
        </tr>
        <tr>
            <td align="left">--</td>
            <td align="left">—</td>
        </tr>
        <tr>
            <td align="left">(c)</td>
            <td align="left">&copy;</td>
        </tr>
        <tr>
            <td align="left">(tm)</td>
            <td align="left">&#153;</td>
        </tr>
        <tr>
            <td align="left">...</td>
            <td align="left">&#133;</td>
        </tr>
    </tbody>
</table>


<h2 style="margin: 0; text-align: center;">Особенности Orphereus</h2>
<ol>
<li>Каждый тред может принадлежать нескольким доскам.</li>
<li>IP адреса зарегистрированных пользователей по умолчанию нигде не хранятся.</li>
<li>Наличествует такая возможность, как <a href="${h.url_for('static', page='finalAnonymity')}">Окончательная Анонимизация</a>.</li>
</ol>



<h3 style="text-align: center;">О досках и плотницком деле</h3>
На чане нет жестко закрепленной системы досок.
Каждому треду может соответствовать несколько <i>тэгов</i>, которые перечисляются в поле boards при создании треда.
Те тэги, список которых вы видите наверху каждой страницы - это и есть доски в обычном значении этого слова.
Любой популярный тэг может стать доской.
<i>Доска — это тэг, который понравился бородатым админам и был закреплен в верхнем меню.</i> Поэтому <b>обязательно пользуйтесь тэгами</b>!

<h3 style="text-align: center;">Фильтры</h3>
Есть возможность не только постить в несколько досок &mdash; можно еще и просматривать посты из разных досок. Для этого
введите в адресной строке браузера адрес вида <a href="${h.url_for('boardBase', board='b+d+a')}">http://${g.OPT.baseDomain}/b+d+a</a>. Вам будут показаны все треды из
досок /b/, /d/ и /a/. Если вы введете адрес вида <a href="${h.url_for('boardBase', board='b+d+a-drugs')}">http://${g.OPT.baseDomain}/b+d+a-drugs</a>, то вы увидите все треды
из /b/, /d/ и /a/ кроме тех, которые размещены еще и на доске /drugs/. Несколько досок, таким образом соединенных в одну, называются <i>фильтрами</i>.
<br/>
Также есть три специальных фильтра:
<ol>
<li><b>/~/</b> — все треды изо всех досок. В своем <a href="${h.url_for('userProfile')}">профиле</a> вы можете перечислить через запятую те тэги, которые вы не хотите видеть в /~/ (пункт Home filter exclusions);</li>
<li><b>/@/</b> — все треды, в которых есть ваши сообщения;</li>
<li><b>/*/</b> — все ваши треды.</li>
</ol>

Вы можете добавить часто используемые фильтры в свой профиль (пункт User Filters) - тогда под списком досок появится еще одна строка с вашими личными фильтрами.<br />
Особая страница <b>/!/</b> — это список досок и тэгов, статистическая информация и прочее.
<br /><br />
По умолчанию вы видите на каждой странице один из старых тредов (время постинга подсвечивается красным). Эту
возможность можно отключить в профиле.
<h3 style="text-align: center;">Операции, используемые в фильтрах</h3>
<ol>
<li><b>+</b> — объединение множеств. A+B выдает все треды из /A/, /B/ и размещенные на обоих досках</li>
<li><b>-</b> — вычитание множеств. A-B выдает все треды из  /A/, которые <i>не</i> являются кросспостами в /B/</li>
<li><b>&amp;</b> — пересечение множеств. A&amp;B выдает все треды из /A/, которые являются кросспостами в /B/</li>
</ol>

<h3 style="text-align: center;">Поиск и фильтры</h3>
<a name="search"></a>
<p>Если поисковый запрос содержит знак двоеточия, то стоящий до двоеточия текст рассматривается как фильтр, внутри
которого должен происходить поиск. Например, если в поле поиска вписать <i>b+d:поисковый_запрос</i>,
то будут найдены все посты, удовлетворяющие "<i>поисковому_запросу</i>" из досок <b>/b/</b> и <b>/d/</b><br/>
В противном случае осуществляется поиск всех постов, удовлетворяющих запросу (аналогично <i>~:поисковый_запрос</i>)</p>
<p>
%if g.OPT.searchPluginId == 'search_sphinx':
В данный момент разрешен полнотекстовый поиск. Информацию о синтаксисе поисковых запросов можно
получить <a href="http://www.sphinxsearch.com/docs/current.html#extended-syntax">здесь</a>
%else:
В данный момент полнотекстовый поиск отключен, поиск производится по подстроке.
%endif
</p>

<div style="text-align: center;">
<h4 style="margin: 0;">Поддерживаемые языки подсветки</h4>
</div>
<table width="80%" class="hlTable" align="center">
    <thead>
        <tr>
            <td style="width:50%;"><b>Название</b></td>
            <td style="width:50%;"><b>Язык</b></td>
        </tr>
    </thead>
    <tbody>
      <tr><td align="left">lua</td><td align="left">Lua</td></tr>
      <tr><td align="left">perl</td><td align="left">Perl</td></tr>
      <tr><td align="left">python</td><td align="left">Python</td></tr>
      <tr><td align="left">python3</td><td align="left">Python 3000</td></tr>
      <tr><td align="left">ruby</td><td align="left">Ruby</td></tr>
      <tr><td align="left">tcl</td><td align="left">TCL</td></tr>
      <tr><td align="left">c</td><td align="left">C</td></tr>
      <tr><td align="left">cpp</td><td align="left">C++</td></tr>
      <tr><td align="left">d</td><td align="left">D</td></tr>
      <tr><td align="left">delphi</td><td align="left">Delphi</td></tr>
      <tr><td align="left">fortran</td><td align="left">Fortran</td></tr>
      <tr><td align="left">java</td><td align="left">Java</td></tr>
      <tr><td align="left">objectivec</td><td align="left">Objective C</td></tr>
      <tr><td align="left">scala</td><td align="left">Scala</td></tr>
      <tr><td align="left">csharp</td><td align="left">C#</td></tr>
      <tr><td align="left">vbnet</td><td align="left">VB.Net</td></tr>
      <tr><td align="left">clisp</td><td align="left">Common LISP</td></tr>
      <tr><td align="left">erlang</td><td align="left">Erlang</td></tr>
      <tr><td align="left">haskell</td><td align="left">Haskell</td></tr>
      <tr><td align="left">ocaml</td><td align="left">Ocaml</td></tr>
      <tr><td align="left">scheme</td><td align="left">Scheme</td></tr>
      <tr><td align="left">bash</td><td align="left">Bash</td></tr>
      <tr><td align="left">mysql</td><td align="left">MySQL</td></tr>
      <tr><td align="left">sql</td><td align="left">SQL</td></tr>
      <tr><td align="left">ini</td><td align="left">Ini files</td></tr>
      <tr><td align="left">tex</td><td align="left">Tex</td></tr>
      <tr><td align="left">html</td><td align="left">HTML</td></tr>
      <tr><td align="left">js</td><td align="left">JavaScript</td></tr>
      <tr><td align="left">php</td><td align="left">PHP</td></tr>
      <tr><td align="left">xml</td><td align="left">XML</td></tr>
    </tbody>
</table>

<hr />
