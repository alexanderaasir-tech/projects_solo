from django.shortcuts import render, redirect, HttpResponse
import bcrypt
from django.contrib import messages
from .models import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    context = {
        "restaurant" : "AAD Bhavan",
        "menuitems" : ["Pizza", "Burger", "Pasta"]
    }
    return render(request, "index.html", context)

def create_user(request):
    print (request.POST['first_name'])
    if request.method == 'POST':
        errors = User.objects.create_validator(request.POST)
        #if the errors dictionary has any errors which is of len>0, then report it back on the index.html page
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
            # print (value)
            # print (request)
        return redirect('/')
    else:
        #bcrypt the password
        password = request.POST['password']
        # create the hash    
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
        print(pw_hash)
        #After decoding the password place all the fields in the User table
        user = User.objects.create(first_name = request.POST['first_name'],last_name = request.POST['last_name'], email= request.POST['email'], password = pw_hash)

        #Ensure the created user is also captured in the session    
        request.session['user_id'] = user.id
    
        return redirect('/dashboard')
    return redirect ('/')


def login(request):
    if request.method == "POST":
        users_with_email = User.objects.filter(email=request.POST['email'])
        #users_with_email comes as a list and using if statement will say it is true or false
        if users_with_email:
            user = users_with_email[0]
            #add bcrypt to encrypt
            if bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):
                #Capture the user in the session
                request.session['user_id'] = user.id
                return redirect ('/dashboard')
        messages.error(request,"Entered email or password is incorrect")
    return redirect('/')

def dashboard(request):
#Once the user logs out and hits the browser back button, the values seems to show as though the user is still logged in. However, refreshing the page will result in error. If the below check is made, then, we dont run into an error.
    if 'user_id' not in request.session:
        return redirect('/')

    for order in Order.objects.filter(user_order=User.objects.get(id=request.session['user_id'])):
        print (order)
    #Only context dict variables are used for rendering on the page.
    context = {
        'current_user' : User.objects.get(id=request.session['user_id']),
        'all_restaurants' : Restaurant.objects.all(),
        'my_restaurants' : Restaurant.objects.filter(owner=User.objects.get(id=request.session['user_id'])),
        'my_orders' : Order.objects.filter(user_order=User.objects.get(id=request.session['user_id'])),
        # 'my_order_list' : ['']
        # {% for one_restaurant in current_user.restaurant_created.all %}
        

    }
    return render(request,"dashboard.html", context)

    #Create a logout method from Dashboard.html page,
def logout(request):
    request.session.flush()
    return redirect('/')



def new_restaurant(request):
    context = {
        'current_user' : User.objects.get(id=request.session['user_id'])
    }
    return render(request,"restaurant.html",context)

def create_restaurant(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user' : User.objects.get(id=request.session['user_id'])
    }
    if request.method == "POST":
        print (request.POST['name'])
        # errors = Restaurant.objects.jobs_validator(request.POST)
        # #if the errors dictionary has any errors which is of len>0, then report it back on the index.html page
        # if len(errors) > 0:
        #     for key, value in errors.items():
        #         messages.error(request,value)
                
            # return render(request, "jobs.html",context)
        # else:
        restaurant = Restaurant.objects.create(name = request.POST['name'], description = request.POST['description'], location = request.POST['location'] ,owner=User.objects.get(id=request.session['user_id']))
        return redirect ('/dashboard')
    return redirect ('/')


def new_item(request,restaurant_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    context = {
        'current_user' : User.objects.get(id=request.session['user_id']),
        'current_restaurant' : Restaurant.objects.get(id=restaurant_id),
        'my_items' : Item.objects.filter(restaurant=restaurant_id)

    }
    return render(request,"item.html",context)

def create_item(request,restaurant_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'current_user' : User.objects.get(id=request.session['user_id']),
        'current_restaurant' : Restaurant.objects.get(id=restaurant_id)
    }
    if request.method == "POST":
        print (request.POST['item'])
        # errors = Restaurant.objects.jobs_validator(request.POST)
        # #if the errors dictionary has any errors which is of len>0, then report it back on the index.html page
        # if len(errors) > 0:
        #     for key, value in errors.items():
        #         messages.error(request,value)
                
            # return render(request, "jobs.html",context)
        # else:
        item = Item.objects.create(item = request.POST['item'], quantity = request.POST['quantity'],restaurant=Restaurant.objects.get(id=restaurant_id))
        return redirect ('/item/new/%s' % restaurant_id)
    return redirect ('/')

def delete_restaurant(request,restaurant_id):
    if 'user_id' not in request.session:
        return redirect('/')
    restaurant_to_delete = Restaurant.objects.get(id=restaurant_id)
    restaurant_to_delete.delete()
    return redirect('/dashboard')


def order_items(request,restaurant_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    context = {
        'current_user' : User.objects.get(id=request.session['user_id']),
        'current_restaurant' : Restaurant.objects.get(id=restaurant_id),
        'my_items' : Item.objects.filter(restaurant=restaurant_id)

    }
    return render(request,"menu.html",context)

@csrf_exempt
def add_items(request):
    if 'user_id' not in request.session:
        return redirect('/')
    if request.method == "POST":
        print (request.POST['item_order'])
        order = Order.objects.create(customer_qty = request.POST['customer_qty'],item_order = Item.objects.get(id = request.POST['item_order']) ,user_order=User.objects.get(id=request.session['user_id']))


        item_to_update = Item.objects.get(id = request.POST['item_order'])
        total_quantity = item_to_update.quantity
        current_quantity = total_quantity -  int(request.POST['customer_qty'])
        item_to_update.quantity = current_quantity
        item_to_update.save()

        restaurant_id = item_to_update.restaurant.id

        # return redirect('/restaurant/menu/restaurant_id')
        return redirect('/dashboard')
    return redirect ('/')

