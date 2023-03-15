**DRF**

pipenv install django

pipenv shell

django-admin startproject BookList .

python manage.py startapp BookListAPI

pipenv install djangorestframework

python manage.py runserver

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

**settings.py ->** 

INSTALLED\_APPS = [

`    `'rest\_framework',

`    `'BookListAPI',

]

**views.py ->** 

from django.shortcuts import render

from rest\_framework.response import Response

from rest\_framework import status

from rest\_framework.decorators import api\_view

from django.http import HttpResponse

@api\_view(['GET', 'POST'])		#Decorator

def books(request):

`    `return Response('list of the books', status=status.HTTP\_200\_OK)



**Create new class named urls.py in BookListAPI and write ->**

from django.urls import path

from . import views

urlpatterns = [

`    `path('books/', views.books),

]

**Open app-level urls.py and import include**

from django.urls import include, path

**Add endpoint ->**

urlpatterns = [

`    `path('api/', include('BookListAPI.urls')),

]

**Class-based views:**

**views.py ->** 

from rest\_framework.views import APIView

class BookList(APIView):

`    `def get(self, request):

`        `return Response({"message": "list of the books"}, status.HTTP\_200\_OK)

**BooklistAPI-level urls.py ->** 

urlpatterns = [

`    `path('books', views.BookList.as\_view()),

]

**views.py ->** 

`    `def post(self, request):

`        `return Response({"message": "new book created"}, status.HTTP\_201\_CREATED)


**To filter by aurhor name, again in views.py change the get method ->**

`    `def get(self, request):

`        `author = request.GET.get('author')

`        `if (author):

`            `return Response({"message": "list of the books by " + author}, status.HTTP\_200\_OK)

`        `return Response({"message": "list of the books"}, status.HTTP\_200\_OK)

**You can check it -> [http://127.0.0.1:8000/api/books/?author=Hemingway**]()**

**Modify post method to return the title from the payload(json or formurl data) ->**

`    `def post(self, request):

`        `return Response({"title": request.data.get('title')}, status.HTTP\_201\_CREATED)

**Accepting the primary key in the methods of class-based views, views.py ->**

class Book(APIView):

`    `def get(self, request, pk):

`        `return Response({"message": "single book with id " + str(pk)}, status.HTTP\_200\_OK)

`    `def put(self, request, pk):

`        `return Response({"title": request.data.get('title')}, status.HTTP\_200\_OK)

**Add a path in BankAPI-level urls.py ->**

`    `path('books/<int:pk>', views.Book.as\_view()),









**Django Debug Toolbar**

pipenv shell

pipenv install django-debug-toolbar

**settings.py ->** 

INSTALLED\_APPS = [

`    `'rest\_framework',

`    `'BookListAPI',

`    `'debug\_toolbar',

]

MIDDLEWARE = [

`    `'debug\_toolbar.middleware.DebugToolbarMiddleware',

]

#Add below code to the end of settings.py file:

INTERNAL\_IPS = [

`    `'127.0.0.1'

]

**App-level urls.py ->**

`    `path('\_\_debug\_\_/', include('debug\_toolbar.urls')),

**!!! ↓ If you’re getting text/plain error try these ↓ !!!**

1. **Try to run the server on different port (python manage.py runserver 7000)**
1. **In the registry Editor ("Ctrl+r" "regedit") find HKEY\_CLASSES\_ROOT/.js then double click on the "Content Type" the "Value data" should be "text/javascript" or “application/javascript”**
1. **Try cleaning up your browser cache.**





**LittleLemonAPI Project**

pipenv install django

pipenv shell

django-admin startproject LittleLemon .

python manage.py startapp LittleLemonAPI

pipenv install djangorestframework

**settings.py ->** 

INSTALLED\_APPS = [

`    `'rest\_framework',

`    `'LittleLemonAPI',

]

**models.py ->** 

class MenuItem(models.Model):

`    `title = models.CharField(max\_length=255)

`    `price = models.DecimalField(max\_digits=6, decimal\_places=2)

`    `inventory = models.SmallIntegerField()

**Open new file named serializers.py and add the following code->** 

from rest\_framework import serializers

from .models import MenuItem

class MenuItemSerializer(serializers.ModelSerializer):

`    `class Meta:

`        `model = MenuItem

`        `fields = ['id', 'title', 'price', 'inventory']

**Serializers help to convert model instances into python data types that can be displayed as JSON or XML. It also helps to convert HTTP body into python data types and map them to model instances.** 

**views.py ->** 

from rest\_framework import generics

from .models import MenuItem

from .serializers import MenuItemSerializer

class MenuItemsView(generics.ListCreateAPIView):

`    `queryset = MenuItem.objects.all()			#Retrieves all the records

`    `serializer\_class = MenuItemSerializer		#Displays and stores the records

**Create a new file named urls.py at LittleLemonAPI-level and add ->** 

from django.urls import path

from . import views

urlpatterns = [

`    `path('menu-items/', views.MenuItemsView.as\_view()),

]

**App-level urls.py ->**

urlpatterns = [

`    `path('api/', include('LittleLemonAPI.urls')),

]

**Run the web server and try …/api/menu-items-> python manage.py runserver**

**Add some data and POST.**

**Displaying Single Record:**

**views.py ->**

class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):

