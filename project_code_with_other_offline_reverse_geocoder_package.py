import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from datetime import date, timedelta, date
import datetime

import reverse_geocoder as rg ##################contains package with all location with lat long ############ install package with reverse_geocoder by Ajay Thampi


# determining the sowing season##############for month between 6&10= kharif ##### 3&5= zaid  ############
def monthcheck(num):
    if num >= 6 and num <= 10:
        return ('kharif')
    elif num >= 3 and num <= 5:
        return ('zaid')
    elif (num >= 11 and num <= 12) or (num >= 1 and num <= 5):
        return ('rabi')
    else:
        return ('')


# file import
file1 = 'C:/Users/1539485/database/input.xls'  #################input excel sheet locations file1 input #############
file2 = 'C:/Users/1539485/database/Final_database.xls'  ##################reference excel sheet location file 2 = reference data###########
file3 = 'C:/Users/1539485/database/dynamicdb.xls'  ###################input weather and soil set location###########

in_put = pd.ExcelFile(file1)  ##########importing input excel sheet into pandas data frame ##########
reference_database = pd.ExcelFile(file2)  ##########importing reference excel sheet into pandas data frame ##########
dynamic = pd.ExcelFile(file3)  ##########importing input weather and soil excel sheet into pandas data frame ##########

# sheetsimport
input_1 = in_put.parse('input_database')  ##################input data set
soil_ddb = dynamic.parse('Soil_database')  ##################input soil dataset
weather_ddb = dynamic.parse('weather_database')  ##############input soil weather data set
crop_requirements = reference_database.parse('Crop_requirements')  ##############crop requirements per day
pop = reference_database.parse('Package_of_practices')  ##############package of practice per day
agro_climatic_info = reference_database.parse('AgroClimatic_wise_info')  ##############reference dataset
crop_comparison = reference_database.parse('crop_comparison_db')  ##############Crop recommended factors to manage crop nutrients w.r.t soil nutrient status
fertilizer = reference_database.parse('fertilizers')  ##############list of fertilizers
crop_disease = reference_database.parse('Crop_disease_refer')  ###############crop disease  dataset

# creating informationdata of farmer with its crop and total crop requirements
prefinaldb = {}  ################ creating dictionary of intermidiate dataset

