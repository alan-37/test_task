from django.contrib import admin
from .models import Ad, ExchangeProposal


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category',
                    'available', 'condition', 'created_at']
    list_filter = ['available', 'created_at', 'category']
    list_editable = ['available']


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ['id', 'ad_sender', 'ad_receiver',
                    'comment', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']