from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from django.db import IntegrityError

from django.http import HttpResponse

from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.contrib.auth.views import logout_then_login
from django.core.mail import EmailMessage


from .models import Positions, Vote, Choice
from .tokens import account_activation_token
from .forms import SignupForm

# Create your views here.

class VoteView(LoginRequiredMixin, generic.ListView):
	model = Positions

	context_object_name = 'positions_list'

	template_name = 'polls/vote.html'

	def get_query_set(self):
		return Positions.objects.all()

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['previous_votes'] = [prev_vote.vote for prev_vote in Vote.objects.filter(voter=self.request.user)]

		return context

	def post(self, request):
		choices = ['choicePR', 'choiceVP', 'choiceHG']

		prev_votes = Vote.objects.filter(voter=request.user)

		try:
			for choice in choices:
				print(request.POST[choice])
				if request.POST[choice] != "0":
					pos_choice = Choice.objects.get(pk=request.POST[choice])
					pos_choice.number_of_votes += 1
					pos_choice.save()

					vote = Vote(vote=pos_choice, voter=request.user)
					vote.save()

		except IntegrityError:
			return HttpResponse("yey")

		except (KeyError, Choice.DoesNotExist):
			return render(request, self.template_name, {'positions_list': self.get_query_set(),
														'error_message': "Please select a choice for all position"})
		
		return HttpResponse('Thank you for voting!')


def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			print('here1') 
			user = form.save(commit=False)
			print('here2')
			user.is_active = False
			print('here3')
			user.save()
			current_site = get_current_site(request)
			mail_subject = 'Activate your account.'
			message = render_to_string('polls/acc_active_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
				'token':account_activation_token.make_token(user),
			})
			to_email = form.cleaned_data.get('email')
			email = EmailMessage(
						mail_subject, message, to=[to_email]
			)
			email.send()
			return HttpResponse('Please confirm your email address in your mailbox to complete the registration')
	else:
		form = SignupForm()
	print('here')
	return render(request, 'polls/signup.html', {'form': form})



def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		# return redirect('home')
		return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
	else:
		return HttpResponse('Activation link is invalid!')

def logoutin(request):
	return logout_then_login(request)