for i in range(len(input_1.Farmer_name)):
    name = input_1.Farmer_name[i].lower().replace(' ', '')  ################  farmer Name
    lat = input_1.latitude[i]  ################ latitude of farmer location
    long = input_1.longitude[i]  ################ longitude
    ll = (lat, long)  ################ lat long set
    cv = input_1.crop_variety[i]  ################ crop variety
    ################calling Noinatim as geolocator

    ################performing the reverse geocoding to get location
    location = rg.search(ll) ################ assigning the location to loc which contains raw
    district = location[0]['admin'].lower().replace(' ', '')  ################ district name
    village = location[0]['name'].lower().raplace(' ','')     ################village/town location
    c1 = input_1.crop[i]  ################# crop name
    d1 = str(input_1.sowing_date[i])  ################# sowing date
    mm = int(d1[4:6])  ################ converting date month string object to int
    sc = monthcheck(mm)  ################# checking th season kharif, rabi, zaid
    d = datetime.datetime(year=int(d1[0:4]), month=int(d1[4:6]), day=int(d1[6:8]), hour=0, minute=0, second=0)  ################# converting date string object to datetime object
    prefinaldb[name] = []  ################# creating list of farmer name to collect crop total requirement
    prefinaldb[name].append(c1)  ################
    for j in range(len(agro_climatic_info.Divisions)):           #####################searching the location and crop  data the reference data
        if (agro_climatic_info.District[j].lower().replace(' ', '') != district or
                agro_climatic_info.Divisions[j].lower() != village or
                agro_climatic_info.Season[j].lower() != sc.lower() or
                agro_climatic_info.Crop[j].lower() != c1.lower() or
                agro_climatic_info.Crop_variety[j].lower().replace(' ','') != cv.lower().replace(' ','')):
            continue
        v1 = agro_climatic_info.Crop_variety[j].lower()
        idivision = agro_climatic_info.Divisions[j].lower()
        prefinaldb[name].append(v1)                                                ########################## inserting Crop variety in the farmer data##################
        prefinaldb[name].append(d)                                                 ######################## inserting  division#######################
        prefinaldb[name].append(sc.lower())                                        ######################## inserting season#######################
        prefinaldb[name].append(agro_climatic_info.Sub_agroclimaticzone[j].lower())          ######################## inserting sub agro climatic zone#######################
        prefinaldb[name].append(agro_climatic_info.District[j].lower())                      ######################## inserting the district#######################
        prefinaldb[name].append(agro_climatic_info.State[j].lower())                         ######################## inserting the state #######################
        prefinaldb[name].append(agro_climatic_info.Crop_water_requirement[j])  ######################### Crop water requirement in cm#######################
        prefinaldb[name].append(agro_climatic_info.Crop_yield[j])  ##################### Crop potential yield tonne/hecatre
        prefinaldb[name].append(agro_climatic_info.Crop_root_zone_depth[j])  #################### Crop root zone depth
        prefinaldb[name].append(agro_climatic_info.GDD[j])  ######################### Crop growing degree days
        prefinaldb[name].append(agro_climatic_info.Row_spacing[j])  ######################## in Crop row spacing
        prefinaldb[name].append(agro_climatic_info.Crop_spacing[j])  ######################## in crop spacing
        prefinaldb[name].append(agro_climatic_info.Seed_rate[j])  ######################## in  seed rate

        ##############Comparing reference (Static) soil dataframe with Dynamic (soil dataframe)#################################
        for k in range(len(soil_ddb.Divisions)):                 ######################searching the soil data for a farmer in input soil data###################
            if (idivision != soil_ddb.Divisions[k].lower() or name != soil_ddb.Farmer_name[i].lower().replace(' ','')):              ############conditions for checking farmer dat######
                continue
            # checking the nitrogen level if input soil data with referred recommended N level
            if agro_climatic_info.Soil_N_content[j] <= soil_ddb.Soil_N_content[k]:
                for l in range(len(fertilizer.name_of_ferti)):                                          ####################searching the Nitrogen fertilizer content in the reference fertlizer data##########
                    if fertilizer.N_content[l] == 0:                                                    ####################nitrogen fertilizer ######
                        continue
                    for m in range(len(crop_comparison.Crop_variety)):                                  #############################getting the crop increase/decrease/same recommended factor for eg for decrease 1.25* crop recommended #######
                        if (c1 == crop_comparison.Crop[m].lower() and v1 == crop_comparison.Crop_variety[m].lower()):
                            prefinaldb[name].append(agro_climatic_info.Recomended_N[j]*crop_comparison.Crop_recommended_low_soil[m]/fertilizer.N_content[l])  ###### nitrogen fertilizer recommended
                        else:
                            continue
            # for increase in current soil Nitrogen level that referred nitrogen level #####same logic as above decrease code
            elif agro_climatic_info.Soil_N_content[j] >= soil_ddb.Soil_N_content[k]:
                for l in range(len(fertilizer.name_of_ferti)):
                    if fertilizer.N_content[l] == 0:
                        continue
                    for m in range(len(crop_comparison.Crop_variety)):
                        if (c1 == crop_comparison.Crop[m].lower() and v1 == crop_comparison.Crop_variety[m].lower()):
                            prefinaldb[name].append(agro_climatic_info.Recomended_N[j]*crop_comparison.Crop_recommended_high_soil[m]/fertilizer.N_content[l])  ############################# nitrogen fertilizer recommended
                        else:
                            continue
                        # for same level or no change nitrogen level #######same logic as above code (94 line) nitrogen decrease logic
            else:
                for l in range(len(fertilizer.name_of_ferti)):
                    if fertilizer.N_content[l] == 0:
                        continue
                    for m in range(len(crop_comparison.Crop_variety)):
                        if (c1 == crop_comparison.Crop[m].lower() and v1 == crop_comparison.Crop_variety[m].lower()):
                            prefinaldb[name].append(agro_climatic_info.Recomended_N[j]*crop_comparison.Crop_recommended_medium_soil[m]/fertilizer.N_content[l])  ############################# nitrogen fertilizer recommended
                        else:
                            continue
             ############################################# Similair logic used for Phosphrous content ###########################################################
            if agro_climatic_info.Soil_P_content[j] <= soil_ddb.Soil_P_content[k]:
                for l in range(len(fertilizer.name_of_ferti)):
                    if fertilizer.P_content[l] == 0:
                        continue
                    for m in range(len(crop_comparison.Crop_variety)):
                        if (c1 == crop_comparison.Crop[m].lower() and v1 == crop_comparison.Crop_variety[m].lower()):
                            prefinaldb[name].append(
                                agro_climatic_info.Recomended_P2O5[j] * crop_comparison.Crop_recommended_low_soil[m]/fertilizer.P_content[l])  #############################P2O5 fertilizer recommended
                        else:
                            continue
            # for increase in current soil Nitrogen level that referred phosphorous level
            elif agro_climatic_info.Soil_P_content[j] >= soil_ddb.Soil_P_content[k]:
                for l in range(len(fertilizer.name_of_ferti)):
                    if fertilizer.P_content[l] == 0:
                        continue
                    for m in range(len(crop_comparison.Crop_variety)):
                        if (c1 == crop_comparison.Crop[m].lower() and v1 == crop_comparison.Crop_variety[m].lower()):
                            prefinaldb[name].append(agro_climatic_info.Recomended_P2O5[j]*crop_comparison.Crop_recommended_high_soil[m]/fertilizer.P_content[l])  #############################P2O5 fertilizer recommended
                        else:
                            continue
                        # for same level or no change
            else:
                for l in range(len(fertilizer.name_of_ferti)):
                    if fertilizer.P_content[l] == 0:
                        continue
                    for m in range(len(crop_comparison.Crop_variety)):
                        if (c1 == crop_comparison.Crop[m].lower() and v1 == crop_comparison.Crop_variety[m].lower()):
                            prefinaldb[name].append(agro_climatic_info.Recomended_P2O5[j]*crop_comparison.Crop_recommended_medium_soil[m]/fertilizer.P_content[l])  #############################P2O5 fertilizer recommended
                        else:
                            continue
            ##############################################Similair logic used for Potassium as Nitrogen###############################
            if agro_climatic_info.Soil_K_content[j] <= soil_ddb.Soil_K_content[k]:
                for l in range(len(fertilizer.name_of_ferti)):
                    if fertilizer.K_content[l] == 0:
                        continue
                    for m in range(len(crop_comparison.Crop_variety)):
                        if (c1 == crop_comparison.Crop[m].lower() and v1 == crop_comparison.Crop_variety[m].lower()):
                            prefinaldb[name].append(
                                agro_climatic_info.Recomended_K2O[j]*crop_comparison.Crop_recommended_low_soil[m]/fertilizer.K_content[l])  #############################P2O5 fertilizer recommended
                        else:
                            continue
            # for increase in current soil potassium level that referred potassium level
            elif agro_climatic_info.Soil_K_content[j] >= soil_ddb.Soil_K_content[k]:
                for l in range(len(fertilizer.name_of_ferti)):
                    if fertilizer.K_content[l] == 0:
                        continue
                    for m in range(len(crop_comparison.Crop_variety)):
                        if (c1 == crop_comparison.Crop[m].lower() and v1 == crop_comparison.Crop_variety[m].lower()):
                            prefinaldb[name].append(agro_climatic_info.Recomended_K2O[j]*crop_comparison.Crop_recommended_high_soil[m]/fertilizer.K_content[l])  #############################K2O fertilizer recommended
                        else:
                            continue
                        # for same level or no change
            else:
                for l in range(len(fertilizer.name_of_ferti)):
                    if fertilizer.K_content[l] == 0:
                        continue
                    for m in range(len(crop_comparison.Crop_variety)):
                        if (c1 == crop_comparison.Crop[m].lower() and v1 == crop_comparison.Crop_variety[m].lower()):
                            prefinaldb[name].append(
                                agro_climatic_info.Recomended_K2O[j] * crop_comparison.Crop_recommended_medium_soil[m] /
                                fertilizer.K_content[l])  #############################K2O fertilizer recommended
                        else:
                            continue

