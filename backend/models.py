from django.db import models


class Agent(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    input = models.TextField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)
    output = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    user_input_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Chain(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    agent_ids = models.JSONField(default=list)  # List of Agent IDs
    dependency_chain = models.JSONField(
        default=list
    )  # List of Agent IDs for dependencies
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Run(models.Model):
    chain = models.ForeignKey(
        Chain, on_delete=models.CASCADE, related_name="runs", null=True
    )
    assistant_id = models.CharField(max_length=100, blank=True, null=True)
    current_agent = models.ForeignKey(
        Agent, on_delete=models.CASCADE, related_name="runs", blank=True, null=True
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("running", "Running"),
            ("completed", "Completed"),
            ("failed", "Failed"),
            ("cancelled", "Cancelled"),
            ("expired", "Expired"),
        ],
        default="running",
    )


class Context(models.Model):
    run = models.ForeignKey(Run, on_delete=models.CASCADE, related_name="contexts")
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="contexts")
    prompt = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    is_final = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
