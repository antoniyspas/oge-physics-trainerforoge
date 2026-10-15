# type: ignore
import streamlit as st
import random
import slovari

tasks_dict_mex = getattr(slovari, "tasks_dict_mex", {})
tasks_dict_teplo = getattr(slovari, "tasks_dict_teplo", {})
tasks_dict_electro = getattr(slovari, "tasks_dict_electro", {})

tasks_dict_mex_hard = getattr(slovari, "tasks_dict_mex_hard", {})
tasks_dict_teplo_hard = getattr(slovari, "tasks_dict_teplo_hard", {})
tasks_dict_electro_hard = getattr(slovari, "tasks_dict_electro_hard", {})

tasks_dict_mex_combo = getattr(slovari, "tasks_dict_mex_combo", {})
tasks_dict_teplo_combo = getattr(slovari, "tasks_dict_teplo_combo", {})
tasks_dict_elec_combo = getattr(slovari, "tasks_dict_elec_combo", {})

st.set_page_config(
    page_title="Тренажёр ОГЭ по физике",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
    html, body, p, h1, h2, h3, h4, h5, h6, label, li, input, button {
        font-family: 'Trebuchet MS', 'Arial', sans-serif !important;
    }
    button[kind="primary"] {
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 14px !important;
        border-radius: 10px !important;
    }
    .stHeadingWithAction > a {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "Навигация",
    ["🧠 Тренажер задач", "📚 Справочник ОГЭ", "🔬 Приборы для ОГЭ"]
)

with st.sidebar:
    st.markdown("---")
    st.header("📚 Табличные константы")
    
    st.markdown("### 🌡️ Тепловые явления")
    st.markdown("""
    * $c$ воды: **4200 Дж/(кг·°C)**
    * $c$ льда: **2100 Дж/(кг·°C)**
    * $c$ алюминия: **920 Дж/(кг·°C)**
    * $c$ стали/железа: **500 Дж/(кг·°C)**
    * $c$ меди: **400 Дж/(кг·°C)**
    * $c$ олова: **230 Дж/(кг·°C)**
    * $c$ свинца: **130 Дж/(кг·°C)**
    * $\\lambda$ плавления льда: **3.3·10⁵ Дж/кг**
    * $L$ парообразования воды: **2.3·10⁶ Дж/кг**
    * $q$ бензина/керосина: **4.6·10⁷ Дж/кг**
    * $q$ спирта: **2.7·10⁷ Дж/кг**
    """)
    
    st.markdown("---")
    st.markdown("### ⚡ Электричество")
    st.markdown("""
    * $\\rho$ нихрома: **1.1 Ом·мм²/м**
    * $\\rho$ никелина: **0.4 Ом·мм²/м**
    """)
    
    st.markdown("---")
    st.markdown("### ⚙️ Механика")
    st.markdown("""
    * $g$: **10 м/с²**
    * $\\rho$ воды: **1000 кг/м³**
    * $\\rho$ керосина / спирта: **800 кг/м³**
    * $\\rho$ глицерина: **1260 кг/м³**
    * $\\rho$ алюминия: **2700 кг/м³**
    * $\\rho$ меди: **8900 кг/м³**
    * $\\rho$ свинца: **11300 кг/м³**
    """)


def render_trainer_tab(prefix, dict_mex, dict_elec, dict_tepl, level_name):
    k_task = f"{prefix}_task"
    k_total = f"{prefix}_total"
    k_correct = f"{prefix}_correct"
    k_attempts = f"{prefix}_attempts"
    k_solved = f"{prefix}_solved"
    k_status = f"{prefix}_status"
    k_input = f"{prefix}_input"
    
    k_mex = f"{prefix}_mex_val"
    k_elec = f"{prefix}_elec_val"
    k_tepl = f"{prefix}_tepl_val"

    if k_task not in st.session_state:
        st.session_state[k_task] = None
        st.session_state[k_total] = 0
        st.session_state[k_correct] = 0
        st.session_state[k_attempts] = 0
        st.session_state[k_solved] = False
        st.session_state[k_status] = ""
        st.session_state[k_input] = 0
        st.session_state[k_mex] = True
        st.session_state[k_elec] = False
        st.session_state[k_tepl] = False

    def generate_task():
        available = []
        if st.session_state[k_mex]:
            available.extend(dict_mex.values())
        if st.session_state[k_elec]:
            available.extend(dict_elec.values())
        if st.session_state[k_tepl]:
            available.extend(dict_tepl.values())

        if not available:
            st.toast("Выберите хотя бы одну тему с задачами!", icon="⚠️")
            return

        chosen = random.choice(available)
        vals = chosen["generatenumb"]()

        st.session_state[k_task] = {
            "text": chosen["text"].format(**vals),
            "answer": int(round(chosen["solve"](vals))),
            "solution": chosen["solution"](vals)
        }
        st.session_state[k_attempts] = 0
        st.session_state[k_solved] = False
        st.session_state[k_status] = ""
        st.session_state[k_input] = 0

    def check_answer():
        task = st.session_state[k_task]
        if not task or st.session_state[k_solved]:
            return

        user_ans = st.session_state[k_input]
        st.session_state[k_attempts] += 1

        if user_ans == task["answer"]:
            st.session_state[k_solved] = True
            st.session_state[k_status] = "correct"
            st.session_state[k_correct] += 1
            if st.session_state[k_attempts] <= 2:
                st.session_state[k_total] += 1
        else:
            st.session_state[k_status] = "wrong"
            if st.session_state[k_attempts] == 2:
                st.session_state[k_total] += 1

    c_stat1, c_stat2 = st.columns(2)
    with c_stat1:
        st.metric("Пройдено задач", st.session_state[k_total])
    with c_stat2:
        st.metric("Правильных ответов", st.session_state[k_correct])

    task = st.session_state[k_task]

    if task:
        st.markdown("---")
        st.markdown("#### 📝 Условие задачи:")
        st.info(task["text"])
        st.markdown("**Ответ округлите до целых.**")

        if not st.session_state[k_solved]:
            st.number_input(
                "Ваш ответ:",
                step=1,
                key=k_input
            )
            st.button("Проверить ответ", on_click=check_answer, key=f"{prefix}_check")

        if st.session_state[k_status] == "correct":
            st.success("🎉 Вы большой молодец, вы получили правильный ответ!")
        elif st.session_state[k_status] == "wrong":
            if st.session_state[k_attempts] == 1:
                st.error("❌ Вы получили неверный ответ, попытайтесь ещё раз (осталась 1 попытка до решения).")
            else:
                st.error("❌ Вы получили неверный ответ. Ниже открылось подробное решение!")

        if st.session_state[k_solved] or st.session_state[k_attempts] >= 2:
            with st.expander("💡 Посмотреть ход решения"):
                st.write(task["solution"])
                st.write(f"**Правильный ответ:** {task['answer']}")

    if not task or st.session_state[k_solved] or st.session_state[k_attempts] >= 2:
        st.markdown("---")
        st.markdown(f"### 🎯 Выберите темы ({level_name}):")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.session_state[k_mex] = st.checkbox(
                f"⚙️ Механика ({len(dict_mex)})",
                value=st.session_state[k_mex],
                key=f"{prefix}_mex_chk"
            )
        with col2:
            st.session_state[k_elec] = st.checkbox(
                f"⚡ Электричество ({len(dict_elec)})",
                value=st.session_state[k_elec],
                key=f"{prefix}_elec_chk"
            )
        with col3:
            st.session_state[k_tepl] = st.checkbox(
                f"🌡️ Теплота ({len(dict_tepl)})",
                value=st.session_state[k_tepl],
                key=f"{prefix}_tepl_chk"
            )

        st.write("")
        btn_text = "🎲 ВЫБРАТЬ РАНДОМНУЮ ЗАДАЧУ" if not task else "🎲 СГЕНЕРИРОВАТЬ ДРУГУЮ ЗАДАЧУ"
        st.button(btn_text, on_click=generate_task, type="primary", use_container_width=True, key=f"{prefix}_gen")


if page == "🧠 Тренажер задач":
    st.title("🧠 Тренажёр задач ОГЭ по физике")

    tab1, tab2, tab3 = st.tabs([
        f"📘 Задачи обычного уровня ({len(tasks_dict_mex) + len(tasks_dict_electro) + len(tasks_dict_teplo)})",
        f"📙 Задачи высокого уровня ({len(tasks_dict_mex_hard) + len(tasks_dict_electro_hard) + len(tasks_dict_teplo_hard)})",
        f"📕 Комбинированные задачи ({len(tasks_dict_mex_combo) + len(tasks_dict_elec_combo) + len(tasks_dict_teplo_combo)})"
    ])

    with tab1:
        render_trainer_tab("normal", tasks_dict_mex, tasks_dict_electro, tasks_dict_teplo, "Обычный уровень")

    with tab2:
        render_trainer_tab("hard", tasks_dict_mex_hard, tasks_dict_electro_hard, tasks_dict_teplo_hard, "Высокий уровень")

    with tab3:
        render_trainer_tab("combo", tasks_dict_mex_combo, tasks_dict_elec_combo, tasks_dict_teplo_combo, "Комбинированные задачи")

elif page == "📚 Справочник ОГЭ":
    st.title("📚 Формулы для ОГЭ по физике")

    ref_tab1, ref_tab2, ref_tab3, ref_tab4 = st.tabs([
        "⚙️ Механика",
        "🔥 Тепловые явления",
        "⚡ Электричество",
        "👁️ Оптика и Ядро"
    ])

    with ref_tab1:
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.markdown("**Путь и скорость (равномерное движение)**")
                st.latex(r"v = \frac{S}{t}")
            with st.container(border=True):
                st.markdown("**Скорость и путь при равноускоренном движении**")
                st.latex(r"v = v_0 + at \quad ; \quad S = v_0 t + \frac{at^2}{2}")
            with st.container(border=True):
                st.markdown("**Формула пути без времени**")
                st.latex(r"S = \frac{v^2 - v_0^2}{2a}")
            with st.container(border=True):
                st.markdown("**Центростремительное ускорение**")
                st.latex(r"a_{ц} = \frac{v^2}{R}")
            with st.container(border=True):
                st.markdown("**Второй закон Ньютона и Сила тяжести**")
                st.latex(r"F = ma \quad ; \quad F_{тяж} = mg")
            with st.container(border=True):
                st.markdown("**Сила трения и Закон Гука**")
                st.latex(r"F_{тр} = \mu N \quad ; \quad F_{упр} = kx")
        with col2:
            with st.container(border=True):
                st.markdown("**Импульс тела и Закон сохранения импульса**")
                st.latex(r"p = mv \quad ; \quad m_1\vec{v}_1 + m_2\vec{v}_2 = m_1\vec{v}_1' + m_2\vec{v}_2'")
            with st.container(border=True):
                st.markdown("**Механическая работа и Мощность**")
                st.latex(r"A = F \cdot S \quad ; \quad P = \frac{A}{t} = F \cdot v")
            with st.container(border=True):
                st.markdown("**Кинетическая и Потенциальная энергия**")
                st.latex(r"E_k = \frac{mv^2}{2} \quad ; \quad E_p = mgh")
            with st.container(border=True):
                st.markdown("**Момент силы (правило рычага)**")
                st.latex(r"M = F \cdot l \quad ; \quad F_1 l_1 = F_2 l_2")
            with st.container(border=True):
                st.markdown("**Гидростатическое давление и Сила Архимеда**")
                st.latex(r"p = \rho g h \quad ; \quad F_A = \rho_{ж} g V_{погр}")
            with st.container(border=True):
                st.markdown("**КПД механизма**")
                st.latex(r"\eta = \frac{A_{полезн}}{A_{затр}} \cdot 100\%")

    with ref_tab2:
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.markdown("**Нагревание и охлаждение**")
                st.latex(r"Q = cm\Delta t = cm(t_2 - t_1)")
            with st.container(border=True):
                st.markdown("**Плавление и кристаллизация**")
                st.latex(r"Q = \lambda m")
            with st.container(border=True):
                st.markdown("**КПД тепловой машины**")
                st.latex(r"\eta = \frac{A_{полезн}}{Q_{нагр}} \cdot 100\%")
        with col2:
            with st.container(border=True):
                st.markdown("**Парообразование и конденсация**")
                st.latex(r"Q = Lm")
            with st.container(border=True):
                st.markdown("**Сгорание топлива**")
                st.latex(r"Q = qm")
            with st.container(border=True):
                st.markdown("**Относительная влажность воздуха**")
                st.latex(r"\varphi = \frac{\rho}{\rho_{н.п.}} \cdot 100\%")

    with ref_tab3:
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.markdown("**Сила тока и Напряжение**")
                st.latex(r"I = \frac{q}{t} \quad ; \quad U = \frac{A}{q}")
            with st.container(border=True):
                st.markdown("**Закон Ома и Сопротивление проводника**")
                st.latex(r"I = \frac{U}{R} \quad ; \quad R = \rho \frac{l}{S}")
            with st.container(border=True):
                st.markdown("**Последовательное соединение**")
                st.latex(r"I = I_1 = I_2 \quad ; \quad U = U_1 + U_2 \quad ; \quad R = R_1 + R_2")
        with col2:
            with st.container(border=True):
                st.markdown("**Мощность тока**")
                st.latex(r"P = U I = I^2 R = \frac{U^2}{R}")
            with st.container(border=True):
                st.markdown("**Закон Джоуля–Ленца (работа и теплота тока)**")
                st.latex(r"Q = A = U I t = I^2 R t = \frac{U^2}{R} t")
            with st.container(border=True):
                st.markdown("**Параллельное соединение**")
                st.latex(r"U = U_1 = U_2 \quad ; \quad I = I_1 + I_2 \quad ; \quad \frac{1}{R} = \frac{1}{R_1} + \frac{1}{R_2}")

    with ref_tab4:
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.markdown("**Оптическая сила и Формула тонкой линзы**")
                st.latex(r"D = \frac{1}{F} \quad ; \quad \pm \frac{1}{F} = \frac{1}{d} \pm \frac{1}{f}")
        with col2:
            with st.container(border=True):
                st.markdown("**Состав ядра и Альфа/Бета-распад**")
                st.latex(r"A = Z + N \quad ; \quad ^{A}_{Z}X \rightarrow ^{A-4}_{Z-2}Y + ^{4}_{2}\text{He}")



elif page == "🔬 Приборы для ОГЭ":
    st.title("🔬 Все приборы и устройства для ОГЭ по физике")
    st.markdown("Выберите раздел, чтобы посмотреть приборы и физические явления/законы, лежащие в основе их работы:")

    devices_data = {
        "⚙️ Механика": [
            ("Рычажные весы", "Условие равновесия рычага"),
            ("Пружинный динамометр", "Зависимость силы упругости от деформации тела"),
            ("Садовая тачка", "Условие равновесия рычага"),
            ("Барометрический высотомер", "Зависимость атмосферного давления от высоты"),
            ("Гидравлический пресс", "Передача давления внутри жидкости (закон Паскаля)"),
            ("Поршневой жидкостный насос", "Действие атмосферного давления"),
            ("Шлюз", "Поведение жидкости в сообщающихся сосудах"),
            ("Жидкостный манометр", "Зависимость гидростатического давления от высоты столба жидкости"),
            ("Барометр-анероид", "Зависимость деформации от действия силы"),
            ("U-образный манометр", "Зависимость гидростатического давления от высоты столба жидкости"),
            ("Медицинская пипетка", "Прибор для получения капель жидкости. Принцип действия основан на действии атмосферного давления")
        ],
        "🌡️ Термодинамика": [
            ("Жидкостный термометр", "Зависимость объема жидкости от ее температуры"),
            ("Психрометр", "Уменьшение температуры жидкости при ее испарении"),
            ("Двигатель внутреннего сгорания", "Превращение внутренней энергии в механическую"),
            ("Спиртовой термометр", "Объёмное расширение жидкости при нагревании"),
            ("Паровая турбина", "Превращение внутренней энергии пара в механическую"),
            ("Гидротурбина", "Превращение механической энергии в электрическую")
        ],
        "⚡ Электромагнитные явления": [
            ("Электрометр", "Зависимость силы отталкивания одноименных зарядов от их величины"),
            ("Копировальный аппарат (ксерокс)", "Электризация (аппарат электрографического типа с порошковым красящим элементом)"),
            ("Циклотрон", "Действие магнитного и электрического полей на движущуюся заряженную частицу"),
            ("Электродвигатель постоянного тока", "Действие магнитного поля на проводник с током"),
            ("Компас", "Взаимодействие постоянных магнитов"),
            ("Амперметр", "Зависимость силы, действующей на проводник с током в магнитном поле, от силы тока в проводнике"),
            ("Демонстрационный гальванометр", "Чувствительный амперметр для малых токов — зависимость силы, действующей на проводник с током в магнитном поле, от силы тока в проводнике"),
            ("Масс-спектрометр", "Действие магнитного поля на движущуюся заряженную частицу"),
            ("Магнитный сепаратор (для очистки зерна)", "Взаимодействие электромагнита и железных или стальных предметов"),
            ("Электродинамический микрофон", "Электромагнитная индукция"),
            ("Трансформатор", "Электромагнитная индукция"),
            ("Индукционная плита", "Электромагнитная индукция"),
            ("Генератор переменного тока на ГЭС", "Электромагнитная индукция"),
            ("Электропаяльник", "Тепловое действие тока"),
            ("Лампа накаливания", "Тепловое действие тока, излучение нагретого тела"),
            ("Электрический утюг", "Тепловое действие тока"),
            ("Электрический кипятильник", "Тепловое действие тока"),
            ("Электрическая плита", "Тепловое действие тока"),
            ("Ванна для получения чистых металлов (электролиз)", "Химическое действие тока"),
            ("Реостат", "Зависимость сопротивления проводника от его длины"),
            ("Гальванический элемент", "Превращение химической энергии в электрическую"),
            ("Тепловизор (прибор ночного видения)", "Излучение нагретым телом инфракрасных лучей"),
            ("Бесконтактный термометр", "Излучение нагретым телом инфракрасных лучей"),
            ("Прибор подводной лодки для связи под водой", "Сверхдлинные радиоволны"),
            ("Лампы в соляриях", "Ультрафиолетовые волны"),
            ("Кварцевые лампы (для дезинфекции воздуха и воды)", "Ультрафиолетовые волны"),
            ("Лампы дневного света", "Видимое излучение")
        ],
        "👁️ Оптика": [
            ("Зеркальный перископ, телескоп", "Отражение света"),
            ("Зеркало", "Отражение света"),
            ("Радиолокатор", "Отражение электромагнитных волн"),
            ("Проекционный аппарат, оптический микроскоп", "Преломление света"),
            ("Линза, лупа, очки", "Преломление света"),
            ("Призменный спектроскоп", "Дисперсия света")
        ],
        "☢️ Атомная и ядерная физика": [
            ("Счетчик Гейгера", "Ударная ионизация электронами атомов газа"),
            ("Приборы для получения снимков скелета человека", "Рентгеновское излучение"),
            ("Индивидуальный дозиметр", "Прибор для измерения поглощённой дозы излучения")
        ]
    }

    dev_tabs = st.tabs(list(devices_data.keys()))

    for tab, (_, items) in zip(dev_tabs, devices_data.items()):
        with tab:
            col1, col2 = st.columns(2)
            for idx, (device_name, principle) in enumerate(items):
                target_col = col1 if idx % 2 == 0 else col2
                with target_col:
                    with st.container(border=True):
                        st.markdown(f"🔹 **{device_name}**")
                        st.caption(f"Принцип действия: {principle}")