`    `queryset = MenuItem.objects.all()

`    `serializer\_class = MenuItemSerializer

**RetrieveUpdateView class has everything to fetch a record, display it, and accept post calls to update them and DestroyApiView, has everything to accept, delete calls, and finally, delete a record.**

**Map the new class in LittleLemonAPI-level urls.py and try it running the server ->**

urlpatterns = [

`    `path('menu-items/<int:pk>', views.SingleMenuItemView.as\_view()) ]

**Convert booklist API project to DRF**

**Create a 'urls.py' file at the app level, add the path()  ->**

urlpatterns = [

`    `path('books', views.BookView.as\_view()),

]

**Project level urls.py  ->**

from django.urls import include

urlpatterns = [

`    `path('api/', include('BookListAPI.urls')),

]

**models.py  ->**

class Book(models.Model):

`    `title = models.CharField(max\_length=255)

`    `author = models.CharField(max\_length=255)

`    `price = models.DecimalField(max\_digits=5, decimal\_places=2)

**Now create a file called serializers.py inside the app level BookListAPI  ->**

from .models import Book

from rest\_framework import serializers

class BookSerializer(serializers.ModelSerializer):

`    `class Meta:

`        `model = Book

`        `fields = ['id', 'title', 'author', 'price']

**views.py  ->**

from .models import Book

from .serializers import BookSerializer

from rest\_framework import generics

class BookView(generics.ListCreateAPIView):

`    `queryset = Book.objects.all()

`    `serializer\_class = BookSerializer


**Single Item View (for example api/books/1 endpoint):**

**views.py  ->**

class SingleBookView(generics.RetrieveUpdateAPIView):

`    `queryset = Book.objects.all()

`    `serializer\_class = BookSerializer

**App-level urls.py  ->**

urlpatterns = [

`    `path('books/<int:pk>', views.SingleBookView.as\_view()),

]





















**Serializers (LittleLemonAPI)**

**views.py  ->**

from .models import MenuItem

from rest\_framework.decorators import api\_view

from rest\_framework.response import Response

@api\_view()

def menu\_items(request):

`    `items = MenuItem.objects.all()

`    `return Response(items.values())

**Create a new file named serializers.py and add  ->**

from rest\_framework import serializers

class MenuItemSerializer(serializers.Serializer):

`    `id = serializers.IntegerField()

`    `title = serializers.CharField(max\_length=255)

**Use the serializer in views.py  ->**

from .serializers import MenuItemSerializer

@api\_view()

def menu\_items(request):

`    `items = MenuItem.objects.all()

`    `serialized\_item = MenuItemSerializer(items, many=True)

`    `return Response(serialized\_item.data)

**Add price and inventory fields to the serializer to be shown in calls, serializers.py  ->**

class MenuItemSerializer(serializers.Serializer):

`    `id = serializers.IntegerField()

`    `title = serializers.CharField(max\_length=255)

`    `price = serializers.DecimalField(max\_digits=6, decimal\_places=2)

`    `inventory = serializers.IntegerField()


**Single Item View:**

**Add a method for single item calls in views.py  ->**

@api\_view()

def single\_item(request, id):

`    `item = MenuItem.objects.get(pk=id)

`    `serialized\_item = MenuItemSerializer(item)

`    `return Response(serialized\_item.data)

**Map the single item method in App-level urls.py  ->**

urlpatterns = [

`    `path('menu-items/<int:id>', views.single\_item),

]

**To get more friendly (Json error message) error change the single item method,  views.py  ->**

from django.shortcuts import get\_object\_or\_404			#import this first

@api\_view()

def single\_item(request, id):

`    `item = MenuItem.objects.get(pk=id) à item = get\_object\_or\_404(MenuItem,pk=id)