# converting dictionary into pandas database
prefinaldb = pd.DataFrame(prefinaldb)
prefinaldb = prefinaldb.T

prefinaldb.columns = ['Crop', 'Crop_variety', 'sowing_date', 'season', 'Sub_agro_climatic_zone', 'District', 'State',
                      'Crop_water_requirement', 'Crop_yield', 'Crop_root_zone_depth', 'GDD', 'Row_spacing',
                      'Crop_spacing',
                      'Seed_rate', 'Urea', 'Coated_Urea', 'Ammonium_chloride', 'Urea_super_granulated',
                      'Ammonium_sulfate', 'super_phosphoric_acid',
                      'Single_super_phosphate', 'Single_super_phosphate2', 'Tripple_superphosphate', 'Bone_meal_raw',
                      'Bone_meal_steam',
                      'rock_phosphate', 'potassium_chloride', 'potassium_sulfate', 'potassium_schoenite',
                      'potassium_chloride_gran',
                      'potassium_derived_molass']

y = int(datetime.date.isoformat(datetime.date.today())[0:4])                     ##################Current date ##################

OutputCR = {}
date = datetime.datetime(year=y, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)         #########################date#########
for i in range(0, 365):                                                                              ##################Creating the datetime dataset ##########
    OutputCR[date] = {}
    date = date + timedelta(days=1)

