# CherryBlossom
Toolkit for automating the buying and selling of designer clothes from Yahoo Japan Auctions, Mercari JP, and Rakuten 

## Usage
CherryBlossom provides several features to speed up and automate the tedious process of buying clothes from Japan at discounts. Use cases include:

-Propagating PostgreSQL databases with listings to easily find relavant products across multiple searches

-Cross referencing listing prices with sold Grailed listings

-Estimating product markups using computer vision

## API
CherryBlossom APIs are meant to be used with PostgreSQL databases. Create a '.env' file and include a DATABASE_URL environment variable 

```py
   DATABASE_URL = YOUR DATABASE URL
```

### Grailed
### /api/items

#### Post
##### Parameters:
```name (String)```: Name of item to be searched

#### Get
##### Parameters:
```name (String)```: Name of item to be searched

#### Response:
```{'Item Name':'Item','Price': $0}```


#### Patch
##### Parameters:
```name (String)```: Name of item to be updated


### /api/items/by-key

#### Get
##### Parameters:
```key (String)```: Keyword to be searched, returning all items with name containing ```key```

#### Response:
```
{
{'Item Name':'Item1','Price': $0},
{'Item Name':'Item2','Price': $0},
{'Item Name':'Item3','Price': $0}
}
```

### /api/items/by-price

#### Get
##### Parameters:
```minPrice (Integer)```: Minimum price of items in search

```maxPrice (Integer)```: Maximum price of items in search

#### Response:
```
{
{'Item Name':'Item1','Price': $0},
{'Item Name':'Item2','Price': $0},
{'Item Name':'Item3','Price': $0}
}
```

### FromJapan

### /api/items/search

#### Post
##### Parameters:
```searchTerm (String)```: Search term that item appears under

### /api/items

#### Post
##### Parameters:
```searchTerm (String)```: Search term that item appears under

```name (String)```: Name of item

```link (String)```: URL linking to item page

```price (Integer)```: Price of item

### /api/items/by-term

#### Get
##### Parameters:
```searchTerm (String)```: Term to be searched, returning all items that appear under given search term

#### Response:
```
{
{'searchTerm':'searchTerm', 'name':''item1', link:'example.com/item1, 'Price': $0},
{'searchTerm':'searchTerm', 'name':''item2', link:'example.com/item2, 'Price': $0},
{'searchTerm':'searchTerm', 'name':''item3', link:'example.com/item3, 'Price': $0}
}
```

### /api/items/by-like-term

#### Get
##### Parameters:
```searchTerm (String)```: Term to be searched, returning all items with name containing ```searchTerm```

#### Response:
```
{
{'searchTerm':'searchTerm', 'name':''item1', link:'example.com/item1, 'Price': $0},
{'searchTerm':'searchTerm', 'name':''item2', link:'example.com/item2, 'Price': $0},
{'searchTerm':'searchTerm', 'name':''item3', link:'example.com/item3, 'Price': $0}
}
```

### /api/items/by-like-searchterm

#### Get
##### Parameters:
```searchTerm (String)```: Term to be searched, returning all items with searchTerm containing ```searchTerm```

#### Response:
```
{
{'searchTerm':'searchTerm', 'name':''item1', link:'example.com/item1, 'Price': $0},
{'searchTerm':'searchTerm', 'name':''item2', link:'example.com/item2, 'Price': $0},
{'searchTerm':'searchTerm', 'name':''item3', link:'example.com/item3, 'Price': $0}
}
```

### /api/items/by-price

#### Get
##### Parameters:
```minPrice (Integer)```: Minimum price of items in search

```maxPrice (Integer)```: Maximum price of items in search

#### Response:
```
{
{'searchTerm':'searchTerm', 'name':''item1', link:'example.com/item1, 'Price': $0},
{'searchTerm':'searchTerm', 'name':''item2', link:'example.com/item2, 'Price': $0},
{'searchTerm':'searchTerm', 'name':''item3', link:'example.com/item3, 'Price': $0}
}
```