`    `serialized\_item = MenuItemSerializer(item)

`    `return Response(serialized\_item.data)










**Model Serializers (LittleLemon)**

**serializers.py  ->** 

from .models import MenuItem

class MenuItemSerializer(serializers.ModelSerializer):

`    `class Meta:

`        `model = MenuItem

`        `fields = ['id', 'title', 'price', 'inventory']

**If you want to change the name of a field, for example, inventory to stock serializers.py    ->**

class MenuItemSerializer(serializers.ModelSerializer):

`    `stock = serializers.IntegerField(source='inventory')	#New field linked to inv.

`    `class Meta:

`        `model = MenuItem

`        `fields = ['id', 'title', 'price', 'stock']	#‘stock’ instead of inv.

**Add a new method called calculate\_tax to calculate price with tax (10% tax)	->**

`    `def calculate\_tax(self, product: MenuItem):

`        `return product.price \* Decimal(1.1)

**Link the new method as a new field (price\_after\_tax) in the serializer, serializers.py	->**

class MenuItemSerializer(serializers.ModelSerializer):

`    `stock = serializers.IntegerField(source='inventory')

`    `price\_after\_tax = serializers.SerializerMethodField(method\_name =    'calculate\_tax')

`    `class Meta:

`        `model = MenuItem

`        `fields = ['id', 'title', 'price', 'stock', 'price\_after\_tax']







**Relationship serializers (LittleLemon)**

**New Category model, models.py	->**

class Category(models.Model):

`    `slug = models.SlugField()

`    `title = models.CharField(max\_length=255)

**Then connect it to MenuItem Model, models.py	->**

class MenuItem(models.Model):

`    `title = models.CharField(max\_length=255)

`    `price = models.DecimalField(max\_digits=6, decimal\_places=2)

`    `inventory = models.SmallIntegerField()

`    `category = models.ForeignKey(Category, on\_delete=models.PROTECT, default=1)

**on\_delete=models.PROTECT = Category cannot be deleted befora all related menu items deleted.**

**!! The row in table 'LittleLemonAPI\_menuitem' with primary key '1' has an invalid foreign key: LittleLemonAPI\_menuitem.category\_id contains a value '1' that does not have a corresponding value in LittleLemonAPI\_category.id. !!**

**!! If you’re getting this error, delete all the migration files exept \_\_init\_\_.py and also delete db.sqlite3. Then do migrations again !!**

**Add the category field to the serializer, serializers.py	->**

class MenuItemSerializer(serializers.ModelSerializer):

...

`    `class Meta:

`        `model = MenuItem

`        `fields = ['id', 'title', 'price', 'stock', 'price\_after\_tax', 'category']

**Display the category name using Relationship Serializer:**

**serializers.py	->**

from .models import MenuItem, Category

class MenuItemSerializer(serializers.ModelSerializer):

`    `stock = serializers.IntegerField(source='inventory')

`    `price\_after\_tax = serializers.SerializerMethodField(

`        `method\_name='calculate\_tax')

`    `category = serializers.StringRelatedField()


**Add a method for string conversion in models.py	->**

class Category(models.Model):

`    `slug = models.SlugField()

`    `title = models.CharField(max\_length=255)

`    `def \_\_str\_\_(self) -> str:

`        `return self.title


**Converting a connected model to string, you also need to change your view files to load the related model in a single SQL code. This will make your API more efficient by not running a separate SQL query for every item to load to the relative data. So change the menu\_items() method.							 		  views.py	 ->**

@api\_view()

def menu\_items(request):

`    `items = MenuItem.objects.select\_related('category').all()

`    `serialized\_item = MenuItemSerializer(items, many=True)

`    `return Response(serialized\_item.data)

**Add a new Category Serializer above the MenuItemSerializer in serializers.py	->**

class CategorySerializer(serializers.ModelSerializer):

`    `class Meta:

`        `model = Category

`        `fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):

...

**Add this Category Serializer in MenuItemSerializer,		serializers.py	->**

class MenuItemSerializer(serializers.ModelSerializer):

`    `stock = serializers.IntegerField(source='inventory')

`    `price\_after\_tax = ...

`    `category = serializers.StringRelatedField() -> category = CategorySerializer()




**Deserialization (POST methods) and Validation ()**

**Modify the menu-items method to accept also POST calls in	views.py  ->**

@api\_view(['GET', 'POST'])

def menu\_items(request):

`    `if request.method == 'GET':

`        `items = MenuItem.objects.select\_related('category').all()

