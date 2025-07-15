from backend.models import Chain, Run, Agent, Context
from utils import chat


def run_chain(chain_id, start_input=None):

    model = "gpt-4o-mini"  # Default model, can be overridden

    try:
        chain = Chain.objects.get(id=chain_id)
    except Chain.DoesNotExist:
        raise ValueError(f"Chain with ID {chain_id} does not exist.")

    # Initialize the run
    run = Run.objects.create(chain=chain, status="running")

    for i, agent_id in enumerate(chain.agent_ids):

        if i == 0:
            agent = Agent.objects.get(id=agent_id)
            if agent.user_input_required and start_input is None:
                raise ValueError(
                    f"Agent {agent.name} requires user input to start the chain."
                )

        run_agent(agent_id, run.id, model=model, start_input=start_input)


def run_agent(agent_id, run_id, model="gpt-4o-mini", start_input=None):
    try:
        agent = Agent.objects.get(id=agent_id)
    except Agent.DoesNotExist:
        raise ValueError(f"Agent with ID {agent_id} does not exist.")

    run = Run.objects.get(id=run_id)
    if run.status != "running":
        return

    run.current_agent = agent
    run.save()

    dependency = None
    dependency_res = None
    for dep in run.chain.dependency_chain:
        if dep[0] == agent_id:
            dependency = dep[1]

    if agent.user_input_required and start_input is not None:
        # If the agent requires user input, use the provided start_input
        dependency_res = start_input
    elif dependency:
        dependency_run = Context.objects.filter(run=run, agent__id=dependency).last()
        dependency_res = dependency_run.response if dependency_run else None

    prompt = build_prompt(agent, dependency_res)
    response = chat.get_response(prompt, model=model, assistant_id=run.assistant_id)

    # Save the context
    context = Context.objects.create(
        run=run, agent=agent, prompt=prompt, response=response, is_final=False
    )

    # Update the run status if this is the last agent
    if agent_id == run.chain.agent_ids[-1]:
        run.status = "completed"
        context.is_final = True
        context.save()

    run.save()

    return response


def build_prompt(agent, dependency_res=None):

    prompt = f"""Who you are:
    {agent.description}

    The input data format:
    {agent.input or "No specific input format provided."}
    Your instructions:
    {agent.instructions or "No specific instructions provided."}

    The output data format:
    {agent.output or "No specific output format provided."}"""

    if dependency_res:
        prompt += f"\n\nThe Input Data::\n{dependency_res}"

    return prompt
