from django.db import models
from viewflow.models import Process, Task
from django.utils.translation import ugettext_lazy as _
from ckeditor.fields import RichTextField


class ClaimProcess(Process):
    text = models.CharField(_('Message'), max_length=50)

    location_of_loss = models.CharField(max_length=255)
    class_of_business = models.CharField(max_length=255)
    business_of_insured =models. CharField(max_length=255)
    consequence_of_loss =models. CharField(max_length=255)
    description = RichTextField()


    approved = models.BooleanField(_('Approved'), default=False)

    class Meta:
        verbose_name = _("Claim_Request")
        verbose_name_plural = _('Claim_Requests')