`        `serialized\_item = MenuItemSerializer(items, many=True)

`        `return Response(serialized\_item.data)

`    `if request.method == 'POST':

`        `serialized\_item = MenuItemSerializer(data=request.data)

`        `serialized\_item.is\_valid(raise\_exception=True)

`        `# serialized\_item.\_validated\_data     # Accessing validated data

`        `serialized\_item.save()  # Saving the record in the database

`        `# Access the method after saving it (You can't without save!)

`        `return Response(serialized\_item.data, status.HTTP\_201\_CREATED)

**We can’t add an item without category field filled so we should modify MenuItemSerializer category field to add item without category field ,  			serializers.py	->**

class MenuItemSerializer(serializers.ModelSerializer):

`    `stock = serializers.IntegerField(source='inventory')

`    `price\_after\_tax = ...

`    `category = CategorySerializer() -> category=CategorySerializer(read\_only=True)

**Now it works but the records are stored in database with category id == 1.**

**To save a menu item with a different category id:**

**Modify MenuItemSerializer,							serializers.py	->**

class MenuItemSerializer(serializers.ModelSerializer):

`    `stock = serializers.IntegerField(source='inventory')

`    `price\_after\_tax = ...

`    `category = CategorySerializer(read\_only=True)

`    `category\_id = serializers.IntegerField()

`    `class Meta:

`        `model = MenuItem

`        `fields = ['id', 'title', 'price', 'stock',

`                  `'price\_after\_tax', 'category', 'category\_id']

**Now there are 2 different fields in database. Category and category\_id. There is a category\_id field in Category so we should make the separate category\_id hidden from only api GET calls.**

**The solution is to make it write only.					serializers.py ->**

class MenuItemSerializer(serializers.ModelSerializer):

`    `stock = serializers.IntegerField(source='inventory')

`    `price\_after\_tax = ...

`    `category = CategorySerializer(read\_only=True)

`    `category\_id = serializers.IntegerField(write\_only=True)

**!! Because I have deleted my database information now I don’t have any category which I can’t add any item without category!!**

**!! To solve this I created a new method and endpoint for just category calls. !!**

`    `**views.py ->**

from .models import MenuItem, Category

from .serializers import MenuItemSerializer, CategorySerializer


@api\_view(['GET', 'POST'])

def categories(request):

`    `if request.method == 'GET':

`        `items = Category.objects.all()

`        `serialized\_item = CategorySerializer(items, many=True)

`        `return Response(serialized\_item.data)

`    `if request.method == 'POST':

`        `serialized\_item = CategorySerializer(data=request.data)

`        `serialized\_item.is\_valid(raise\_exception=True)

`        `# serialized\_item.\_validated\_data     # Accessing validated data

`        `serialized\_item.save()  # Save the record in the database

`        `# Access the method after saving it (You can't without save!)

`        `return Response(serialized\_item.data, status.HTTP\_201\_CREATED)

@api\_view()

def single\_category(request, id):

`    `item = get\_object\_or\_404(Category, pk=id)

`    `serialized\_item = CategorySerializer(item)

`    `return Response(serialized\_item.data)
**


**app-level urls.py ->**

urlpatterns = [

`    `path('categories/', views.categories),

`    `path('categories/<int:id>', views.single\_category),

]

**Because I already have a category serializer and a category model, I just added GET and POST method in views.py and a path for them in app-level urls.py. After this I just added categories and menu items with category id on POST calls**





















**Renderers**

`  `**Add settings to initialize renderers at the end of settings.py ->**

REST\_FRAMEWORK = {

`    `'DEFAULT\_RENDERER\_CLASSES': [

`        `'rest\_framework.renderers.JSONRenderer',

`        `'rest\_framework.renderers.BrowsableAPIRenderer',

`    `]

}

**JSON Renderer accepts application/json header. Now, comment the BrowsableAPIRenderer and run the server. You’ll see a JSON result. With BrowsableAPIRenderer it will accept text/html and you’ll get the result you were getting all the time.**

**For XML Renderer, you must install djangorestframework-xml package on terminal.**

**(pipenv install djangorestframework-xml) Then add it to 				settings.py ->**

REST\_FRAMEWORK = {

`    `'DEFAULT\_RENDERER\_CLASSES': [

...

`        `'rest\_framework\_xml.renderers.XMLRenderer',

`    `] }

**XML Renderer accepts application/xml header.**

**Types of Renderers:**

