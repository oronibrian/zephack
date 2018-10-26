import os
from django.utils.translation import ugettext_lazy as _

from viewflow import flow, frontend, lock
from viewflow.base import this, Flow
from viewflow.flow import views as flow_views


from .models import ClaimProcess


@frontend.register
class HelloWorldFlow(Flow):
    process_class = ClaimProcess
    process_title = _('New Claim Application')
    process_description = _('TLodging new claim request.')

    lock_impl = lock.select_for_update_lock

    summary_template = _("'{{ process.text }}'")

    start = (
        flow.Start(
            flow_views.CreateProcessView,
            fields=['text','location_of_loss','class_of_business','business_of_insured',
            'consequence_of_loss','description'],
            task_title=_('Lodge Claim'))
        .Permission(auto_create=True)
        .Next(this.approve)
    )



    approve = (
        flow.View(
            flow_views.UpdateProcessView, fields=['approved'],
            task_title=_('Approve'),
            task_description=_("Claim approvement required"),
            task_result_summary=_("Claim was {{ process.approved|yesno:'Approved,Rejected' }}"))
        .Permission(auto_create=True)
        .Assign(lambda act: act.process.created_by)

        .Next(this.check_approve)
    )

    check_approve = (
        flow.If(
            cond=lambda act: act.process.approved,
            task_title=_('Approvement check'),
        )
        .Then(this.send)
        .Else(this.end)
    )

    send = (
        flow.Handler(
            this.send_hello_world_request,
            task_title=_('Send Claim'),
        )
        .Next(this.end)
    )

    end = flow.End(
        task_title=_('End'),
    )

    def send_hello_world_request(self, activation):
        with open(os.devnull, "w") as world:
            world.write(activation.process.text)
