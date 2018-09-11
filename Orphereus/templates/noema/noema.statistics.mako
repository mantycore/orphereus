# -*- coding: utf-8 -*-

%if g.OPT.vitalSigns:
<%def name="vital_signs()" cached=${g.OPT.statsCacheTime>0} cache_timeout=${g.OPT.statsCacheTime} cache_type="memory">
    <div id="vitalSigns">
        <h2>Кто имеет ум, тот сочти числа Аномы</h2>
        <table>
            <thead>
                <tr>
                    <td></td>
                    <th>Сейчас</th>
                    <th>До этого</th>
                    <th>Отношение</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <th>Пользователей на 1000 постов</th>
                    <td>${c.last1KUsersCount}</td>
                    <td>${c.prev1KUsersCount}</td>
                    <td>
                        <span class="rate-${c.last1KUsersCount / (c.prev1KUsersCount + 0.01) > 1.0 and "rise" or "fall"}">${'%.2f' % (c.last1KUsersCount / (c.prev1KUsersCount + 0.01))}</span>
                    </td>
                </tr>
                <tr>
                    <th>Постов за неделю</th>
                    <td>${c.lastWeekMessages}</td>
                    <td>${c.prevWeekMessages}</td>
                    <td>
                        <span class="rate-${c.lastWeekMessages / (c.prevWeekMessages + 0.01) > 1.0 and "rise" or "fall"}">${'%.2f' % (c.lastWeekMessages / (c.prevWeekMessages + 0.01))}</span>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</%def>

${vital_signs()}
%endif
