# Full Stack Store API
This API was made to control the CRUD operations of a simple online store using Flask. The idea of the application is a multi-vendor e-commerce platform. Every seller with an Admin role can create products, tags, cats, and so on. And the regular user can review and buy the products.

## Installing Dependencies

### Python 3.9
You need python 3.9 version to run this application. You can follow the instructions on [Python Documentation](https://docs.python.org/3/using/index.html)

### Virtual Environment (pipenv)
You need to install pipenv on your machine in order to enable the virtual environment. Running your application on a diffrent environment considered a better practice. You can install pipenv following the instructions in [this](https://pypi.org/project/pipenv/) link.

### PIP Dependencies
Once you have set up pipenvm, you need to install the dependencies using the bellow command
```
pipenv install
```

And then you can run your environment using the bellow command
```
pipenv shell
```

### Local Database Setup
Once you create the database, navigate to the root folder using your terminal and run the following commands
```
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### Local Testing
To verify that everything is running as it supposed to without any errors, navigate to the app folder and run
```
python3 test_app.py
```

### Running the server
In order to run your server, you need to setup the environment variables in the terminal as below
```
export DATABASE_URL={YOUR_DB_URL}
export AUTH0_DOMAIN={YOUR_AUTH0_DOMAIN}
export ALGORITHMS={YOUR_AUTH0_ALGORITHMS}
export API_AUDIENCE={YOUR_API_AUDIENCE}
export PRODUCT_PER_PAGE={NUMBER_OF_PRODUCTS_TO_SHOW_PER_PAGE}
export SELLER_PER_PAGE={NUMBER_OF_SELLERS_TO_SHOW_PER_PAGE}
export FLASK_APP=app
export FLASK_DEBUG=true
export FLASK_ENV=development
```
and then you can run the app using the below command
```
flask run
```



## Endpoints
Below are the endpoints which are available to use.

#### Products

GET '/products' - Get all products

- Fetches a list of products and another helpful information
- Request Arguments: None
- Returns: An object as per below:
{
  'success': boolean,
  'products': array_of_objects,
  'total_products': integer,
  'cats': array_of_categories,
  'tags': array_of_tags,
}
- 404 will be returned if not found

GET '/products/<id>' - Get one product

- Fetches a single product
- Request Arguments: id: integer. 
- Returns: An object as per below:
{
  'id': boolean,
  'name': string,
  'description': string,
  'creation_date': string,
  'update_date': string,
  'price': float,
  'num_of_sales': integer,
  'total_sales': integer,
  'rating': integer,
  'image_url': string,
  'seller': seller_data_object,
  'cat': cat_data_object,
  'reviews': array,
  'tags': array,
}
- 404 will be returned if not found

POST '/products' - Add product

- Add on product to the database
- Request Arguments: none. JSON data: {
  'name': string, 'description': string, 'price': integer, 'image_url': string, 'seller_id': integer, 'cat_id': integer
}
- Returns: An object as per below:
{
  'success': boolean,
  'product_id': integer
}
- 422 will be returned if failed to 

PATCH '/products/<id>' - Update product

- Update product on the database
- Request Arguments: product. JSON data: {
  'name': string, 'description': string, 'price': integer, 'image_url': string, 'seller_id': integer, 'cat_id': integer
}
- Returns: An object as per below:
{
  'success': boolean,
  'product': integer
}
- 422 will be returned if failed to 

DELETE '/products/<id>' - Delete product

- Delete product on the database
- Request Arguments: id.
- Returns: An object as per below:
{
  'success': boolean,
  'product': integer
}
- 422 will be returned if failed to 

POST '/search' - Search for a product

- Fetches list of product as per the given argument.
- Request Arguments: None. JSON data: {search_term: string} 
- Returns: An object as per below:
{
  products_len: integer,
  products: array
}
- 422 will be returned if failed to 

PATCH '/sell_product/<id>' - Used when buyer by product

- Increment the value of the product number of sales and the total amount of sales. 
- Request Arguments: id: integer. 
- Returns: An object as per below:
{
  formated product
}
- 422 will be returned if failed to 

#### Sellers

GET '/sellers' - Get all sellers

- Fetches and array of sellers and another helpful information
- Request Arguments: None
- Returns: An object as per below:
{
  'success': boolean,
  'sellers': array,
  'total_sellers': integer,
}
- 404 will be returned if not found

GET '/sellers/<id>' - Get one seller

- Fetches a single seller
- Request Arguments: id: integer. 
- Returns: An object as per below:
{
  'id': integer,
  'name': string,
  'phone_number': string,
  'store_description': string,
  'avatar': string,
  'website': string,
  'facebook_link': string,
  'registration_date': string,
  'related_products': array,
  'total_sold_products': integer,
  'total_sold_amount': float
}
- 404 will be returned if not found

POST '/sellers' - Add seller

- Add seller to the database
- Request Arguments: none. JSON data: {'avatar': string, 'facebook_link': string, 'name': string, 'phone_number': string, 'store_description': string, 'website': string}
- Returns: An object as per below:
{
  'success': boolean,
  'seller_id': integer,
}
- 422 will be returned if failed to 

PATCH '/sellers/<id>' - Update seller

- Update seller on the database
- Request Arguments: id. 
- Returns: An object as per below:
{
  'success': boolean,
  'seller': object,
}
- 422 will be returned if failed to 

DELETE '/sellers/<id>' - Delete seller

- Delete seller on the database
- Request Arguments: id. 
- Returns: An object as per below:
{
  'success': boolean,
  'seller': integer,
}
- 422 will be returned if failed to 

POST '/seller_search' - Search for a seller

- Search for a seller
- Request Arguments: None. JSON data: {search_term: string} 
- Returns: An object as per below:
{
  'sellers_len': integer,
  'sellers': array
}
- 422 will be returned if failed to 

GET '/sellers/<id>/products' - Get products under specific seller

- Fetches a list of products under specific seller
- Request Arguments: id: integer
- Returns: An object as per below:
{
  'total_products': integer,
  'success': boolean,
  'products': array,
  'cats': array,
  'tags': array,
}
- 404 will be returned if not found

#### Categories

GET '/categories' - Get all categories

- Fetches and array of categories and another helpful information
- Request Arguments: None
- Returns: An object as per below:
{
  'success': boolean,
  'categories': array,
  'total_categories': integer,
}
- 404 will be returned if not found

GET '/categories/<id>' - Get one category

- Fetches a single category
- Request Arguments: id: integer. 
- Returns: An object as per below:
{
  'id': integer,
  'name': string,
  'related_products': array
}
- 404 will be returned if not found

POST '/categories' - Add category

- Add category to the database
- Request Arguments: none. JSON data: {'name': string}
- Returns: An object as per below:
{
  'success': boolean,
  'category_id': integer,
}
- 422 will be returned if failed to 

PATCH '/categories/<id>' - Update category

- Update category on the database
- Request Arguments: id. 
- Returns: An object as per below:
{
  'success': boolean,
  'category': object,
}
- 422 will be returned if failed to 

DELETE '/categories/<id>' - Delete category

- Delete category on the database
- Request Arguments: id. 
- Returns: An object as per below:
{
  'success': boolean,
  'category': integer,
}
- 422 will be returned if failed to 

POST '/category_search' - Search for a category

- Search for a category
- Request Arguments: None. JSON data: {search_term: string} 
- Returns: An object as per below:
{
  'categories_len': integer,
  'categories': array
}
- 422 will be returned if failed to 

GET '/categories/<id>/products' - Get products under specific category

- Fetches a list of products under specific category
- Request Arguments: id: integer
- Returns: An object as per below:
{
  'total_products': integer,
  'success': boolean,
  'products': array,
  'cats': array,
  'tags': array,
}
- 404 will be returned if not found

#### Tags

GET '/tags' - Get all tags

- Fetches and array of tags and another helpful information
- Request Arguments: None
- Returns: An object as per below:
{
  'success': boolean,
  'tags': array,
  'total_tags': integer,
}
- 404 will be returned if not found

GET '/tags/<id>' - Get one tag

- Fetches a single tag
- Request Arguments: id: integer. 
- Returns: An object as per below:
{
  'id': integer,
  'name': string,
  'related_products': array
}
- 404 will be returned if not found

POST '/tags' - Add tag

- Add tag to the database
- Request Arguments: none. JSON data: {'name': string}
- Returns: An object as per below:
{
  'success': boolean,
  'tag_id': integer,
}
- 422 will be returned if failed to 

PATCH '/tags/<id>' - Update tag

- Update tag on the database
- Request Arguments: id. 
- Returns: An object as per below:
{
  'success': boolean,
  'tag': object,
}
- 422 will be returned if failed to 

DELETE '/tags/<id>' - Delete tag

- Delete tag on the database
- Request Arguments: id. 
- Returns: An object as per below:
{
  'success': boolean,
  'tag': integer,
}
- 422 will be returned if failed to 

POST '/tag_search' - Search for a tag

- Search for a tag
- Request Arguments: None. JSON data: {search_term: string} 
- Returns: An object as per below:
{
  'tags_len': integer,
  'tags': array
}
- 422 will be returned if failed to 

GET '/tags/<id>/products' - Get products under specific tag

- Fetches a list of products under specific tag
- Request Arguments: id: integer
- Returns: An object as per below:
{
  'total_products': integer,
  'success': boolean,
  'products': array,
  'cats': array,
  'tags': array,
}
- 404 will be returned if not found


#### Reviews

GET '/reviews' - Get all reviews

- Fetches and array of reviews and another helpful information
- Request Arguments: None
- Returns: An object as per below:
{
  'success': boolean,
  'reviews': array,
  'total_reviews': integer,
}
- 404 will be returned if not found

GET '/reviews/<id>' - Get one review

- Fetches a single review
- Request Arguments: id: integer. 
- Returns: An object as per below:
{
  'id': integer,
  'reviewer': string,
  'review': string,
  'review_date': string,
  'product_id': integer,
}
- 404 will be returned if not found

POST '/reviews' - Add review

- Add review to the database
- Request Arguments: none. JSON data: {'reviewer': string, 'review': string, 'product_id': integer}
- Returns: An object as per below:
{
  'success': boolean,
  'review_id': integer,
}
- 422 will be returned if failed to 

PATCH '/reviews/<id>' - Update review

- Update review on the database
- Request Arguments: id. 
- Returns: An object as per below:
{
  'success': boolean,
  'review': object,
}
- 422 will be returned if failed to 

DELETE '/reviews/<id>' - Delete review

- Delete review on the database
- Request Arguments: id. 
- Returns: An object as per below:
{
  'success': boolean,
  'review': integer,
}
- 422 will be returned if failed to 

#### Error Handeling

- 404 Error: Resource was not found
- 401 Error: Unauthorized Access
- 422 Error: Unprocessable Entity
- Auth Error: {
  400: [
    Unable to parse authentication token,
    Unable to find the appropriate key
  ],
  401: [
    Authorization header is expected,
    Authorization header is misconfigured,
    Token not found,
    Authorization header must be bearer token,
    No token was found,
    Authorization malformed,
    Token expired,
    Incorrect claims. Please, check the audience and issuer,
    check your RBAC settings in Auth0,
  ],
  403: [
    You don\'t have access to the requested resource
  ]

}














