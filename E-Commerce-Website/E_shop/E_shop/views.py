from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from app.models import Category,Product,Contact_us,Order,Brand

from django.contrib.auth import authenticate
from django.contrib.auth import login
from app.models import UserCreateForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from cart.cart import Cart

from django.contrib.auth import logout
from django.shortcuts import redirect

from app.models import Blog

from app.models import Blog




def master(request):
    return render(request,'master.html')


def index(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
    categoryID = request.GET.get('category')

    if categoryID:
        product = Product.objects.filter(sub_category = categoryID).order_by('-id')
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product = Product.objects.all()


    context = {
        'category':category,
        'product':product,
        'brand':brand
    }
    return render(request,'index.html',context)


def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()  # Save the user instance
            login(request, new_user)  # Log in the user directly
            return redirect('index')  # Redirect to home page
    else:
        form = UserCreateForm()

    context = {
        'form': form,
    }
    return render(request, 'registration/signup.html', context)


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

def custom_logout(request):
    logout(request)
    return redirect('index')  # Redirect to the home page

def Contact_Page(request):
    if request.method == "POST":
        contact = Contact_us(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )
        contact.save()
    return render(request,'contact.html')

def CheckOut(request):
    if request.method == "POST":
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        cart = request.session.get('cart')
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(pk = uid)

        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['quantity']
            total = a*b
            order = Order(
                user = user,
                product = cart[i]['name'],
                price = cart[i]['price'],
                quantity = cart[i]['quantity'],
                image = cart[i]['image'],
                address = address,
                phone = phone,
                pincode = pincode,
                total = total,
            )
            order.save()
        request.session['cart']={}
        return redirect('index')

    return HttpResponse("this is checkout page")

def Your_Order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(pk=uid)
    order = Order.objects.filter(user = user)
    context = {
        'order':order,
    }
    return render(request,'order.html',context)


def Product_page(request):
    category = Category.objects.all()
    brand = Brand.objects.all()
    brandID = request.GET.get('brand')
    categoryID = request.GET.get('category')

    if categoryID:
        product = Product.objects.filter(sub_category=categoryID).order_by('-id')
    elif brandID:
        product = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product = Product.objects.all()
    context = {
        'category':category,
        'brand':brand,
        'product':product,
    }
    return render(request,'product.html',context)

def Search(request):
    query = request.GET.get('query', '')  # Safely get the 'query' parameter with a default value
    product = Product.objects.filter(name__icontains=query) if query else []  # Search products if query exists
    context = {
        'product': product,
    }
    return render(request, 'search.html', context)

def blog_list(request):
    blogs = Blog.objects.filter(is_published=True).order_by('-published_date')
    return render(request, 'blog.html', {'blogs': blogs})


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog_detail.html', {'blog': blog})


def Product_Datil(request,id):
    product= Product.objects.filter(id = id).first()
    context ={
        'product':product
    }
    return render(request,'product_detail.html',context)