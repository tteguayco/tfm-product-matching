
select top(300000) ProductID		as PriceID
, CrawlerDateTime		as CrawlerDateTime
, WebShopID				as WebShopID
, PSMID					as SearchEngineID
, ProdanetID			as ProdanetID
, WebShopProductID		as WebShopProductID
, IsPriceSearchEngine	as IsSearchEngine
, DeliveryTimeID		as DeliveryTimeID
, ShippingCosts			as ShippingCosts
, Price					as Price
, ProductLink			as ProductLink
from [Crawler_Final_Data].dbo.Crawler_Product_Data_Final with (nolock)
where AdditionDate > '2019-01-31 00:00:00'

select
  DeliveryTimeID	as DeliveryTimeID
, DeliveryTime		as DeliveryTime
from [Crawler_Final_Data].[dbo].[DeliveryTimeMapping]

select 
  ProdanetID				as ProdanetID
, CountryID					as TerritoryID
, BrandID					as BrandID
, ProductName				as ProcductName
, ProductName2				as ProductName2
, ManufacturerCode			as ManufacturerCode
, ProdanetProductGroupID	as ProductCategoryID
from [PMV2_Reference].dbo.ProductsBasic with (nolock)
where IsDeleted=0


select
  [BrandID]				as BrandID
, [ResKeyBrandName]		as BrandName
from [MasterData].dbo.Brand
where Active=1


select 
  TerritoryID			as TerritoryID
, ReskeyTerritoryName	as TerritoryName
 from MasterData.dbo.TerritoryISO31661 


select 
  CountryID as TerritoryID
, ShopID	as WebShopID
, ShopName	as WebShopName
from Crawler_Basic_V2.dbo.webshops 
where IsEnableD=1


select  a.WgrID						as ProductCategoryID
, a.WgrCode							as ProductCategoryCode
, case	when a.WgrCode like '%000000'	then  null 
		when a.WgrCode like '%0000'		then  left(a.WgrCode,2)+'000000'
		when a.WgrCode like '%00'		then  left(a.WgrCode,4)+'0000'
		else left(a.WgrCode,6)+'00' 
		end							as ParentProductCategoryCode
, TextOfWgr							as ProductCategoryName
from 
Artman_Sync.[dbo].[WGrData] a
inner join Artman_Sync.[dbo].[WGrTable] b on a.WgrCode =b.WgrCode
where b.CountryIDf & 16= 16