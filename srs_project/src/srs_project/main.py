import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI

# Устанавливаем ключ (тот же самый)
os.environ["GOOGLE_API_KEY"] = "AIzaSyByoPMgs718njzzdnc9ZNXFJPgR2Qu6y38"

def run():
    # Настраиваем модель
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    # Вводные данные (те самые, что ты хотела)
    inputs = {
        'origin_country': 'Южная Корея',
        'campus_infrastructure': """1. ЦОС Керемет
2. Библиотека Аль-Фараби
3. Спаун (Арай донерка)
4. Общежитие №8
5. Учебные корпуса"""
    }

    # Создаем агентов вручную (как в Streamlit)
    cultural_analyst = Agent(
        role='Культурный эксперт КазНУ',
        goal=f'Проанализировать особенности студентов из {inputs["origin_country"]}',
        backstory="Ты профи в межкультурной коммуникации.",
        llm=llm
    )

    campus_guide = Agent(
        role='Студенческий гид-проводник',
        goal=f'Составить маршрут по местам: {inputs["campus_infrastructure"]}',
        backstory="Ты знаешь всё про Спаун и лучшие донеры в КазНУ.",
        llm=llm
    )

    # Задачи
    task1 = Task(
        description=f"Дай 3 совета для студентов из {inputs['origin_country']}.",
        expected_output="Культурные советы.",
        agent=cultural_analyst
    )

    task2 = Task(
        description=f"""Напиши гид по {inputs['campus_infrastructure']}. 
        В конце добавь: 'Вступай в студ организации! Это весело и быстро найдешь друзей и вы вместе пройдете КазНУ еще 930498 раз! Советую СББП!'""",
        expected_output="Готовый текст гида.",
        agent=campus_guide
    )

    # Сборка и запуск
    crew = Crew(
        agents=[cultural_analyst, campus_guide],
        tasks=[task1, task2],
        process=Process.sequential,
        verbose=True
    )

    print("🚀 Запуск агентов из терминала...")
    result = crew.kickoff(inputs=inputs)
    print("\n\n✨ РЕЗУЛЬТАТ:\n")
    print(result)

if __name__ == "__main__":
    run()