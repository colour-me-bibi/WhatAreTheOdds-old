from django.contrib import admin

from .models import Contract, Investment, Market, Offer, PriceHistory, Tag

# admin.site.register(UserAccount)
admin.site.register(Tag)
admin.site.register(Market)
admin.site.register(Contract)
admin.site.register(Offer)
admin.site.register(PriceHistory)
admin.site.register(Investment)
