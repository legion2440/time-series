# time-series

Учебный проект по работе с временными рядами на Python.

В проекте реализованы упражнения `ex00`-`ex04` с использованием `pandas`, `numpy` и `plotly`. В качестве исходных данных используется файл `data/AAPL.txt` с историческими котировками Apple.

## Что сделано

### ex00 - проверка окружения
- подготовлен `requirements.txt`
- добавлен `check_env.py` для проверки версии Python и наличия библиотек
- проверяются: `pandas`, `numpy`, `jupyter`, `plotly`

### ex01 - базовый временной ряд и rolling average
- строится `Series` с датами от `2010-01-01` до `2020-12-31`
- значения начинаются с `0` и растут на `1` каждый день
- рассчитывается `7-day moving average` через `rolling().mean()`
- решение сделано без `for`

### ex02 - preprocessing, resample, candlestick, returns
- читается файл `data/AAPL.txt`
- обрабатываются пропуски
- колонка `Date` переводится в `datetime`
- `Date` становится индексом
- данные сортируются по дате
- выполняется первичный анализ через `info()` и `describe()`
- строится candlestick chart по `Open`, `High`, `Low`, `Close`
- график сохраняется в `ex02/aapl_candlestick.html`
- данные агрегируются по последнему рабочему дню месяца
- рассчитываются дневные доходности по `Open`
- дневные доходности считаются двумя способами:
  - через `pct_change()`
  - через формулу с `shift()`
- дополнительно проверяется совпадение результатов

### ex03 - multi-index и доходности нескольких тикеров
- создается `MultiIndex DataFrame` по рабочим дням 2021 года
- используются тикеры: `AAPL`, `FB`, `GE`, `AMZN`, `DAI`
- рассчитываются дневные доходности через `pivot_table(...).pct_change()`
- итоговая таблица имеет широкий формат: индекс `Date`, колонки - тикеры

### ex04 - простой backtest стратегии
- данные `AAPL.txt` заново читаются и очищаются
- рассчитывается `Daily_futur_returns` по `Adj Close`
- генерируется случайный long-only сигнал `0/1`
- рассчитывается `Portfolio_Daily_returns`
- считается total return случайной стратегии
- считается baseline `always buy`
- строится общий график дневного PnL двух стратегий
- график сохраняется в `ex04/strategy_daily_pnl.html`

## Структура проекта

```text
.
├── data/
│   └── AAPL.txt
├── ex00/
│   ├── check_env.py
│   └── requirements.txt
├── ex01/
│   └── answer.py
├── ex02/
│   ├── answer.py
│   └── aapl_candlestick.html
├── ex03/
│   └── answer.py
└── ex04/
    ├── answer.py
    └── strategy_daily_pnl.html
```

## Требования

- Python 3.9+
- `pip`

## Установка

Из корня проекта:

```bash
python -m pip install -r ex00/requirements.txt
```

## Как запускать

### Проверка окружения

```bash
python ex00/check_env.py
```
Проверьте, что Jupyter CLI доступен:

```bash
python -m jupyter --version
```


### Упражнения

```bash
python ex01/answer.py
python ex02/answer.py
python ex03/answer.py
python ex04/answer.py
```

## Что выводят скрипты

- `ex01` печатает исходный ряд и 7-day moving average
- `ex02` печатает информацию о пропусках, `info`, `describe`, результат monthly aggregation и дневные доходности
- `ex03` печатает head исходного `MultiIndex DataFrame`, shape и head таблицы доходностей
- `ex04` печатает `Daily_futur_returns`, `Portfolio_Daily_returns`, PnL baseline-стратегии и итоговые total return

## Сгенерированные файлы

После запуска создаются или обновляются HTML-файлы:

- `ex02/aapl_candlestick.html`
- `ex04/strategy_daily_pnl.html`

Эти файлы можно открыть в браузере.

## Особенности реализации

### Работа с пропусками
В `AAPL.txt` есть пропуски, поэтому перед расчетами данные очищаются через `dropna()`.

### Business month end
В `ex02` для агрегации по последнему рабочему дню месяца используется alias бизнес-конца месяца.

Так как в новых версиях pandas alias `BM` заменен на `BME`, в коде предусмотрена совместимость:
- если `BM` поддерживается, используется `BM`
- если нет, используется эквивалентный `BME`

### Воспроизводимость
В `ex03` и `ex04` используется `np.random.seed(2712)`, чтобы результаты были воспроизводимыми.

## Краткий итог

Проект покрывает базовые задачи по time series:
- создание временного ряда
- rolling average
- preprocessing рыночных данных
- resample и monthly aggregation
- расчет доходностей
- multi-index
- простой backtest стратегии
- визуализация через Plotly

## TOC

- [time-series](#time-series)
- [Что сделано](#что-сделано)
  - [ex00 - проверка окружения](#ex00---проверка-окружения)
  - [ex01 - базовый временной ряд и rolling average](#ex01---базовый-временной-ряд-и-rolling-average)
  - [ex02 - preprocessing, resample, candlestick, returns](#ex02---preprocessing-resample-candlestick-returns)
  - [ex03 - multi-index и доходности нескольких тикеров](#ex03---multi-index-и-доходности-нескольких-тикеров)
  - [ex04 - простой backtest стратегии](#ex04---простой-backtest-стратегии)
- [Структура проекта](#структура-проекта)
- [Требования](#требования)
- [Установка](#установка)
- [Как запускать](#как-запускать)
  - [Проверка окружения](#проверка-окружения)
  - [Упражнения](#упражнения)
- [Что выводят скрипты](#что-выводят-скрипты)
- [Сгенерированные файлы](#сгенерированные-файлы)
- [Особенности реализации](#особенности-реализации)
  - [Работа с пропусками](#работа-с-пропусками)
  - [Business month end](#business-month-end)
  - [Воспроизводимость](#воспроизводимость)
- [Краткий итог](#краткий-итог)

## Автор
- Nazar Yestayev (@nyestaye / @legion2440)