- **BrowsableAPI Renderer**
- **JSON Renderer**
- **XML Renderer**
- **TemplateHTML Renderer**
- **StaticHTMLRenderer**
- **CSV Renderer**
- **YAML Renderer**



**extra\_kwargs:  Basic form validation**

`											`**serializer.py ->**

class MenuItemSerializer(serializers.ModelSerializer):



...

`    `class Meta:

`        `model = MenuItem

`        `fields = ['id', 'title', 'price', 'stock',

`                  `'price\_after\_tax', 'category', 'category\_id']

`        `extra\_kwargs = {

`            `'price': {'min\_value': 2},

`		`'stock': {'source': 'inventory', 'min\_value': 0},

`        `}

**Adding an item with price lower than 2 won’t be available in this situation. We will get an error:**





**!! Please keep in mind that, if the field has already been explicitly declared on the serializer class, then the extra\_kwargs option will be ignored !!**

**Generic View**

**Modified every view method using generic view:					  views.py ->**

from rest\_framework import generics


class MenuItemsView(generics.ListCreateAPIView):

`    `queryset = MenuItem.objects.all()

`    `serializer\_class = MenuItemSerializer

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):

`    `queryset = MenuItem.objects.all()

`    `serializer\_class = MenuItemSerializer

class CategoriesView(generics.ListCreateAPIView):

`    `queryset = Category.objects.all()

`    `serializer\_class = CategorySerializer

class SingleCategoryView(generics.RetrieveUpdateDestroyAPIView):

`    `queryset = Category.objects.all()

`    `serializer\_class = CategorySerializer

**Also modified url patterns because the change of the view methods 	  app-level urls.py ->**

urlpatterns = [

`    `path('menu-items/', views.MenuItemsView.as\_view()),

`    `path('menu-items/<int:pk>', views.SingleMenuItemView.as\_view()),

`    `path('categories', views.CategoriesView.as\_view()),

`    `path('categories/<int:pk>', views.SingleCategoryView.as\_view()),

]








**Filtering**

**To use filtering and searching I get back to the old views instead of generic ones.**

**Modify menu\_items method,							  views.py ->**

@api\_view(['GET', 'POST'])

def menu\_items(request):

`    `if request.method == 'GET':

`        `items = MenuItem.objects.select\_related('category').all()

`        `category\_name = request.query\_params.get('category')

`        `to\_price = request.query\_params.get('to\_price')

`        `if category\_name:

`            `items = items.filter(category\_\_title=category\_name)

`        `if to\_price:

`            `items = items.filter(price=to\_price)

`        `serialized\_item = MenuItemSerializer(items, many=True)

`        `return Response(serialized\_item.data)

...

**The double underscore (\_\_) in category\_\_title means that title field belongs to category model and is linked to MenuItem model. Double underscore need to be used between model and the field to filter a linked model. Like a category inside the menu item.**  

items = items.filter(price=to\_price) 

**We can use price\_\_lte=to\_pice here which \_\_lte means less than or equal to. (Field Lookups) 
While price filter is working fine category filter doesn’t. I found that the problem was category title starts with an Uppercase. I tried category\_\_slug=category\_name and it worked.**

**To solve this, I made category\_\_title case-insensitive. I used a field lookup like category\_\_title\_\_iexact to make the query case-insensitive with \_\_iexact.**

**Now it is possible to filter using endpoints:**

**…/api/menu-items/?to\_price=3**

**…/api/menu-items/?category=cake**




**Searching**

**Modify menu\_items method,							  views.py ->**

@api\_view(['GET', 'POST'])

def menu\_items(request):

`    `if (request.method == 'GET'):

`        `items = MenuItem.objects.select\_related('category').all()

`        `category\_name = request.query\_params.get('category')

`        `to\_price = request.query\_params.get('to\_price')

`        `search = request.query\_params.get('search')

`        `if (category\_name):

`            `items = items.filter(category\_\_title\_\_iexact=category\_name)

`        `if (to\_price):

`            `items = items.filter(price\_\_lte=to\_price)

`        `if (search):

`            `items = items.filter(title\_\_startswith=search)

`        `serialized\_item = MenuItemSerializer(items, many=True)

`        `return Response(serialized\_item.data)

**\_\_contains lookup can also be used to search if those characters are present anywhere in the title.**

`            `items = items.filter(title\_\_contains=search)

**It is also possible to make \_\_contains and \_\_startswith case insensitive. Case insensitive versions are \_\_icontains and \_\_istartswith.**

**Now try search endpoints like:**

