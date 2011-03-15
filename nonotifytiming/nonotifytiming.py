from trac.ticket.api import ITicketActionController, TicketSystem
from trac.ticket.default_workflow import ConfigurableTicketWorkflow
import trac.ticket.notification as notifier
import re

def changed_notify(self, ticket, newticket=True, modtime=None):

	self.env.log.debug("-- New session for ticket %d" % ticket.id)
	
	if newticket:
		self.env.log.debug("New ticet: notifying")
		return self.old_notify(ticket, newticket, modtime)

	has_no_clock_field = False
	has_comment = True

	from trac.ticket.web_ui import TicketModule
	for change in TicketModule(self.env).grouped_changelog_entries(ticket, self.db, when=modtime):
		self.env.log.debug(str(change))
 		if not change['permanent']: # attachment with same time...
			self.env.log.debug("Permanent change, wtf i dont get it")
 			continue

		if 'comment' in change:
			self.env.log.debug("There is 'comment' in change")
			if len(change['comment']) and not re.match(r'(?sumi)^hours[^\n]+plugin.$', change['comment']):
				self.env.log.debug("The comment is not empty!")
				has_comment = True
				break

		self.env.log.debug("There is no comment or it is empty")
		has_comment = False
		
		for field, values in change['fields'].iteritems():
			if field not in ['hours', 'totalhours']:
				has_no_clock_field = True
				self.env.log.debug("It does have no clock field: %s" %field)
				break


	if has_comment or has_no_clock_field:
		self.env.log.debug("Sending email")
		return self.old_notify(ticket, newticket, modtime)


notifier.TicketNotifyEmail.old_notify = notifier.TicketNotifyEmail.notify
notifier.TicketNotifyEmail.notify = changed_notify
