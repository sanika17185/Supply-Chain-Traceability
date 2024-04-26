import tqdm
import random
from datetime import timedelta, datetime
import pandas as pd
from data_generation.supply_chain import SupplyChain
from data_generation.business_entities import BusinessEntitiesData
from data_generation.utils import cross_contaminate, add_epcis_formatting

def dataframe_to_csv(df, destination_path):
    df.to_csv(destination_path)

def generate_data(ftl_df, entities_df, n=10000):
    #Create a dictionary of the functions so that they can be called in the supply chain based on the type of entity
    functions_dict = {
        'farm': BusinessEntitiesData.farm_function,
        'wholesaler': BusinessEntitiesData.wholesaler_function,
        'grocery': BusinessEntitiesData.grocery_function,
        'groceryNoTransform': BusinessEntitiesData.grocery_no_transform_function,
        'distributor': BusinessEntitiesData.distributor_function,
        'packaging': BusinessEntitiesData.coolingpacking_function,
        'restaurant': BusinessEntitiesData.restaurant_function,
        'processor': BusinessEntitiesData.processing_plant_function,
        'landBasedReceiver': BusinessEntitiesData.initial_fish_function,
        'seafoodFarm': BusinessEntitiesData.initial_fish_function
    }

    all_ctes = []
    for i in range(n):
        #Randomly select a food item and generate the supply chain
        food_item = ftl_df.sample()
        sc = SupplyChain.generate_supply_chain(food_item)

        #Determine the entities for the supply chain
        indexes = []
        for entity_type in sc:
            try:
                entity = entities_df[entities_df.businessType == entity_type].sample(weights='sizeWeight',replace=True).index.values[0]
                indexes.append(entity)
            except:
                pass

        entities = entities_df.iloc[indexes].reset_index(drop=True)

        #Run the function for each entity in the supply chain
        #Note: the input for each function will be (fake, food_item, sc, entities, previous_cte, index)
        #A standardized input makes it easy to iterate through and call each function
        #In plain language, it is calling an instance of faker, the current food_item, the supply chain, the entities in the supply chain, the most recent CTE, and the index
        ctes = []
        for index in entities.index:
            try:
                previous_cte_name = list(ctes[-1].keys())[-1]
                previous_cte = ctes[-1][previous_cte_name]
            except:
                previous_cte = []

            ctes.append(functions_dict[entities.iloc[index].businessType](food_item, sc, entities,previous_cte,index))
        
            

        all_ctes.extend(ctes)

    # import pdb;pdb.set_trace()
    return all_ctes


def create_dfs(data, create_csv = False):
    cte_data = {
        'harvesting' : [],
        'cooling' : [],
        'initialPackaging' : [],
        'firstLandBasedReceiving' : [],
        'shipping' : [],
        'receiving' : [],
        'transformation' : []
    }


    for entity in data:
        for type in list(entity.keys()):
            cte_data[type].append(entity[type]) 

    for event in list(cte_data.keys()):
        cte_data[event] = pd.DataFrame(cte_data[event])
    
    #Cross contaminate
    cte_data = cross_contaminate(cte_data)

    #Add EPCIS formatting
    cte_data = add_epcis_formatting(cte_data)

    #Create a csv of data
    if create_csv == True:
        for event in list(cte_data.keys()):
            cte_data[event].to_csv(f'output/{event}.csv',index=False)

    return cte_data


if __name__ == "__main__":

    entityCount = int(input("Enter how many food items you would like to simulate: "))

    #Load the core data
    ftl_df = pd.read_excel('ftl_items.xlsx', sheet_name='Sheet1')
    business_entities = BusinessEntitiesData()
    business_entities_df = business_entities.generate_synthetic_data(100)

    data = generate_data(ftl_df, business_entities_df, n=entityCount)


    dfs = create_dfs(data,create_csv=True)

    dataframe_to_csv(business_entities_df, 'output/business_enitiies.csv')

    print("Data Successfully generated")
