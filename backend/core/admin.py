from django.contrib import admin

from .models import Contract, Market, Offer, UserAccount

admin.site.register(UserAccount)
admin.site.register(Market)
admin.site.register(Contract)
admin.site.register(Offer)
