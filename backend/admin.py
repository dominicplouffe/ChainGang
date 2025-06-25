from django.contrib import admin

# Register your models here.

from .models import Agent, Chain, Run, Context


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("-created_at",)


@admin.register(Chain)
class ChainAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at", "updated_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("-created_at",)


@admin.register(Run)
class RunAdmin(admin.ModelAdmin):
    list_display = ("chain", "assistant_id", "current_agent", "id")
    search_fields = ("assistant_id",)
    list_filter = ("chain", "current_agent")
    ordering = ("-id",)


@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):
    list_display = ("run", "agent", "is_final", "created_at")
    search_fields = ("run__chain__name", "agent__name")
    list_filter = ("is_final",)
    ordering = ("-created_at",)
