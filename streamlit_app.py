import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

# --- 1. НАСТРОЙКА МОДЕЛИ И КЛЮЧА ---
MODEL_NAME = "gemini-2.5-flash" 
MY_API_KEY = "AIzaSyByoPMgs718njzzdnc9ZNXFJPgR2Qu6y38"
os.environ["GOOGLE_API_KEY"] = MY_API_KEY

# --- 2. ИНТЕРФЕЙС STREAMLIT ---
st.set_page_config(
    page_title="Адаптивный гид KazNU", 
    layout="wide", 
    page_icon="🌍",
    initial_sidebar_state="expanded" # Панель можно скрыть стрелочкой слева
)

# --- ЛЕВАЯ  ПАНЕЛЬ (SIDEBAR) ---
with st.sidebar:
    try:
        st.image("1221.JPG", use_container_width=True)
    except:
        st.error("Фото 1221.JPG не найдено")
    
    st.title("Настройки МАС")
    st.success(f"🤖 Модель: {MODEL_NAME}")
    
    st.link_button("🔥 Вступить в СББП (Instagram)", "https://www.instagram.com/sbbp_kaznu/")
    
    st.write("---")
    st.write("**Разработано круто и хайпово**")
    st.write("Студентка: Снежана")
    st.write("Контакты: @snezhanw (inst)")

# --- ЦЕНТРАЛЬНАЯ ЧАСТЬ ---
st.title("🌍 Адаптивный гид для иностранных абитуриентов")

try:
    st.image("kaznu.png", use_container_width=True, caption="Кампус КазНУ им. Аль-Фараби")
except:
    st.warning("Файл kaznu.png не найден в папке с проектом")

st.markdown("Добро пожаловать в КазНУ! Система составит для тебя лучший маршрут.")

# --- ЗОНА 1: КОНФИГУРАЦИЯ ---
st.header("⚙️ Зона 1: Конфигурация")
with st.expander("✨ Выбери гидов :) (нажми, чтобы настроить их характер)"):
    st.subheader("Настройка Агента-Аналитика")
    role_analyst = st.text_input("Роль Аналитика:", value="Культурный эксперт КазНУ")
    backstory_analyst = st.text_area("История Аналитика:", 
                                     value="Ты профи в межкультурной коммуникации. Помогаешь иностранцам влюбиться в КазНУ.")
    
    st.divider()
    
    st.subheader("Настройка Агента-Гида")
    role_guide = st.text_input("Роль Гида:", value="Студенческий гид-проводник")
    backstory_guide = st.text_area("История Гида:", 
                                   value="Ты свой парень в кампусе. Знаешь всё про Спаун и лучшие донеры. Говоришь на дружелюбном языке.")

# --- ЗОНА 2: ВВОД ДАННЫХ ---
st.header("📝 Зона 2: Ввод данных")
col1, col2 = st.columns(2)
with col1:
    origin_country = st.text_input("Из какой страны студенты?", value="Южная Корея")
with col2:
    campus_objects = st.text_area(
        "Объекты кампуса:", 
        value="""1. ЦОС Керемет (центр обслуживания и поликлиника)
2. Библиотека Аль-Фараби (самая большая в стране)
3. Спаун / Арай донерка (место силы и отдыха)
4. Общежитие №8 (твой новый дом)
5. Учебные корпуса (твои будущие аудитории)""",
        height=150
    )

# --- 4. ЛОГИКА АГЕНТОВ ---
def run_tour_process(country, objects, r_analyst, b_analyst, r_guide, b_guide):
    llm = ChatGoogleGenerativeAI(model=MODEL_NAME, google_api_key=MY_API_KEY)

    analyst = Agent(
        role=r_analyst, 
        goal=f'Адаптация для студентов из {country}', 
        backstory=b_analyst, 
        llm=llm
    )
    
    guide = Agent(
        role=r_guide, 
        goal=f'Составить лучший маршрут по {objects}', 
        backstory=b_guide, 
        llm=llm
    )

    t1 = Task(
        description=f"3 совета для студентов из {country} при посещении КазНУ.", 
        expected_output="Культурные советы.", 
        agent=analyst
    )
    
    t2 = Task(
        description=f"""Напиши крутой гид по местам: {objects}. 
        В конце обязательно добавь: 'Вступай в студ организации! Это весело и быстро найдешь друзей и вы вместе пройдете КазНУ еще 930498 раз! Советую СББП!'""", 
        expected_output="Текст гида на русском языке.", 
        agent=guide
    )

    crew = Crew(agents=[analyst, guide], tasks=[t1, t2], process=Process.sequential)
    return crew.kickoff()

# --- ЗОНА 3: ЗАПУСК ---
st.divider()
st.header("🚀 Зона 3: Запуск")
if st.button("🌟 Сгенерировать гид и вступить в движ", use_container_width=True):
    with st.status("🤖 Агенты обсуждают маршрут...", expanded=True) as status:
        try:
            result = run_tour_process(
                origin_country, 
                campus_objects, 
                role_analyst, 
                backstory_analyst, 
                role_guide, 
                backstory_guide
            )
            status.update(label="✅ Гид готов! СББП ждет тебя!", state="complete", expanded=False)
            
            st.markdown("### ✨ Твой персональный гид по КазНУ")
            st.markdown(result.raw)
            
            st.download_button("📥 Скачать гид (.md)", result.raw, file_name="kaznu_guide.md")
            st.balloons()
        except Exception as e:
            st.error(f"Произошла ошибка: {e}")