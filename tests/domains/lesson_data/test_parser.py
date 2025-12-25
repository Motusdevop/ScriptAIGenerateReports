"""
Tests for LessonParser domain class
"""

import pytest

from app.domains.lesson_data.parser import LessonParser
from app.domains.lesson_data.interfaces import Child


@pytest.fixture
def parser_fixture(mock_logger):
    return LessonParser(logger=mock_logger)


class TestLessonParser:
    """Tests for LessonParser class"""

    def test_parse_children_with_valid_html(self, parser_fixture):
        """Test parsing children from valid HTML"""
        # Arrange

        # Real HTML would go here
        html = """ 
<a href='lessonjournal.htm?nomenu=1&id=331331' class='w3-btn w3-blue' target='_blank'>Журнал измерения температуры детей</a>


<p>Филиал: Мск - Нестеров, класс: Биб 143<p>Ведущий: Шмаренков Матвей<p><button onclick="checkLeads()" class="w3-btn w3-blue">Изменить ведущего</button><p><script>$("#lessoncomment").val("");</script>Дата занятия: суббота, 20 дек 2025 с 15:00 по 16:30<p><button onclick="document.getElementById('id_comment').style.display='block';" class="w3-btn w3-blue">Комментарий:</button>  <p>Занятие закончено<p><table><tr class="w3-light-grey"><th>Запись на занятие</th><th>Возраст</th><th>Посещение</th><th>Тариф</th><th>Посещаемость</th><th>Школьный класс</th><th></th><th></th><th>Примечания</th><th></th></tr><tr><td><a name="childlist" id="ach90118" href="child.htm?child=90118">Бурман Артём </a></td><td bgcolor=#ffffff>10 лет</td><td bgcolor=#ffffff>Пропуск</td><td>4-Суперноль</td><td>75%</td><td></td><td></td><td></td></tr>
<tr><td><a name="childlist" id="ach91148" href="child.htm?child=91148">Войтов Артём Дмитриевич</a></td><td bgcolor=#009D5C>10 лет</td><td bgcolor=#009D5C>Посетил<br></td><td>4-Суперноль</td><td>84%</td><td></td><td></td><td></td></tr>
<tr><td><a name="childlist" id="ach91279" href="child.htm?child=91279">Гудов Кирилл Русланович</a></td><td bgcolor=#009D5C>8 лет</td><td bgcolor=#009D5C>Посетил<br></td><td>4-Суперноль</td><td>85%</td><td></td><td></td><td></td></tr>
<tr><td><a name="childlist" id="ach85585" href="child.htm?child=85585">Гусейнов Малик </a></td><td bgcolor=#009D5C>10 лет</td><td bgcolor=#009D5C>Посетил<br></td><td>4-Суперноль</td><td>95%</td><td></td><td></td><td></td></tr>
<tr><td><a name="childlist" id="ach90568" href="child.htm?child=90568">Шахмуратов Максим Антонович</a></td><td bgcolor=#009D5C>10 лет</td><td bgcolor=#009D5C>Посетил<br></td><td>4-Суперноль</td><td>93%</td><td></td><td></td><td></td></tr>
</table><h2>Отчет по детям на занятии</h2>
<table><tr style="background-color: #ffffff"><td><table id="reptable1147895" style="border-color: #ddffdd; border-style: solid; width: 100%"><tr style="background-color: #ffffff"><td>Имя</td><td><a href="child.htm?child=91148&branch=193">Войтов Артём</a></td></tr><tr style="background-color: #ffffff"><td>Класс</td><td>Мск - Нестеров, Биб 143, 20.12.2025 15:00</td></tr><tr style="background-color: #ffffff"><td>Ведущий</td><td>Матвей Шмаренков</td></tr><tr style="background-color: #ffffff"><td>Заметки</td><td id="repdescr1147895">Артём осваивал работу с веб-интерфейсами, а также пробовал решать логические задачи. В Scratch он создавал композиции из спрайтов и приступил к персональному проекту, делая симулятор метро с фоном и поездом.</td></tr><tr style="background-color: #ffffff"><td>Замечания для ведущего</td><td id="repnotes1147895"></td></tr><tr style="background-color: #ffffff"><td>Бонусы от ведущего</td><td id="repproject1147895">2 пнг за персональный проект: Делал игру симулятор на HTML метрополитена, молодец!!!<br></td></tr><tr style="background-color: #ffffff"><td>Сделано заданий</td><td><a href="javascript:" onclick="ShowTasks(91148, '2025-12-20', 0, 1147895)" class="BillLink">5</a></td></tr><tr style="background-color: #ffffff"><td>Консультаций</td><td>0</td></tr><tr style="background-color: #ffffff"><td>Скриншоты</td><td>2&nbsp;&nbsp;&nbsp;&nbsp;<button id="repshowscrbtn1147895" onclick="ShowScr(1147895, 91148, 331331);" class="w3-btn w3-blue">Показать</button><div id="scr1147895" style="display: none;"></div></td></tr><tr style="background-color: #ffffff"><td>Заработано</td><td>46 пнг.</td></tr><tr style="background-color: #ffffff"><td>Чистая прибыль</td><td>18 пнг.</td></tr><tr style="background-color: #ffffff"><td>Потрачено</td><td>28 пнг.</td></tr><tr style="background-color: #ffffff"><td>Утвердил</td><td>Дмитрий Нестеров</td></tr><tr style="background-color: #ffffff"><td>Дата утверждения</td><td>Вс, 21.12.2025 22:53 <a href="https://client.softium-deti.ru/client/viewletter.htm?b=193&id=5435095&hash=05c7783246f68610854c5540f4628587" target="_blank">Ссылка на письмо с отчетом</a></td></tr></table></td></tr>

<tr style="background-color: #f2f2f2"><td><table id="reptable1147897" style="border-color: #ddffdd; border-style: solid; width: 100%"><tr style="background-color: #f2f2f2"><td>Имя</td><td><a href="child.htm?child=91279&branch=193">Гудов Кирилл</a></td></tr><tr style="background-color: #f2f2f2"><td>Класс</td><td>Мск - Нестеров, Биб 143, 20.12.2025 15:00</td></tr><tr style="background-color: #f2f2f2"><td>Ведущий</td><td>Матвей Шмаренков</td></tr><tr style="background-color: #f2f2f2"><td>Заметки</td><td id="repdescr1147897">Кирилл настраивал логику перемещения и взаимодействия объектов, проектируя игровую механику в Kodu Game Lab. Он пробовал различные сценарии для создания небольшой игры.</td></tr><tr style="background-color: #f2f2f2"><td>Замечания для ведущего</td><td id="repnotes1147897"></td></tr><tr style="background-color: #f2f2f2"><td>Бонусы от ведущего</td><td id="repproject1147897"></td></tr><tr style="background-color: #f2f2f2"><td>Сделано заданий</td><td><a href="javascript:" onclick="ShowTasks(91279, '2025-12-20', 0, 1147897)" class="BillLink">2</a></td></tr><tr style="background-color: #f2f2f2"><td>Консультаций</td><td>0</td></tr><tr style="background-color: #f2f2f2"><td>Скриншоты</td><td>1&nbsp;&nbsp;&nbsp;&nbsp;<button id="repshowscrbtn1147897" onclick="ShowScr(1147897, 91279, 331331);" class="w3-btn w3-blue">Показать</button><div id="scr1147897" style="display: none;"></div></td></tr><tr style="background-color: #f2f2f2"><td>Заработано</td><td>26 пнг.</td></tr><tr style="background-color: #f2f2f2"><td>Чистая прибыль</td><td>10 пнг.</td></tr><tr style="background-color: #f2f2f2"><td>Потрачено</td><td>17 пнг.</td></tr><tr style="background-color: #f2f2f2"><td>Утвердил</td><td>Дмитрий Нестеров</td></tr><tr style="background-color: #f2f2f2"><td>Дата утверждения</td><td>Вс, 21.12.2025 22:53 <a href="https://client.softium-deti.ru/client/viewletter.htm?b=193&id=5435092&hash=7a9c676f7db925fab889038d2fdac9d8" target="_blank">Ссылка на письмо с отчетом</a></td></tr><tr style="background-color: #f2f2f2"><td>Задание в работе</td><td>Лабиринт. Строим стены</td></tr></table></td></tr>

<tr style="background-color: #ffffff"><td><table id="reptable1147896" style="border-color: #ddffdd; border-style: solid; width: 100%"><tr style="background-color: #ffffff"><td>Имя</td><td><a href="child.htm?child=85585&branch=193">Гусейнов Малик</a></td></tr><tr style="background-color: #ffffff"><td>Класс</td><td>Мск - Нестеров, Биб 143, 20.12.2025 15:00</td></tr><tr style="background-color: #ffffff"><td>Ведущий</td><td>Матвей Шмаренков</td></tr><tr style="background-color: #ffffff"><td>Заметки</td><td id="repdescr1147896">Малик активно работал с электронными таблицами, разбирался в настройках числовых форматов данных и применял различные методы сортировки для упорядочивания информации. Он внимательно подходил к каждому шагу, молодец!</td></tr><tr style="background-color: #ffffff"><td>Замечания для ведущего</td><td id="repnotes1147896"></td></tr><tr style="background-color: #ffffff"><td>Карьера</td><td>Специалист расчeтного центра, бонусов: 7, штрафов: 0 из 3.</td></tr><tr style="background-color: #ffffff"><td>Бонусы от ведущего</td><td id="repproject1147896"></td></tr><tr style="background-color: #ffffff"><td>Сделано заданий</td><td><a href="javascript:" onclick="ShowTasks(85585, '2025-12-20', 0, 1147896)" class="BillLink">2</a></td></tr><tr style="background-color: #ffffff"><td>Консультаций</td><td>1</td></tr><tr style="background-color: #ffffff"><td>Скриншоты</td><td>1&nbsp;&nbsp;&nbsp;&nbsp;<button id="repshowscrbtn1147896" onclick="ShowScr(1147896, 85585, 331331);" class="w3-btn w3-blue">Показать</button><div id="scr1147896" style="display: none;"></div></td></tr><tr style="background-color: #ffffff"><td>Заработано</td><td>19 пнг.</td></tr><tr style="background-color: #ffffff"><td>Чистая прибыль</td><td>7 пнг.</td></tr><tr style="background-color: #ffffff"><td>Потрачено</td><td>12 пнг.</td></tr><tr style="background-color: #ffffff"><td>Утвердил</td><td>Дмитрий Нестеров</td></tr><tr style="background-color: #ffffff"><td>Дата утверждения</td><td>Вс, 21.12.2025 22:53 <a href="https://client.softium-deti.ru/client/viewletter.htm?b=193&id=5435093&hash=ae82be9f90a39ae1cdb5b79e7d42f619" target="_blank">Ссылка на письмо с отчетом</a></td></tr></table></td></tr>

<tr style="background-color: #f2f2f2"><td><table id="reptable1147894" style="border-color: #ddffdd; border-style: solid; width: 100%"><tr style="background-color: #f2f2f2"><td>Имя</td><td><a href="child.htm?child=90568&branch=193">Шахмуратов Максим</a></td></tr><tr style="background-color: #f2f2f2"><td>Класс</td><td>Мск - Нестеров, Биб 143, 20.12.2025 15:00</td></tr><tr style="background-color: #f2f2f2"><td>Ведущий</td><td>Матвей Шмаренков</td></tr><tr style="background-color: #f2f2f2"><td>Заметки</td><td id="repdescr1147894">Максим осваивал взаимодействие с операционной системой, запуская различные приложения и практикуясь с командной строкой. Он также изучал условные операторы в Python и применил эти знания, чтобы создать диспетчер задач, с помощью нейросететей.</td></tr><tr style="background-color: #f2f2f2"><td>Замечания для ведущего</td><td id="repnotes1147894"></td></tr><tr style="background-color: #f2f2f2"><td>Бонусы от ведущего</td><td id="repproject1147894">5 пнг за персональный проект: Практиковался в работе с терминалом windows, молодец!<br></td></tr><tr style="background-color: #f2f2f2"><td>Сделано заданий</td><td><a href="javascript:" onclick="ShowTasks(90568, '2025-12-20', 0, 1147894)" class="BillLink">3</a></td></tr><tr style="background-color: #f2f2f2"><td>Консультаций</td><td>0</td></tr><tr style="background-color: #f2f2f2"><td>Скриншоты</td><td>1&nbsp;&nbsp;&nbsp;&nbsp;<button id="repshowscrbtn1147894" onclick="ShowScr(1147894, 90568, 331331);" class="w3-btn w3-blue">Показать</button><div id="scr1147894" style="display: none;"></div></td></tr><tr style="background-color: #f2f2f2"><td>Заработано</td><td>31 пнг.</td></tr><tr style="background-color: #f2f2f2"><td>Чистая прибыль</td><td>12 пнг.</td></tr><tr style="background-color: #f2f2f2"><td>Потрачено</td><td>19 пнг.</td></tr><tr style="background-color: #f2f2f2"><td>Утвердил</td><td>Дмитрий Нестеров</td></tr><tr style="background-color: #f2f2f2"><td>Дата утверждения</td><td>Вс, 21.12.2025 22:53 <a href="https://client.softium-deti.ru/client/viewletter.htm?b=193&id=5435094&hash=41a1f3d307011dbf0b721456d60e8f49" target="_blank">Ссылка на письмо с отчетом</a></td></tr></table></td></tr>

</table><script>
  SetMessageVars("171316947193d65641ff3f1586614cf2c1ad240b6c661ce43f35869");
</script>
        """

        result = parser_fixture.parse_children(html)

        assert len(result) == 4

        first = result[0]

        assert isinstance(first, Child)
        assert first.name == "Войтов Артём"
        assert first.child_id == 91148
        assert first.lesson_id == "2025-12-20"
        assert first.arepid == 1147895
        assert first.done_tasks_count == 5

    def test_parse_tasks_with_valid_html(self, parser_fixture):
        """Test parsing tasks from valid HTML"""
        # Arrange
        parser = LessonParser(logger=parser_fixture)
        html = "<html>...</html>"  # Real HTML would go here

        ...

        # Act & Assert
        # Add real test implementation based on parser logic
        pass
