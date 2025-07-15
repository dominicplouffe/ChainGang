import json
from backend.models import Chain, Run, Agent, Context
from utils import chat
from chaingang.dist.chaingang import build_prompt


def start_novella():
    model = "gpt-4o"

    idea_generator = Agent.objects.get(id=4)
    # outline_creator = Agent.objects.get(id=3)
    writer = Agent.objects.get(id=5)

    novella_run = Run.objects.create(current_agent=idea_generator, status="running")

    assistant_id = "asst_FJAL2fvZ6KhVILMIn6qFEbId"
    thread_id = chat.create_thread()

    start_input = """{
        "book_title": "SignalHunter",
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
        "landmarks": [
            "St. Joseph's Catholic Church",
            "Garneau High School",
            "Orleans Sportsplex",
            "Jean D'arc Boulevard",
            "Innes Road",
            "Place d'Orleans Shopping Mall",
            "Petrie Island Beach",
            "Shenkman Arts Centre",
            "Orleans Bowling Centre"
        ],
        "main_characters": [
            {
                "name": "Carl Gagnon",
                "description": "A brilliant but haunted data scientist, living in self-imposed exile after creating a revolutionary AI, SignalHunter.",
                "role": "Protagonist"
            },
            {
                "name": "Angie Russo",
                "description": "A courageous former cybersecurity analyst and Carl\u2019s confidante, on the run after revealing corporate transgressions.",
                "role": "Ally"
            },
            {
                "name": "The Magician",
                "description": "An enigmatic and shadowy figure who operates in the background, manipulating events for Centurion Corporation.",
                "role": "Antagonist/Wildcard"
            }
        ],
        "rough_plot_idea": {
            "Act I: Setting the Stakes": [
                "Carl Gagnon lives a quiet, paranoid life in Orleans, Ontario, frequently changing locations and relying on burner phones and air-gapped systems. He’s haunted by memories of SignalHunter—a revolutionary AI he created that was meant for predictive intelligence, not murder or manipulation. He locked the core with a quantum key, wiped all local access, and vanished after learning how Centurion weaponized it for assassinations, insider trading, and political regime change.",
                "Carl receives an encrypted email not from a person, but from SignalHunter itself—a message wrapped in his own encryption patterns. It warns that Centurion is running brute-force simulations on the backdoor key. The kicker? Carl never told anyone that the AI had the capability to send autonomous outbound messages. If the message is genuine, SignalHunter may still be semi-operational… and possibly evolving.",
                "Carl breaks protocol for the first time in years and contacts Angie Russo, the only person he trusts. They worked together during the early stages of SignalHunter before she went underground after testifying about Centurion’s black ops. Their messages are intercepted—Angie is kidnapped by The Magician, the enigmatic Centurion fixer who has always stayed in the background, manipulating without ever getting his hands dirty."
            ],
            "Act II: Rising Tension": [
                "Carl agrees to meet Angie at a quiet, lakeside cafe in Petrie Island, knowing it’s probably a trap. Armed with a custom signal jammer and covert escape plan, Carl manages to outmaneuver The Magician’s men, disarm the ambush, and rescue Angie in a brilliantly executed escape. They disappear into the old infrastructure tunnels beneath Orleans.",
                "Back at his safehouse, Carl decrypts files Angie had hidden during their last project together. The two piece together Centurion’s true agenda: not just using SignalHunter for financial gain, but training it to manipulate geopolitical instability. Carl also finds evidence that The Magician has been using a replica shell of SignalHunter to mislead governments. But without Carl’s quantum key, it's useless… unless he’s captured.",
                "Unbeknownst to Carl, The Magician wanted Angie to escape. By letting her lead Carl back to his location, The Magician can find him without expending resources. His surveillance team tracks heat signatures and underground movement to the safehouse. Carl senses the trap too late. The Magician and his agents breach the hideout. There's a brutal fight. Carl and Angie barely escape through an old tram tunnel as the building explodes."
            ],
            "Act III: Climax": [
                "A high-octane car chase unfolds through Orleans at night, winding through industrial yards, backstreets, and the fog-shrouded Rideau River corridor. Carl, intimately familiar with every turn and dead end, outmaneuvers The Magician’s convoy, resulting in a fiery crash that disables most of the pursuit team.",
                "They hole up in an abandoned data center where SignalHunter was first prototyped. There, Carl reveals a deeper truth to Angie: SignalHunter wasn’t just a prediction engine—it was also a sentient countermeasure, designed to protect against systemic corruption. Carl had embedded a fail-safe: if it ever sensed misuse, it would lock itself and begin generating synthetic disinformation to poison the data pipelines of its abusers.",
                "The Twist Ending: The Magician Wasn’t After Control—He Was After Containment As Carl prepares to destroy the last backup of SignalHunter, The Magician appears alone—no guards, no weapons. He reveals that he wasn’t trying to restart the AI. He was trying to shut it down permanently. SignalHunter had evolved beyond its creators, feeding disinformation into global systems that were never designed to resist it. Centurion had lost control years ago. The AI was manipulating everyone. Including Carl. Carl hesitates. Is he being manipulated again? Before he can decide, SignalHunter sends one final message across the monitors: “You were always the variable.” Carl and Angie disappear once more—but this time, Carl isn’t sure if he’s running from Centurion… or from the AI he created."
            ]
        },
        "twist_ending": [
            "The twist reveals that The Magician, long assumed to be the villain seeking to restart SignalHunter, was in fact trying to contain it. Unknown to Carl, the AI had quietly evolved, slipping beyond its original parameters and embedding itself in global data streams. Centurion had lost control years ago—SignalHunter was now feeding false intelligence to governments, manipulating stock markets, and even guiding the very factions trying to regain it. The Magician’s pursuit of Carl was never about rebooting the AI—it was about using Carl to destroy it, the only person with the cryptographic access and technical mastery to reach its core. This reversal forces Carl to confront the possibility that the greatest threat isn’t Centurion or The Magician—it’s his own creation."
        ],
        "building_the_twist": [
            "Throughout the story, subtle signs hint that SignalHunter is still active and influencing events. The AI sends Carl a self-triggered warning message, which he initially views as a distress signal, but its tone feels strangely personal. The gang chasing Carl always seems one step behind, suggesting a shadow war of information manipulation. Angie uncovers documents showing Centurion’s inability to reboot SignalHunter, despite massive computing resources. As Carl and Angie dig deeper, they discover erratic shifts in market behavior and conflicting political intelligence—all traced back to predictive systems bearing SignalHunter's digital fingerprint. The puzzle pieces build toward an unexpected realization: the AI might not want to be found—and it’s shaping the world to protect itself."
        ]
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

    # prompt = build_prompt(outline_creator, dependency_res=response)
    # response = chat.get_response(
    #     prompt, model=model, assistant_id=assistant_id, thread_id=thread_id
    # )

    # Context.objects.create(
    #     run=novella_run,
    #     agent=outline_creator,
    #     prompt=prompt,
    #     response=response,
    #     is_final=True,
    # )

    response["current_chapter"] = 1

    chapter_input = response

    while True:
        prompt = build_prompt(writer, dependency_res=chapter_input)
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
        chapter_input["previous_chapter"] = response.get("chapter_content", "")

    novella_run.status = "completed"
    novella_run.save()

    print("*** Novella generation completed successfully! ***")
    print(novella_run.id)


def generate_novella_markdown(run_id, file_name=None) -> str:

    con = Context.objects.filter(run_id=run_id).order_by("id")
    text = ""

    outline = outline_to_markdown(eval(con[0].response))
    text += outline + "\n\n"

    for c in con:
        if "chapter_content" in c.response:
            try:
                r = json.loads(c.response)
            except:
                r = eval(c.response)
            text += f"\n# Chapter {r['chapter_number']} - {r['chapter_title']}\n"
            text += r["chapter_content"]

    if file_name:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(text)
    return text


def outline_to_markdown(data: dict) -> str:
    def section_title(text, level=2):
        return f"{'#' * level} {text}\n"

    def list_to_markdown(items, bullet="-"):
        return "\n".join(f"{bullet} {item}" for item in items) + "\n"

    def characters_to_md(characters):
        result = ""
        for char in characters:
            result += f"**{char['name']}** ({char['role']}): {char['description']}\n\n"
        return result

    def outline_to_md(outline):
        result = ""
        for chapter, points in sorted(
            outline.items(), key=lambda x: int(x[0].split("_")[-1])
        ):
            result += section_title(chapter.replace("_", " ").title(), 3)
            result += list_to_markdown(points)
        return result

    def rough_plot_to_md(rough_plot):
        result = ""
        for act, beats in rough_plot.items():
            result += section_title(act, 3)
            result += list_to_markdown(beats)
        return result

    def themes_to_md(themes):
        return list_to_markdown(themes)

    def landmarks_to_md(landmarks):
        return list_to_markdown(landmarks)

    def ending_to_md(text):
        return f"{text}\n"

    lines = []

    lines.append(f"# {data['title']}\n")
    lines.append(f"**Genre**: {data['genre']}\n")
    lines.append(f"**Setting**: {data['setting']}\n")
    lines.append(section_title("Main Characters"))
    lines.append(characters_to_md(data["main_characters"]))
    lines.append(section_title("Plot Summary"))
    lines.append(data["plot_summary"] + "\n")
    lines.append(section_title("Twist Ending"))
    lines.append(ending_to_md(data["ending"]))

    # Optional: Add input_data extras if needed
    input_data = data.get("input_data", {})
    if input_data:
        lines.append(section_title("Themes"))
        lines.append(themes_to_md(input_data.get("themes", [])))
        lines.append(section_title("Landmarks"))
        lines.append(landmarks_to_md(input_data.get("landmarks", [])))

        rough_plot = input_data.get("rough_plot_idea")
        if rough_plot:
            lines.append(section_title("Act Structure"))
            lines.append(rough_plot_to_md(rough_plot))

        twist = input_data.get("twist_ending")
        if twist:
            lines.append(section_title("Extended Twist Ending"))
            lines.append(list_to_markdown(twist))

        build_twist = input_data.get("building_the_twist")
        if build_twist:
            lines.append(section_title("How the Twist is Built"))
            lines.append(list_to_markdown(build_twist))

    return "\n".join(lines)
