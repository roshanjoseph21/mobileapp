from django.shortcuts import render,redirect
from mobile.forms import MobileForm,RegistrationForm,LoginForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator
# Create your views here.
from django.views.generic import View
from mobile.models import Mobiles

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"Sign in required")
            return redirect("signin")
        else:
            return fn(request,*args, **kwargs)
    return wrapper

@method_decorator(signin_required,name="dispatch")
class MobileListView(View):
    def get(self,request,*args,**kwargs):
        qs=Mobiles.objects.all()
        print(request.GET)
        if "brand" in request.GET: 
            brand=request.GET.get("brand")
            qs=qs.filter(brand__iexact=brand)
        
        if "display" in request.GET: 
            display=request.GET.get("display")
            qs=qs.filter(display__iexact=display)

        return render(request,"mobile_list.html",{"data":qs})
    
        
@method_decorator(signin_required,name="dispatch")
class MobileDetailView(View):
    def get(self,request,*args,**kwargs):
        # if not request.user.is_authenticated:
        #     return redirect(("signin"))
        id=kwargs.get("pk")
        qs=Mobiles.objects.get(id=id)
        return render(request,"mobile_detail.html",{"data":qs})
    

@method_decorator(signin_required,name="dispatch")   
class MobileDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Mobiles.objects.filter(id=id).delete()
        messages.success(request,"mobile deleted")
        return redirect("mobile-all")
    

@method_decorator(signin_required,name="dispatch")
class MobileAddView(View):
    def get(self,request,*args,**kwargs):
        form=MobileForm()
        return render(request,"mobile_add.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=MobileForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"MOBILE ADDED")
            return redirect("mobile-all")
        else:
            messages.warning(request,"ERROR CREATING MOBILE")
            return render(request,"mobile_add.html",{"form":form})

    #localhost/mobile/{id}/update  
@method_decorator(signin_required,name="dispatch")
class MobileUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Mobiles.objects.get(id=id)
        form=MobileForm(instance=obj)
        return render(request,"mobile_update.html",{"form":form})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Mobiles.objects.get(id=id)
        form=MobileForm(request.POST,files=request.FILES,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,"MOBILE UPDATED")
            return redirect("mobile-all")
        else:
            messages.warning(request,"ERROR UPDATING MOBILE")
            return render(request,"mobile_update.html",{"form":form})

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            # form.save()
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"Account Created")
            return render(request,"register.html",{"form":form})
        else:
            messages.error(request,"Error Creating Account")
            return render(request,"register.html",{"form":form})



class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})  
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(uname,pwd)
            user_object=authenticate(request,username=uname,password=pwd)
            if user_object:
                print("valid credentials")
                login(request,user_object)
                print(request.user)
                return redirect("mobile-all")
            else:
                print("invalid credentials")
            return render(request,"login.html",{"form":form})
        else:
            return render(request,"login.html",{"form":form})

@method_decorator(signin_required,name="dispatch")        
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
        