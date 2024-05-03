from django.contrib import admin
from .models import User, Cloupe, CoupleSpecialDate, CoupleMessage, CoupleWishList, CoupleImage

admin.site.register(User)

# TODO remove
admin.site.register(Cloupe)
admin.site.register(CoupleSpecialDate)
admin.site.register(CoupleMessage)
admin.site.register(CoupleWishList)
admin.site.register(CoupleImage)