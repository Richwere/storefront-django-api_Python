from django.db import models
#from profiling.tracing import label
from store.models import Product
from django.contrib.contenttypes.models import ContentType 
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class Tag(models.Manager):#inheriting from the manager class to create a custom manager for the Tag model
    def get_tags_for(self, model, label):   
        content_type = ContentType.objects.get_for_model(model)
        return self.filter(content_type=content_type, tag__label=label) 

        return TaggedItem.objects.filter(content_type=content_type, object_id=object.id)  
    

class Tag(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self) ->str:
        return self.label

class TaggedItem(models.Model):
    # What tag is applied to what object
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey(
        'content_type',
        'object_id'
    )