# OutputCR =OutputCR.T
Newdict = {}  #####################################Crop management timetable
DOS = []           ################################Sowing date list #########
for i in range(len(prefinaldb)):
    Newdict[str(prefinaldb.index.values[i])] = OutputCR                                                            ########################inserting the date time data dictionary within the list
    for j in range(len(crop_requirements)):
        if (prefinaldb.Crop[i].lower() != crop_requirements.Crop[j].lower() or
                prefinaldb.Crop_variety[i].lower() != crop_requirements.Crop_variety[j].lower() or
                prefinaldb.season[i].lower() != crop_requirements.Season[j].lower()):
            continue                                                                               ############################ searching the crop and agro climatic data within the reference crop requirement #
        DOS.append(prefinaldb.sowing_date[i])
        # Water requirements of crop
        for k in range(len(crop_requirements)):
            if (crop_requirements.Crop_requirements[k] != 'Water_requirements'):                      ######################water requirements for the crop from sowing to hravesting
                continue
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['Water requirement'] = crop_requirements['Day_of_sowing'][k]           ###############crop water requirements during the sowing
            nd = DOS[i] - timedelta(days=30)
            for l in range(0, 29):
                Newdict[str(prefinaldb.index.values[i])][nd]['Water requirement'] = crop_requirements['Day_pre_'+str(l)][k]          ######################field irrigation/crop water requirement per before sowing
                nd = nd + timedelta(days=1)
            ados = DOS[i]
            for m in range(1, prefinal.GDD[i]):
                Newdict[str(prefinaldb.index.values[i])][ados]['Water requirement'] = crop_requirements['Day_after_sowing'+str(m)][k]            ######################field irrigation/crop water requirement per after sowing
                ados = ados + timedelta(days=1)

        # Nitrogen Fertilizer requirements same logic as the Crop water requirement
        for k in range(len(crop_requirements)):
            if (crop_requirements.Crop_requirements[k] != 'N_requirements'):
                continue
            nd = DOS[i] - timedelta(days=30)
            for l in range(0, 29):
                nd = nd + timedelta(days=1)
                if (crop_requirements['Day_pre_' + str(l)][k] == ''):
                    continue
                Newdict[str(prefinaldb.index.values[i])][nd]['Urea'] = (crop_requirements['Day_pre_' + str(l)][k])*prefinaldb.Urea[i]      ##################################multiplying the nitrogen requirement fraction amount  for a day
                Newdict[str(prefinaldb.index.values[i])][nd]['Coated Urea'] = (crop_requirements['Day_pre_' + str(l)][k])*prefinaldb.Coated_Urea[i]
                Newdict[str(prefinaldb.index.values[i])][nd]['Ammonium_chloride'] = (crop_requirements['Day_pre_' + str(l)][k])*prefinaldb.Ammonium_chloride[i]
            ados = DOS[i]
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['Urea'] = (crop_requirements['Day_of_sowing'][k])*prefinaldb.Urea[i]                 #############Crop nutrient fraction requirement during the sowing date
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['Coated Urea'] = (crop_requirements['Day_of_sowing'][k])*prefinaldb.Coated_Urea[i]
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['Ammonium_chloride'] = (crop_requirements['Day_of_sowing'][k])*prefinaldb.Ammonium_chloride[i]
            for l in range(1, prefinal.GDD[i]):
                ados = ados + timedelta(days=1)
                if (crop_requirements['Day_after_sowing' + str(l)][k] == ''):
                    continue
                Newdict[str(prefinaldb.index.values[i])][ados]['Urea'] = (crop_requirements['Day_after_sowing'+ str(l)][k]) * prefinaldb.Urea[i]
                Newdict[str(prefinaldb.index.values[i])][ados]['Coated Urea'] = (crop_requirements['Day_after_sowing' + str(l)][k])* prefinaldb.Coated_Urea[i]
                Newdict[str(prefinaldb.index.values[i])][ados]['Urea'] = (crop_requirements['Day_after_sowing' + str(l)][k])*prefinaldb.Ammonium_chloride[i]
        # Phosphrous fertilizers requirements same logic as the nitrogen requirement and water requirement
        for k in range(len(crop_requirements)):
            if (crop_requirements.Crop_requirements[k] != 'P2O5_requirements'):
                continue
            nd = DOS[i] - timedelta(days=30)
            for l in range(0, 29):
                nd = nd + timedelta(days=1)
                if (crop_requirements['Day_pre_' + str(l)][k] == ''):
                    continue
                Newdict[str(prefinaldb.index.values[i])][nd]['Tripple_superphosphate'] = (crop_requirements['Day_pre_' + str(l)][k])*prefinaldb.Tripple_superphosphate[i]
                Newdict[str(prefinaldb.index.values[i])][nd]['Bone_meal_raw'] = (crop_requirements['Day_pre_' + str(l)][k])*prefinaldb.Bone_meal_raw[i]
                Newdict[str(prefinaldb.index.values[i])][nd]['Bone_meal_steam'] = (crop_requirements['Day_pre_' + str(l)][k])*prefinaldb.Bone_meal_steam[i]
            ados = DOS[i]
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['Tripple_superphosphate'] = (crop_requirements['Day_of_sowing'][k])*prefinaldb.Tripple_superphosphate[i]
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['Bone_meal_raw'] = (crop_requirements['Day_of_sowing'][k])*prefinaldb.Bone_meal_raw[i]
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['Bone_meal_steam'] = (crop_requirements['Day_of_sowing'][k])*prefinaldb.Bone_meal_steam[i]
            for l in range(1, prefinal.GDD[i]):
                ados = ados + timedelta(days=1)
                if (crop_requirements['Day_after_sowing' + str(l)][k] == ''):
                    continue
                Newdict[str(prefinaldb.index.values[i])][ados]['Tripple_superphosphate'] = (crop_requirements['Day_after_sowing'+str(l)][k])*prefinaldb.Tripple_superphosphate[i]
                Newdict[str(prefinaldb.index.values[i])][ados]['Bone_meal_raw'] = (crop_requirements['Day_after_sowing' + str(l)][k])*prefinaldb.Bone_meal_raw[i]
                Newdict[str(prefinaldb.index.values[i])][ados]['Bone_meal_steam'] = (crop_requirements['Day_after_sowing' + str(l)][k]) * prefinaldb.Bone_meal_steam[i]

        # Potassium requirements same logic as the Nitrogen and water requirement
        for k in range(len(crop_requirements)):
            if (crop_requirements.Crop_requirements[k] != 'K2O_requirements'):
                continue
            nd = DOS[i] - timedelta(days=30)
            for l in range(0, 29):
                nd = nd + timedelta(days=1)
                if (crop_requirements['Day_pre_' + str(l)][k] == ''):
                    continue
                Newdict[str(prefinaldb.index.values[i])][nd]['potassium_chloride'] = (crop_requirements['Day_pre_' + str(l)][k])*prefinaldb.potassium_chloride[i]
                Newdict[str(prefinaldb.index.values[i])][nd]['potassium_sulfate'] = (crop_requirements['Day_pre_' + str(l)][k])*prefinaldb.potassium_sulfate[i]
                Newdict[str(prefinaldb.index.values[i])][nd]['potassium_schoenite'] = (crop_requirements['Day_pre_' + str(l)][k])*prefinaldb.potassium_schoenite[i]
            ados = DOS[i]
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['potassium_chloride'] = (crop_requirements['Day_of_sowing'][k])*prefinaldb.potassium_chloride[i]
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['Coated Urea'] = (crop_requirements['Day_of_sowing'][k])*prefinaldb.potassium_sulfate[i]
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['potassium_schoenite'] = (crop_requirements['Day_of_sowing'][k])*prefinaldb.potassium_schoenite[i]

            for l in range(1, prefinal.GDD[i]):
                ados = ados + timedelta(days=1)
                if (crop_requirements['Day_after_sowing' + str(l)][k] == ''):
                    continue
                Newdict[str(prefinaldb.index.values[i])][ados]['potassium_chloride'] = (crop_requirements['Day_after_sowing'+str(l)][k])*prefinaldb.potassium_chloride[i]
                Newdict[str(prefinaldb.index.values[i])][ados]['potassium_sulfate'] = (crop_requirements['Day_after_sowing' + str(l)][k])*prefinaldb.potassium_sulfate[i]
                Newdict[str(prefinaldb.index.values[i])][ados]['potassium_schoenite'] = (crop_requirements['Day_after_sowing'+ str(l)][k])*prefinaldb.potassium_schoenite[i]
                          ########################Crop bio mass distribution before sowing date till harvesting
        for k in range(len(crop_requirements)):
            if (crop_requirements.Crop_requirements[k] != 'Crop_biomass'):
                continue
            nd = DOS[i] - timedelta(days=30)
            for l in range(0, 29):
                nd = nd + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][nd]['Crop_biomass'] = (crop_requirements['Day_pre_' + str(l)][k])
            ados = DOS[i]
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['Crop_biomass'] = (crop_requirements['Day_of_sowing'][k])
            for l in range(1, prefinal.GDD[i]):
                ados = ados + timedelta(days=1)
                if (crop_requirements['Day_after_sowing' + str(l)][k] == ''):
                    continue
                Newdict[str(prefinaldb.index.values[i])][ados]['Crop_biomass'] = (crop_requirements['Day_after_sowing' + str(l)][k])
        #########Crop leaf area index #################
        for k in range(len(crop_requirements)):
            if (crop_requirements.Crop_requirements[k] != 'Crop_LAI'):
                continue
            nd = DOS[i] - timedelta(days=30)
            for l in range(0, 29):
                nd = nd + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][nd]['Crop_LAI'] = (crop_requirements['Day_pre_' + str(l)][k])
            ados = DOS[i]
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['Crop_LAI'] = (crop_requirements['Day_of_sowing'][k])
            for l in range(1, prefinal.GDD[i]):
                ados = ados + timedelta(days=1)
                if (crop_requirements['Day_after_sowing' + str(l)][k] == ''):
                    continue
                Newdict[str(prefinaldb.index.values[i])][ados]['Crop_LAI'] = (crop_requirements['Day_after_sowing' + str(l)][k])
        #####################Crop base temperature required for the crop
        for k in range(len(crop_requirements)):
            if (crop_requirements.Crop_requirements[k] != 'Crop_base_temperature'):
                continue
            nd = DOS[i] - timedelta(days=30)
            for l in range(0, 29):
                nd = nd + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][nd]['Crop_base_temperature'] = (crop_requirements['Day_pre_' + str(l)][k])
            ados = DOS[i]
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['Crop_base_temperature'] = (crop_requirements['Day_of_sowing'][k])
            for l in range(1, 150):
                ados = ados + timedelta(days=1)
                if (crop_requirements['Day_after_sowing' + str(l)][k] == ''):
                    continue
                Newdict[str(prefinaldb.index.values[i])][ados]['Crop_base_temperature'] = (crop_requirements['Day_after_sowing' + str(l)][k])
        ###########################Crop consumptive use coeff for crop consumptive use/Evapotranspiration
        for k in range(len(crop_requirements)):
            if (crop_requirements.Crop_requirements[k] != 'Crop_consumptive_use_coeff'):
                continue
            nd = DOS[i] - timedelta(days=30)
            for l in range(0, 29):
                nd = nd + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][nd]['Crop_consumptive_use_coeff'] = (crop_requirements['Day_pre_' + str(l)][k])
            ados = DOS[i]
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['Crop_consumptive_use_coeff'] = (crop_requirements['Day_of_sowing'][k])
            for l in range(1, prefinal.GDD[i]):
                ados = ados + timedelta(days=1)
                if (crop_requirements['Day_after_sowing' + str(l)][k] == ''):
                    continue
                Newdict[str(prefinaldb.index.values[i])][ados]['Crop_consumptive_use_coeff'] = (crop_requirements['Day_after_sowing' + str(l)][k])

    # Package of practice inserting same logic as Crop Water requirement ###########################
    for o in range(len(pop)):
        if (prefinaldb.Crop[i].lower() != pop.Crop[o].lower() or
                prefinaldb.Crop_variety[i].lower() != pop.Crop_variety[o].lower() or
                prefinaldb.season[i].lower() != pop.Season[o].lower() or
                prefinaldb.Sub_agro_climatic_zone[i].lower().replace(' ', '') != pop.Sub_agroclimatic_zone[
                    o].lower().replace(' ', '') or
                prefinaldb.State[i].lower().replace(' ', '') != pop.State[o].lower().replace(' ', '')):                    ########################searching the crop package of practice for that agro climatic data####
            continue

        ################# insearting field protocol ####################
        for x in range(len(pop)):
            if (pop.type_of_protocol[x] != 'field_protocol'):
                continue
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['field protocol'] = pop['Day_of_sowing'][x]
            nd = DOS[i] - timedelta(days=30)
            ados = DOS[i]
            for y in range(0, 29):
                nd = nd + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][nd]['field protocol'] = pop['Day_pre_' + str(y)][x]
            for z in range(1, prefinal.GDD[i]):
                ados = ados + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][ados]['field protocol'] = pop['Day_after_sowing' + str(z)][x]
        ################# insearting   irrigation protocol ###################
        for x in range(len(pop)):
            if (pop.type_of_protocol[x] != 'Irrigation_protocol'):
                continue
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['Irrigation_protocol'] = pop['Day_of_sowing'][x]
            nd = DOS[i] - timedelta(days=30)
            ados = DOS[i]
            for y in range(0, 29):
                nd = nd + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][nd]['Irrigation_protocol'] = pop['Day_pre_' + str(y)][x]
            for z in range(1, prefinal.GDD[i]):
                ados = ados + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][ados]['Irrigation_protocol'] = \
                    pop['Day_after_sowing' + str(z)][x]
        ################# inserting   fertilizer protocol ###################
        for x in range(len(pop)):
            if (pop.type_of_protocol[x] != 'fertilizer_protocol'):
                continue
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['fertilizer_protocol'] = pop['Day_of_sowing'][x]
            nd = DOS[i] - timedelta(days=30)
            ados = DOS[i]
            for y in range(0, 29):
                nd = nd + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][nd]['fertilizer_protocol'] = pop['Day_pre_' + str(y)][x]
            for z in range(1, prefinal.GDD[i]):
                ados = ados + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][ados]['fertilizer_protocol'] = \
                    pop['Day_after_sowing' + str(z)][x]
                ################# inserting  disease protocol #####################
        for x in range(len(pop)):
            if (pop.type_of_protocol[x] != 'disease_protocol'):
                continue
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['disease_protocol'] = pop['Day_of_sowing'][x]
            nd = DOS[i] - timedelta(days=30)
            ados = DOS[i]
            for y in range(0, 29):
                nd = nd + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][nd]['disease_protocol'] = pop['Day_pre_' + str(y)][x]
            for z in range(1, 150):
                ados = ados + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][ados]['disease_protocol'] = pop['Day_after_sowing' + str(z)][x]
            ################# inserting  pest protocol ###################################
        for x in range(len(pop)):
            if (pop.type_of_protocol[x] != 'pest_protocol'):
                continue
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['pest_protocol'] = pop['Day_of_sowing'][x]
            nd = DOS[i] - timedelta(days=30)
            ados = DOS[i]
            for y in range(0, 29):
                nd = nd + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][nd]['pest_protocol'] = pop['Day_pre_' + str(y)][x]
            for z in range(1, prefinal.GDD[i]):
                ados = ados + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][ados]['pest_protocol'] = pop['Day_after_sowing' + str(z)][x]
            ################# inserting   Crop protocol same logic used for irrigation ############
        for x in range(len(pop)):
            if (pop.type_of_protocol[x] != 'crop_protocol'):
                continue
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['crop_protocol'] = pop['Day_of_sowing'][x]
            nd = DOS[i] - timedelta(days=30)
            ados = DOS[i]
            for y in range(0, 29):
                nd = nd + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][nd]['crop_protocol'] = pop['Day_pre_' + str(y)][x]
            for z in range(1, prefinal.GDD[i]):
                ados = ados + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][ados]['crop_protocol'] = pop['Day_after_sowing' + str(z)][x]
                ################# inserting  Crop protocol #################################
        for x in range(len(pop)):
            if (pop.type_of_protocol[x] != 'crop_protocol'):
                continue
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['crop_protocol'] = pop['Day_of_sowing'][x]
            nd = DOS[i] - timedelta(days=30)
            ados = DOS[i]
            for y in range(0, 29):
                nd = nd + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][nd]['crop_protocol'] = pop['Day_pre_' + str(y)][x]
            for z in range(1, prefinal.GDD[i]):
                ados = ados + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][ados]['crop_protocol'] = pop['Day_after_sowing' + str(z)][x]
                ################# inserting # weed_management_protocol
        for x in range(len(pop)):
            if (pop.type_of_protocol[x] != 'weed_protocol'):
                continue
            Newdict[str(prefinaldb.index.values[i])][DOS[i]]['weed_protocol'] = pop['Day_of_sowing'][x]
            nd = DOS[i] - timedelta(days=30)
            ados = DOS[i]
            for y in range(0, 29):
                nd = nd + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][nd]['weed_protocol'] = pop['Day_pre_' + str(y)][x]
            for z in range(1, prefinal.GDD[i]):
                ados = ados + timedelta(days=1)
                Newdict[str(prefinaldb.index.values[i])][ados]['weed_protocol'] = pop['Day_after_sowing' + str(z)][x]


































































































