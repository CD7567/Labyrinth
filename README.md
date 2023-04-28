# Генератор лабиринтов

## Описание

На данном этапе проект представлен интерактивной консолью генератора лабиринтов.

Команды интерактивной консоли:

- `generate {width} {height} {name} [algorithm name]` - генерация лабиринта
- `show` - вывести лабиринт в консоль
- `solve` - найти решение и вывести в консоль решенную версию данного лабиринта
- `focus` - вывести имя текущего активного лабиринта
- `list` - вывести список сохраненных лабиринтов
- `save` -  сохранить лабиринт в формате `csv`
- `load` - загрузить лабиринт из файла сохранения
- `configure` - изменить конфигурацию (визуальный стиль)
- `exit` - покинуть консоль

Консоль реализована с помощью встроенного пакета `Cmd`, потому является удобным и стабильным инструментом взаимодействия с алгоритмами программы.

На данный момент реализованы алгоритмы `(algorithm name)`:
- `'dfs'` - поиск в глубину
- `'wilson'` - алгоритм Уилсона
- `'prim'` - алгоритм Прима

## Кастомизация интерактивной консоли

Пакет стилей располагается в файле `conf/styles.json`.
Кастомизация выполняется при помощи файла конфигурации `conf/conf.json` или команды `configure` интерактивной консоли.

Возможно настроить:

- Вид оформления стенок `border` лабиринта
- Вид оформления пути-решения `path` лабиринта
- Символ старта `entry` лабиринта
- Символ финиша `finish` лабиринта
- Цвет стенок `border` лабиринта
- Цвет пути-решения `path` лабиринта