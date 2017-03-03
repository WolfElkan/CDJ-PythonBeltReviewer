from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
# - - - - - HELPER FUNCTIONS - - - - -

# Function for initializing session variables.
def seshinit(request, sesh, val=''):
	if sesh not in request.session:
		request.session[sesh] = val

# - - - - - DEVELOPER VIEWS - - - - -

def hot(request):
	seshinit(request,'command')
	context = {
		# Models
		'command': request.session['command']
	}
	return render(request, "main/hot.html", context)

def run(request):
	command = request.POST['command']
	request.session['command'] = command
	exec(command)
	return redirect ('/hot')

def nuke(request):
	#.objects.all().delete()
	return redirect ('/hot')

# - - - - - APPLICATION VIEWS - - - - -

def index(request):
	context = {}
	return render(request, "main/index.html", context)
