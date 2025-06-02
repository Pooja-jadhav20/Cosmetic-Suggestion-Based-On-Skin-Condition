from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
from skincare_recommendation_app.models import Product
from skincare_recommendation_app.models import Function
from skincare_recommendation_app.models import ProductType
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import ensure_csrf_cookie

import json
from django.templatetags.static import static
from skincare_recommendation_app.utils import utils
from django.views import View

import os

class views(View):
    # Create your views here.
    def home(request):
        return render(request, 
        "admin/home.html", 
        {
            'name': 'Test',
            'date': datetime.now()
        })

    def about(request):
        return render(request, "public/about.html", {})

    def user_product(request):
        # Get List Product
        products = Product.objects.filter(category__icontains=request.GET.get("category"))

        returnProduct = []
        for product in products:
            temp = {
                    'name':product.name, 
                    'imagePath':product.image, 
                    'description':product.price,
                    'price':product.price,
                    'review':product.review,
                    'defaultImage':'assets/img/Logo-BINUS-University.jpg'
                }
            returnProduct.append(temp)

        returnProduct = Paginator(returnProduct, 6)

        totalData = returnProduct.count
        print("total data product : " + str(totalData))

        pageNum = 1
        if(totalData > 0): 
            pageNum = request.GET.get("page") if request.GET.get("page") else 1

        return JsonResponse({
                'products': list(returnProduct.page(pageNum)),
                'range': list(range(1, returnProduct.page(pageNum).paginator.num_pages + 1))
            })
        
    def user_home(request):
        if(request.method=='POST'):
            # Upload User File
            file_name = utils.upload_file(request.FILES.get("inputFile"))

            # get user skin condition 
            user_skin_condition = utils.get_user_skin_condition('skincare_recommendation_app' + static("user/upload/") + file_name)

            # Get List Product
            products = Product.objects.filter(category__icontains=user_skin_condition)

            returnProduct = []
            print("cek function id : ")
            for product in products:
                functionId = product.function.split(";")
                productFunction = []

                productDescription = None
                if (len(productFunction) > 0) :
                    productDescription = "This product is useful in dealing with <b> " + str(product.category.replace(";", ",")) + " </b> conditions. In addition, this product also has other benefits, namely for <b>" + ", ".join(productFunction) + "</b> "
                    # + str(",".join(','.join(l) for l in productFunction))

                temp = {
                        'name':product.name, 
                        'imagePath':product.image, 
                        'description':productDescription,
                        'price':product.price,
                        'review':product.review,
                        'defaultImage':'assets/img/Logo-BINUS-University.jpg'
                    }
                returnProduct.append(temp)

            returnProduct = Paginator(returnProduct, 6)

            totalData = returnProduct.count
            print("total data product : " + str(totalData))

            pageNum = 1
            if(totalData > 0): 
                pageNum = request.GET.get("page") if request.GET.get("page") else 1

            skinDescription = ""
            if (user_skin_condition == 'Wrinkles') :
                skinDescription = "Wrinkles "
            elif(user_skin_condition == 'Acne'):
                skinDescription = "Acne "
            elif(user_skin_condition == 'Blackhead'):
                skinDescription = "Blackhead "
            
            return render(request, 
                "public/home.html", 
                {
                    'name': 'Test',
                    'date': datetime.now(),
                    'title': 'Skincare Recommendation',
                    'skinDescription': skinDescription,
                    'userUploadImage': '/user/upload/' + file_name,
                    'userFileName': file_name,
                    'productCategory': user_skin_condition,
                    'products': returnProduct.page(pageNum),
                    'range': range(1, returnProduct.page(pageNum).paginator.num_pages + 1)
                })

        if (request.GET.get("page")):
            # Get List Product
            products = Product.objects.filter(category__icontains=request.GET.get("category"))
            print(products)

            returnProduct = []
            for product in products:
                functionId = product.function.split(";")
                productFunction = []

                for id in functionId:
                    if(id != ''):
                        productFunction.append(Function.objects.get(pk=id).name)

                productDescription = None
                if (len(productFunction) > 0) :
                    productDescription = "This product is useful in dealing with <b> " + str(product.category.replace(";", ",")) + " </b> conditions. In addition, this product also has other benefits, namely for <b>" + ", ".join(productFunction) + "</b> "
                    # + str(",".join(','.join(l) for l in productFunction))


                temp = {
                        'name':product.name, 
                        'imagePath':product.image, 
                        'description':productDescription,
                        'price':product.price,
                        'review':product.review,
                        'defaultImage':'assets/img/Logo-BINUS-University.jpg'
                    }
                returnProduct.append(temp)

            returnProduct = Paginator(returnProduct, 6)

            totalData = returnProduct.count
            print("total data product : " + str(totalData))

            pageNum = 1
            if(totalData > 0): 
                pageNum = request.GET.get("page") if request.GET.get("page") else 1
            
            skinDescription = ""
            if (request.GET.get("category") == 'Wrinkles') :
                skinDescription = "Wrinkles "
            elif(request.GET.get("category") == 'Acne'):
                skinDescription = "Acne "
            elif(request.GET.get("category") == 'Blackhead'):
                skinDescription = "Blackhead "

            return render(request, 
                "public/home.html", 
                {
                    'name': 'Test',
                    'date': datetime.now(),
                    'title': 'Skincare Recommendation',
                    'userUploadImage': ('/user/upload/' + request.GET.get('fileName')) if request.GET.get('fileName') else None,
                    'userFileName': request.GET.get('fileName'),
                    'skinDescription': skinDescription,
                    'productCategory': request.GET.get("category"),
                    'products': returnProduct.page(pageNum),
                    'range': range(1, returnProduct.page(pageNum).paginator.num_pages + 1)
                })
        
        return render(request, 
            "public/home.html", 
            {
                'name': 'Test',
                'date': datetime.now(),
                'title': 'Skincare Recommendation',
            })