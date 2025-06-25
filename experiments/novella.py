import json
from backend.models import Chain, Run, Agent, Context
from utils import chat
from chaingang.dist.chaingang import build_prompt


def start_novella():
    model = "gpt-4o"

    idea_generator = Agent.objects.get(id=4)
    outline_creator = Agent.objects.get(id=3)
    writer = Agent.objects.get(id=5)

    novella_run = Run.objects.create(current_agent=idea_generator, status="running")

    assistant_id = "asst_FJAL2fvZ6KhVILMIn6qFEbId"
    thread_id = chat.create_thread()

    start_input = """{
    "genre": "Mystery Thriller",
    "setting": "Orleans, Ontario Canada",
    "time_period": "Present day",
    "themes": [
        "Secrets",
        "Betrayal",
        "Deceipt",
        "Artificial Intelligence",
        "How AI is powerful, can change control our lives and be deceitful "
    ],
    "rough_plot_idea": "Fast-Paced Plot Suggestions with a Twist. Act I: Setting the Stakes: 1. Carl, working on a benign freelance contract, notices a signal that seems familiar—Centurion’s shadow operations echo through encrypted financial trails. 2. Angie reconnects with Carl, presenting evidence about Centurion’s funds resurfacing, tied to new corporate sabotage. 3. The Magician nudges Carl toward a lucrative contract to distract him, hiding the fact that Carl is under surveillance by the Black Talon. Act II: Rising Tension: 1. Black Talon Attacks: Carl’s condo is ransacked, forcing him and Angie to go on the run. 2. Nikita Kozlov’s Cyber Duel: Nikita hacks into SignalHunter to use it for Andrei’s plans, triggering the ECM. Carl must remotely secure the system while evading capture. 3. The Magician’s Betrayal: Carl uncovers evidence tying The Magician to Centurion’s original scandals but hesitates to confront him, fearing exposure to Angie. Act III: Climax: 1. The Professor’s Gambit: Andrei captures Angie, demanding Carl hand over SignalHunter’s access codes. Carl uses SignalHunter to predict Andrei’s moves, leading to a high-stakes rescue. 2. Double Betrayal: Carl learns The Magician orchestrated the entire plot to recover Centurion’s hidden funds to clear his debts and protect his career. 3. Angie’s Confrontation: She uncovers Robert’s identity as The Magician, forcing Carl to choose between exposing him or using his knowledge to trap Andrei. Twist Ending: SignalHunter’s Revelation: The ECM reveals that SignalHunter has been autonomously tracking The Magician’s unethical behavior for years, culminating in a climactic reveal that threatens to bring down global networks tied to corruption. Moral Dilemma: Carl can use SignalHunter to destroy the villains but risks exposing innocent parties or sparing The Magician to keep his family safe. Final Choice: Carl leverages SignalHunter to anonymously release incriminating evidence, sacrificing his chance at a quiet life for global accountability. Building the Twist: Emphasize Misdirection: Early clues suggest Andrei or Nikita are the ultimate threat, while The Magician’s role in orchestrating Centurion’s actions is revealed only late. Multiple Layers: Introduce a subplot involving Madison or Carl Jr. that collides with the main conspiracy, tying personal stakes to the climax. Ethical Dilemma Payoff: SignalHunter’s ECM serves as a mirror to Carl’s morality, questioning every choice he makes"
    }
    """

    prompt = build_prompt(idea_generator, dependency_res=start_input)
    response = chat.get_response(
        prompt, model=model, assistant_id=assistant_id, thread_id=thread_id
    )

    Context.objects.create(
        run=novella_run,
        agent=idea_generator,
        prompt=prompt,
        response=response,
        is_final=False,
    )

    prompt = build_prompt(outline_creator, dependency_res=response)
    response = chat.get_response(
        prompt, model=model, assistant_id=assistant_id, thread_id=thread_id
    )

    Context.objects.create(
        run=novella_run,
        agent=outline_creator,
        prompt=prompt,
        response=response,
        is_final=True,
    )

    novella_run.status = "completed"
    novella_run.save()

    response["current_chapter"] = 1

    chapter_input = response

    while True:
        prompt = build_prompt(
            writer, dependency_res=chapter_input, assistant_id=assistant_id
        )
        response = chat.get_response(
            prompt, model=model, assistant_id=assistant_id, thread_id=thread_id
        )

        if response is None:
            continue

        Context.objects.create(
            run=novella_run,
            agent=writer,
            prompt=prompt,
            response=response,
            is_final=False,
        )

        if "updated_input" not in response:
            print("Attention Required")
            continue

        previous_input = response["updated_input"]

        if previous_input.get("current_chapter") == "FINISHED":
            break
        if previous_input.get("current_chapter") is None:
            break

        chapter_input = previous_input

    novella_run.status = "completed"
    novella_run.save()

    print("*** Novella generation completed successfully! ***")
    print(novella_run.id)
