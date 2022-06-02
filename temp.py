
"""

class CarCompany(models.Model):
    name = models.CharField(max_length = 100)


slug

    slug imports:
        from django.utils.text import slugify   
        from django.db.models.signals import pre_save


    slug field for listing
        slug = models.SlugField(unique=True)




    slugify function and signal for listing
        def create_listing_slug(instance, new_slug = None):
            slug = slugify(instance.make + " " +instance.model_name)
            if new_slug is not None:
                slug = new_slug
            qs = SellCarListing.objects.filter(slug = slug)
            exists = qs.exists()
            if exists:
                new_slug = "%s-%s"%(slug, qs.first().id)
                return create_listing_slug(instance, new_slug = new_slug)
            return slug

        def pre_listing_created_signal(sender, instance, **kwargs):
            if not instance.slug:
                instance.slug = create_listing_slug(instance)
        

        # post_save.connect(post_blog_created_signal, sender = Listing)
        pre_save.connect(pre_listing_created_signal, sender = SellCarListing)
        # pre_save.connect(pre_category_created_signal, sender = Category)





"""