**…/api/menu-items/?search=chocolate or …/api/menu-items/?search=beef**







**Ordering**

@api\_view(['GET', 'POST'])

def menu\_items(request):

`    `if (request.method == 'GET'):

`        `items = MenuItem.objects.select\_related('category').all()

`        `category\_name = request.query\_params.get('category')

`        `to\_price = request.query\_params.get('to\_price')

`        `search = request.query\_params.get('search')

`        `ordering = request.query\_params.get('ordering')

`        `if (category\_name):

`            `items = items.filter(category\_\_title\_\_iexact=category\_name)

`        `if (to\_price):

`            `items = items.filter(price\_\_lte=to\_price)

`        `if (search):

`            `items = items.filter(title\_\_istartswith=search)

`        `if ordering:

`            `items = items.order\_by(ordering)

**Try: …/api/menu-items/?ordering=price**

**This makes ordering in an ascending fashion. To change it from ascending to descending you can just change ordering=price to ordering=-price.**

**To be able to order with 2 fields like price and inventory like: (…/api/menu-items/?ordering=price,inventory)**

**Modify the ordering if clause like this:**

@api\_view(['GET', 'POST'])

def menu\_items(request):

`    `if (request.method == 'GET'):

...



`        `if ordering:

`            `ordering\_fields = ordering.split(",")

`            `items = items.order\_by(\*ordering\_fields)

**Try:**

**(…/api/menu-items/?ordering=price,inventory)**

**(…/api/menu-items/?ordering=price,-inventory)**

**(…/api/menu-items/?ordering=price,inventory)**

**Pagination**

**views.py ->**

from django.core.paginator import Paginator, EmptyPage

@api\_view(['GET', 'POST'])

def menu\_items(request):

`    `if (request.method == 'GET'):

`        `items = MenuItem.objects.select\_related('category').all()

`        `category\_name = request.query\_params.get('category')

`        `to\_price = request.query\_params.get('to\_price')

`        `search = request.query\_params.get('search')

`        `ordering = request.query\_params.get('ordering')

`        `perpage = request.query\_params.get('perpage', default=2)

`        `page = request.query\_params.get('page', default=1)

`        `if category\_name:

`            `items = items.filter(category\_\_title\_\_iexact=category\_name)

`        `if to\_price:

`            `items = items.filter(price\_\_lte=to\_price)

`        `if search:

`            `items = items.filter(title\_\_istartswith=search)

`        `if ordering:

`            `ordering\_fields = ordering.split(",")

`            `items = items.order\_by(\*ordering\_fields)

`        `paginator = Paginator(items, per\_page=perpage)

`        `try:

`            `items = paginator.page(number=page)

`        `except EmptyPage:

`            `items = []

`        `serialized\_item = MenuItemSerializer(items, many=True)

`        `return Response(serialized\_item.data)

**Now, visiting the menu-items page we get first page with 2 items listed, the default values.**

**And these queries will work as it should:**

**…/api/menu-items/?perpage=3&page=1**

**…/api/menu-items/?perpage=4&page=2**

**Implementing pagination enables APIs to send results in smaller chunks.**

**Caching**

**Caching is a technique of serving saved results instead of creating a fresh one every time it is requested.**

`			   `**↑ Cachning can be done on these layers ↑**

**Database Server Caching: Uses query cache where the SQL queries and their result are stored in the memory.**

**Web Server Caching: Server-side scripts cache the result in a separate cache storage which could be simple files, or a database, or in caching tools like Redis, or Memcached, which can save you from connecting to the database every time.**

**Reverse Proxy Server Caching: Traffic heavy applications use multiple web servers behind reverse proxies to distribute the requests evenly. The web server can send responses with appropriate caching headers, and the reverse proxy then caches the result for a certain amount of time, as mentioned in those headers. They then serve the request straight from the cache.**

**Client-Side Caching: Reverse proxies or web servers can send responses with caching headers, which tell the client to cache the request for a specific time. During this time, if a request is made the client browser or application decides whether it will use those caching headers, serve the result from a local cache, or create a call to your server. Since this is a client-side behavior where you may not have complete control, it's always a good idea to implement the proper caching strategy on the server side.**




**Token-based Authentication in DRF**

**settings.py ->**

INSTALLED\_APPS = [

...

`    `'rest\_framework',

`    `'rest\_framework.authtoken',

`    `'LittleLemonAPI',

]

**python manage.py migrate**

**python manage.py createsuperuser		->	  Creating an admin user**

**Enter username and password**

