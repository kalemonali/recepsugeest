import pandas as pd
import numpy as np
import pickle
from numpy import random


def test(FT, DT, VNE, RE, MO, SU, Item, Qty):
    df = pd.read_csv("processed_data.csv", encoding='unicode_escape')

    dfsurprise = pd.read_csv("processed_data.csv", encoding='unicode_escape')

    ##############json start
    df1 = pd.DataFrame(zip(Item, Qty), columns=['Item', 'Qty'])
    ##############json end
    df1[['Item']] = df1[['Item']].apply(lambda x: x.astype(str).str.lower())
    df1['Qty'] = df1['Qty'].tolist()
    check = df1[df1['Qty'] > 0]

    user_list = []
    user_stock_list = check['Item'].tolist()
    rece_ingre = df['ingredients'].tolist()

    for j in range(len(rece_ingre)):
        list1 = []
        for i in range(len(user_stock_list)):
            try:
                if user_stock_list[i] in rece_ingre[j]:
                    list1.append(user_stock_list[i])
            except:
                list1 = []
        user_list.append(list1)

    df['user_ingre_list'] = user_list

    # To count no of ingredients user has
    user_ingredient_count = []

    for i in range(len(user_list)):
        count = len(user_list[i])
        user_ingredient_count.append(count)

    df['user_no_of_ingredients'] = user_ingredient_count

    # Calculate the pecerntage for stock & round_off the percentage by using round() function..
    df['Available Stock(%)'] = round(((df['user_no_of_ingredients'] / df['ingredientcount']) * 100)).fillna(0)

    # Drop the percentage which is less than 50
    df.drop(df[df['Available Stock(%)'] < 50.0].index, inplace=True)

    #####CONDITIONS STARTS HERE
    #################################################################################
    if (FT != '' and DT != '' and VNE != '' and MO != '' and RE != '' and SU == 'no'):
        # print("conditions 1 here")
        def food_type(choice):
            return df[df['Food Type'] == choice]

        df_food_type = food_type(FT)

        def dish_type(choice):
            return df_food_type[df_food_type['Dish Type'] == choice]

        df_dish_type = dish_type(DT)

        def region(choice):
            return df_dish_type[df_dish_type['region'] == choice]

        df_region = region(RE)

        def moo(choice):
            return df_region[df_region['Mood'] == choice]

        df_moo = moo(MO)

        def veg_non_veg(choice):
            return df_moo[df_moo['veg_non_veg_egg'] == choice]

        df_veg_non_veg = veg_non_veg(VNE)

    elif (FT != '' and DT != '' and VNE != '' and MO != '' and RE == '' and SU == 'no'):
        # print("conditions 1 here")
        def food_type(choice):
            return df[df['Food Type'] == choice]

        df_food_type = food_type(FT)

        def dish_type(choice):
            return df_food_type[df_food_type['Dish Type'] == choice]

        df_dish_type = dish_type(DT)

        def moo(choice):
            return df_dish_type[df_dish_type['Mood'] == choice]

        df_moo = moo(MO)

        def veg_non_veg(choice):
            return df_moo[df_moo['veg_non_veg_egg'] == choice]

        df_veg_non_veg = veg_non_veg(VNE)

        ####################surprise condition
    elif (FT != '' and DT != '' and VNE != '' and MO != '' and RE != '' and SU == 'yes'):
        # print("conditions 1 here")
        def food_type(choice):
            return dfsurprise[dfsurprise['Food Type'] == choice]

        df_food_type = food_type(FT)

        def dish_type(choice):
            return df_food_type[df_food_type['Dish Type'] == choice]

        df_dish_type = dish_type(DT)

        def region(choice):
            return df_dish_type[df_dish_type['region'] == choice]

        df_region = region(RE)

        def moo(choice):
            return df_region[df_region['Mood'] == choice]

        df_moo = moo(MO)

        def veg_non_veg(choice):
            return df_moo[df_moo['veg_non_veg_egg'] == choice]

        df_veg_non_veg = veg_non_veg(VNE)

    elif (FT != '' and DT != '' and VNE != '' and MO != '' and RE == '' and SU == 'yes'):
        # print("conditions 1 here")
        def food_type(choice):
            return dfsurprise[dfsurprise['Food Type'] == choice]

        df_food_type = food_type(FT)

        def dish_type(choice):
            return df_food_type[df_food_type['Dish Type'] == choice]

        df_dish_type = dish_type(DT)

        def moo(choice):
            return df_dish_type[df_dish_type['Mood'] == choice]

        df_moo = moo(MO)

        def veg_non_veg(choice):
            return df_moo[df_moo['veg_non_veg_egg'] == choice]

        df_veg_non_veg = veg_non_veg(VNE)

    ####################################################################################

    if (FT != '' and DT != '' and VNE != '' and MO != '' and RE != '' and SU == 'no'):
        # This is our final dataset for recipe recommendation.In this we contains all the required columns
        df_func = df_veg_non_veg.drop(
            columns=['Unnamed: 0', 'Description', 'ingredients_data', 'ingredients', 'ingredientcount', 'Occasion',
                     'user_ingre_list', 'user_no_of_ingredients'], axis=1)

        # suggesting the random recipies
        a = len(df_func)
        if a == 0:
            print(
                "****YOUR ENTERED OPTIONS DOSEN'T MATCHED WITH OUR RECIPES SO WE HAVE SOME SURPRISE RECIPE FOR YOU****")
            print('\n')
            print(
                "******************************************SURPRISE RECIPE********************************************")

            # This is our final dataset for recipe recommendation.In this we contains all the required columns
            df_sss = dfsurprise.drop(
                columns=['Unnamed: 0', 'Description', 'ingredients_data', 'ingredients', 'ingredientcount', 'Occasion'],
                axis=1)

            # suggesting the random recipies
            b = len(df_sss)
            i = random.randint(b)
            j = i + 2
            # Sorting best recipes by views,likes....
            df_views = df_sss.sort_values(by=['Views']).iloc[i:j]  # sort by views
            df_likes = df_sss.sort_values(by=['Likes']).iloc[i:j]  # sort by likes
            df_Easyness = df_sss.sort_values(by=['Easiness']).iloc[i:j]  # sort by easyness score of recipe
            # df_uploaded_time = df_ss.sort_values(by=['uploaded_time']).iloc[i:j]      # sort by uploded date of video or new videos

            # Concatenating all outputs in one dataframe
            df_final_random = pd.concat([df_views, df_likes, df_Easyness], axis=0)

            # final dataframe
            # print(df_final_random)
            return (df_final_random)


        else:
            i = random.randint(a)
            j = i + 2
            # Sorting best recipes by views,likes....
            df_views = df_func.sort_values(by=['Views']).iloc[i:j]  # sort by views
            df_likes = df_func.sort_values(by=['Likes']).iloc[i:j]  # sort by likes
            df_Easyness = df_func.sort_values(by=['Easiness']).iloc[i:j]  # sort by easyness score of recipe

            # Concatenating all outputs in one dataframe
            df_final_random = pd.concat([df_views, df_likes, df_Easyness], axis=0)

            # final dataframe
            # print(df_final_random)
            return (df_final_random)
    #####################################################################

    elif (FT != '' and DT != '' and VNE != '' and MO != '' and RE == '' and SU == 'no'):
        # This is our final dataset for recipe recommendation.In this we contains all the required columns
        df_func = df_veg_non_veg.drop(
            columns=['Unnamed: 0', 'Description', 'ingredients_data', 'ingredients', 'ingredientcount', 'Occasion',
                     'user_ingre_list', 'user_no_of_ingredients'], axis=1)

        # suggesting the random recipies
        a = len(df_func)
        if a == 0:
            print(
                "****YOUR ENTERED OPTIONS DOSEN'T MATCHED WITH OUR RECIPES SO WE HAVE SOME SURPRISE RECIPE FOR YOU****")
            print('\n')
            print(
                "******************************************SURPRISE RECIPE********************************************")

            # This is our final dataset for recipe recommendation.In this we contains all the required columns
            df_sss = dfsurprise.drop(
                columns=['Unnamed: 0', 'Description', 'ingredients_data', 'ingredients', 'ingredientcount', 'Occasion'],
                axis=1)

            # suggesting the random recipies
            b = len(df_sss)
            i = random.randint(b)
            j = i + 2
            # Sorting best recipes by views,likes....
            df_views = df_sss.sort_values(by=['Views']).iloc[i:j]  # sort by views
            df_likes = df_sss.sort_values(by=['Likes']).iloc[i:j]  # sort by likes
            df_Easyness = df_sss.sort_values(by=['Easiness']).iloc[i:j]  # sort by easyness score of recipe
            # df_uploaded_time = df_ss.sort_values(by=['uploaded_time']).iloc[i:j]      # sort by uploded date of video or new videos

            # Concatenating all outputs in one dataframe
            df_final_random = pd.concat([df_views, df_likes, df_Easyness], axis=0)

            # final dataframe
            # print(df_final_random)
            return (df_final_random)


        else:
            i = random.randint(a)
            j = i + 2
            # Sorting best recipes by views,likes....
            df_views = df_func.sort_values(by=['Views']).iloc[i:j]  # sort by views
            df_likes = df_func.sort_values(by=['Likes']).iloc[i:j]  # sort by likes
            df_Easyness = df_func.sort_values(by=['Easiness']).iloc[i:j]  # sort by easyness score of recipe

            # Concatenating all outputs in one dataframe
            df_final_random = pd.concat([df_views, df_likes, df_Easyness], axis=0)

            # final dataframe
            # print(df_final_random)
            return (df_final_random)

        #################################new surprise me conditions

    elif (FT != '' and DT != '' and VNE != '' and MO != '' and RE != '' and SU == 'yes'):
        # This is our final dataset for recipe recommendation.In this we contains all the required columns
        df_func = df_veg_non_veg.drop(
            columns=['Unnamed: 0', 'Description', 'ingredients_data', 'ingredients', 'ingredientcount', 'Occasion'],
            axis=1)

        # suggesting the random recipies
        a = len(df_func)
        if a == 0:
            print(
                "****YOUR ENTERED OPTIONS DOSEN'T MATCHED WITH OUR RECIPES SO WE HAVE SOME SURPRISE RECIPE FOR YOU****")
            print('\n')
            print(
                "******************************************SURPRISE RECIPE********************************************")

            # This is our final dataset for recipe recommendation.In this we contains all the required columns
            df_sss = dfsurprise.drop(
                columns=['Unnamed: 0', 'Description', 'ingredients_data', 'ingredients', 'ingredientcount', 'Occasion'],
                axis=1)

            # suggesting the random recipies
            b = len(df_sss)
            i = random.randint(b)
            j = i + 2
            # Sorting best recipes by views,likes....
            df_views = df_sss.sort_values(by=['Views']).iloc[i:j]  # sort by views
            df_likes = df_sss.sort_values(by=['Likes']).iloc[i:j]  # sort by likes
            df_Easyness = df_sss.sort_values(by=['Easiness']).iloc[i:j]  # sort by easyness score of recipe
            # df_uploaded_time = df_ss.sort_values(by=['uploaded_time']).iloc[i:j]      # sort by uploded date of video or new videos

            # Concatenating all outputs in one dataframe
            df_final_random = pd.concat([df_views, df_likes, df_Easyness], axis=0)

            # final dataframe
            # print(df_final_random)
            return (df_final_random)


        else:
            i = random.randint(a)
            j = i + 2
            # Sorting best recipes by views,likes....
            df_views = df_func.sort_values(by=['Views']).iloc[i:j]  # sort by views
            df_likes = df_func.sort_values(by=['Likes']).iloc[i:j]  # sort by likes
            df_Easyness = df_func.sort_values(by=['Easiness']).iloc[i:j]  # sort by easyness score of recipe

            # Concatenating all outputs in one dataframe
            df_final_random = pd.concat([df_views, df_likes, df_Easyness], axis=0)

            # final dataframe
            # print(df_final_random)
            return (df_final_random)
    #####################################################################

    elif (FT != '' and DT != '' and VNE != '' and MO != '' and RE == '' and SU == 'yes'):
        # This is our final dataset for recipe recommendation.In this we contains all the required columns
        df_func = df_veg_non_veg.drop(
            columns=['Unnamed: 0', 'Description', 'ingredients_data', 'ingredients', 'ingredientcount', 'Occasion'],
            axis=1)

        # suggesting the random recipies
        a = len(df_func)
        if a == 0:
            print(
                "****YOUR ENTERED OPTIONS DOSEN'T MATCHED WITH OUR RECIPES SO WE HAVE SOME SURPRISE RECIPE FOR YOU****")
            print('\n')
            print(
                "******************************************SURPRISE RECIPE********************************************")

            # This is our final dataset for recipe recommendation.In this we contains all the required columns
            df_sss = dfsurprise.drop(
                columns=['Unnamed: 0', 'Description', 'ingredients_data', 'ingredients', 'ingredientcount', 'Occasion'],
                axis=1)

            # suggesting the random recipies
            b = len(df_sss)
            i = random.randint(b)
            j = i + 2
            # Sorting best recipes by views,likes....
            df_views = df_sss.sort_values(by=['Views']).iloc[i:j]  # sort by views
            df_likes = df_sss.sort_values(by=['Likes']).iloc[i:j]  # sort by likes
            df_Easyness = df_sss.sort_values(by=['Easiness']).iloc[i:j]  # sort by easyness score of recipe
            # df_uploaded_time = df_ss.sort_values(by=['uploaded_time']).iloc[i:j]      # sort by uploded date of video or new videos

            # Concatenating all outputs in one dataframe
            df_final_random = pd.concat([df_views, df_likes, df_Easyness], axis=0)

            # final dataframe
            # print(df_final_random)
            return (df_final_random)


        else:
            i = random.randint(a)
            j = i + 2
            # Sorting best recipes by views,likes....
            df_views = df_func.sort_values(by=['Views']).iloc[i:j]  # sort by views
            df_likes = df_func.sort_values(by=['Likes']).iloc[i:j]  # sort by likes
            df_Easyness = df_func.sort_values(by=['Easiness']).iloc[i:j]  # sort by easyness score of recipe

            # Concatenating all outputs in one dataframe
            df_final_random = pd.concat([df_views, df_likes, df_Easyness], axis=0)

            # final dataframe
            # print(df_final_random)
            return (df_final_random)