**Go to …/admin/ and login with super user information. Then try to create a token.**

**Creating a protected API endpoint:**

`   `**End of views.py ->**

@api\_view()

def secret(request):

`    `return Response({"message": "Some secret message"})

`  `**App-level urls.py ->**

`    `urlpatterns = [path('secret/', views.secret)]

**Endpoint = …/api/secret**

**This endpoint will show the secret message to everyone. To make it shown just for token verified users modify the method secret:						  views.py ->**

from rest\_framework.decorators import api\_view, permission\_classes

from rest\_framework.permissions import IsAuthenticated

@api\_view()

@permission\_classes([IsAuthenticated])

def secret(request):

`    `return Response({"message": "Some secret message"})

**Now we will get <Authentication credentials were not provided> message at the same endpoint without being verified user.**

**Also, add this in settings.py to tell DRF to use token based authentication:**

REST\_FRAMEWORK = {

`    `'DEFAULT\_RENDERER\_CLASSES': [

...

`    `],

`    `'DEFAULT\_AUTHENTICATION\_CLASSES': (

`        `'rest\_framework.authentication.TokenAuthentication',

`    `),

}

**Copy the token that you have created and add it to Authorization tab in Insomnia or Postman.**

**Try the …/api/secret endpoint again with this token and you’ll get the secret message.**

**!! In Postman its own Bearer Token Authorization tab doesn’t work !!**

**You have to add the token like this:**


**To be able to generate tokens from an API endpoint:**

**App-level urls.py ->**

from rest\_framework.authtoken.views import obtain\_auth\_token    

urlpatterns = [path('api-token-auth/', obtain\_auth\_token)]



**Now we are able to create token entering admin information with this endpoint:**


**If you create a new user from the Django admin panel, or via code, you can always use the endpoint /api/api-token-auth to authenticate them and generate a token.** **Then use this token to make HTTP calls to the protected URLs.**











**User roles**

**Open the django admin panel from http://127.0.0.1:8000/admin/ and log in as the super user.**

**Create Group:**

**Name it Manager and save.**

**Create 2 Users:**

**(username:password)**

**johndoe:user1234**

**jimmydoe:user1234**

**Add Personal information to John and assign him the Manager group:**

**Now create a new view method just for Manager role:				  views.py ->**

@api\_view()

@permission\_classes([IsAuthenticated])

def manager\_view(request):

`    `return Response({"message": "Only Manager should see this!"})

**Then, map it in the urls.py file: 							  views.py ->**

urlpatterns = [path('manager-view/', views.manager\_view)]

**Let's log in as John Doe and create a token, also create a token for Jimmy Doe too:**

**Send a get call to the manager-view endpoint with John Doe’s token and you’ll see the response message because John is a Manager:**

**Send another get call to the manager-view endpoint with Jimmy Doe’s token and you’ll see the response message again eventhough Jimmy is not Manager.** 

**To fix this rewrite the manager-view method in the views.py:		        views.py ->**

@api\_view()

@permission\_classes([IsAuthenticated])

def manager\_view(request):

`    `if request.user.groups.filter(name='Manager').exists():

`        `return Response({"message": "Only Manager should see this!"})

`    `else:

`        `return Response({"message": "You are not authorized."}, 403)

**Now try again …/api/manager-view/ endpoints with John’s and Jimmy’s tokens again and you will see that it is working as it should work.**







**API Throttling**

- **User Throttling for Authenticated Users (With Token header)**
- **Anonymous Throttling for Unauthenticated Users (Without Token header)**

`  `**views.py ->**

@api\_view()

def throttle\_check(request):

`    `return Response({"message": "Successful."})

`  `**App-level urls.py ->**

`    `urlpatterns = [path('throttle-check/', views.throttle\_check)]

**Limit this endpoint for anonymous users to two calls per minute 		  views.py ->**

from rest\_framework.throttling import AnonRateThrottle

from rest\_framework.decorators import api\_view, throttle\_classes

@api\_view()

@throttle\_classes([AnonRateThrottle])

def throttle\_check(request):

`    `return Response({"message": "Successful."})

` `**settings.py ->**

REST\_FRAMEWORK = {

...

`    `'DEFAULT\_THROTTLE\_RATES': {

`        `'anon': '2/minute',

`    `} }

**Now if you refresh …/api/throttle-check/ endpoint 3 times in a minute it will show a message:**

**Change DEFAULT\_THROTTLE\_RATES for anon to 20/day**

**Throttling an endpoint for an anonymous users to 20 calls per day:            views.py ->**

from rest\_framework.throttling import AnonRateThrottle, UserRateThrottle

@api\_view()

@permission\_classes([IsAuthenticated])

@throttle\_classes([UserRateThrottle])

def throttle\_check\_auth(request):

`    `return Response({"message": "Only logged in users can see this."})

**App-level urls.py ->**

`    `urlpatterns = [path('throttle-check-auth/', views.throttle\_check\_auth)]

**settings.py ->**

REST\_FRAMEWORK = {

...

`    `'DEFAULT\_THROTTLE\_RATES': {

`        `'anon': '2/minute',

`        `'user': '5/minute',

`    `} }

**After 5 calls with John Doe’s token:**
**


**With the current setting, when you use throttling classes, all API endpoints will be limited to two calls per minute for the anonymous users and five calls per minute for the authenticated users.**

**To make another policy for some API endpoints so that authenticated users can call them 10 times per minute:**

**Create a new file called throttles.py and insert this code:** 

from rest\_framework.throttling import UserRateThrottle

class TenCallsPerMinute(UserRateThrottle):

`    `scope = 'ten'

**settings.py ->**

REST\_FRAMEWORK = {

...

`    `'DEFAULT\_THROTTLE\_RATES': {

`        `'anon': '2/minute',

`        `'user': '5/minute',

`        `'ten': '10/minute',

`    `} }

**Modify throttle\_check\_auth method’s throttle\_classes 			        views.py ->**

from .throttles import TenCallsPerMinute

@api\_view()

@permission\_classes([IsAuthenticated])

@throttle\_classes([TenCallsPerMinute])

def throttle\_check\_auth(request):

`    `return Response({"message": "Only logged in users can see this."})

**Now we’re getting this message after 10 calls with John Doe’s Token:**

**DJOSER**

**pipenv install djoser**

**settings.py ->**

INSTALLED\_APPS = [    ...

'djoser',]

**it's important that you keep Djoser after the rest\_framework app in INSTALLED\_APPS.**

**Add this config code at the end of 							 settings.py ->**

DJOSER = {

`    `"USER\_ID\_FIELD": "username",

}

**↑ This is how you specify which field in your user model will act as the primary key ↑**

**To use the Django admin login simultaneously with a browsable API view of Djoser, you need to add this session authentication class:**

`    `'DEFAULT\_AUTHENTICATION\_CLASSES': (

`        `'rest\_framework.authentication.TokenAuthentication',

`        `'rest\_framework.authentication.SessionAuthentication',

`    `),

`     `**Project-level urls.py ->**

urlpatterns = [

`    `path('auth/', include('djoser.urls')),

`    `path('auth/', include('djoser.urls.authtoken')),

]






**DJOSER Endpoints:**

**You can try these endpoints: …/auth/users/me**

- **The users/ endpoint lists all users and you can make a post call to create a new one.**
- **You can also create tokens for a user from the auth/token/login endpoint.**

- **auth/users/me endpoint:  Make a get call with any user's token to this end point, and it will provide the details of the authenticated user. This endpoint also supports a put call to update the email address of this user.**

**DJOSER - JWT**





























**DRF JWT**

pipenv install djangorestframework-simplejwt~=5.2.1

**settings.py ->** 

INSTALLED\_APPS = [

`    `'rest\_framework.authtoken',

`    `'djoser',

`    `'rest\_framework\_simplejwt',

]

`        `'DEFAULT\_AUTHENTICATION\_CLASSES': (

`        `'rest\_framework.simplejwt.authentication.JWTAuthentication',

`            `'rest\_framework.authentication.TokenAuthentication',

`        `),

from datetime import timedelta

SIMPLE\_JWT = {

`    `'ACCESS\_TOKEN\_LIFETIME': timedelta(minutes=5),

}


**urls.py ->**

from rest\_framework\_simplejwt.views import TokenObtainPairView, TokenRefreshView

`    `path('api/token/', TokenObtainPairView.as\_view(), name='token\_obtain\_pair'),

`    `path('api/token/refresh/', TokenRefreshView.as\_view(), name='token\_refresh'),

**BLACKLIST**

**settings.py ->** 

INSTALLED\_APPS = [

`    `'djoser',

`    `'rest\_framework\_simplejwt',

`    `'rest\_framework\_simplejwt.token\_blacklist'

]

**urls.py ->**

from rest\_framework\_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView

`    `path('api/token/blacklist/', TokenBlacklistView.as\_view(), name='token\_blacklist'),






