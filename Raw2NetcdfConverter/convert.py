'''
Description: 
This Modul convert the .raw files to .nc files. 
In future, the function should be abe to store several pings within one file


    
Author: 
Dr. Sindre Vatnehol (PhD)
Institute of Marine Research, Norway

Mail: 
sindre.vatnehol@imr.no

Tlf.: 
+47 900 79 376


Project: 
REDUS (Reducing uncertainty in stock assessment)  
www.redus.no
'''


    
import glob,os, pynmea2,os.path
from netCDF4 import Dataset
import numpy as np
#from shutil import copyfile
from .ReadRawData import ReadRawData
from .template import addAnnotation, addEnvironment, addPlatform, addProvenance
from .template import addGlobalAttributes, writePlatformData, createSonarData
from .template import addVendorSpecificGrp, addSonarData, addEnvironmentData
import os

    



def getGPSsourcesfromdata(NMEA_info): 
    
    PriorityList = np.array(('RMC', 'GLL','GGA'))
    
    Tempo = []
    for LoopIndex0 in range(len(NMEA_info)): 
        info = NMEA_info[LoopIndex0]
        try: 
            msg = pynmea2.parse(info,check= False)
            try: 
                msg.longitude
                Tempo = np.hstack((Tempo,info.split(',')[0][-3:]))
            except AttributeError: 
                k=1
        except pynmea2.nmea.ParseError:
            k=1
            
             
    return [i for i, j in zip(PriorityList, np.unique(Tempo)) if i == j]
               
    
    
    
def WelcomeScreen(projectName): 
    print(projectName)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    print('    >=>      /\      >=>          >=>           ')
    print('  >=>       /  \           >=>         >=>      ')
    print('           / >=>\                               ')
    print('   >=>    /      \                 >=>          ')
    print('         /   >=>  \      >=>                >=> ')
    print('        / >=>      \              >=>    >=>    ')
    print('_______/________>=>_\___________________________')
    print('')

    
    
    
    
def GetListOfFiles(directory,directoryToRaw,Files2Convert): 
    
    os.chdir(directory)
    
    ConvertedFiles = glob.glob('*.nc')
    
    Files = []

    for i in range(len(Files2Convert)): 
        if not Files2Convert[i].replace('.raw','.nc') in ConvertedFiles: 
            Files.append(Files2Convert[i])
    
    os.chdir(directoryToRaw)
    
    return Files
    
    
    
    
    
def Raw2NetcdfConverter(directoryToRaw,vessel_name,platform_type,
                        platform_code,maxPingInFile,MaxNumberOfFilesInNC,
                        directory, reconvert): 
    '''
    Description: 
        Protocol to convert sonar raw data to netcdf
    '''
    
    
    
    
    #Clear terminal window
    os.system('cls' if os.name == 'nt' else 'clear')
    
    
    
    
    #print welcome screen
    WelcomeScreen('convertrawtonetcdf')
    
    
    
    #Get the location of the templet
    this_dir, this_filename = os.path.split(__file__)
    template_file = os.path.join(this_dir, "data", "source_template.nc")
    
    f =Dataset(template_file,'r') 
    #Check if netcdf folder exist
    #If not create the directory
    if (not os.path.isdir(directory)): 
        os.makedirs(directory)
        
    

    #Change the directory to the raw files
    os.chdir(directoryToRaw)
    
    
    
    Files2Convert = sorted(glob.glob("*.raw"))
    
    
    if reconvert == False: 
        Files2Convert=GetListOfFiles(directory,directoryToRaw,Files2Convert)
        
    
    
    #Go through each .raw file in folder
    for filename in Files2Convert:
        
        
        #Display msg to user
        print('Converting '+filename+' to netcdf')
        
        
        
        #Change the directory back to .raw folder. 
        #Later it will be send to the netcdf folder
        os.chdir(directoryToRaw)
        
        
            
        #open .raw file
        fid = open(filename,mode='rb')
#        try: 
           
        
        #Read the .raw file according to SIMRAD spesifications
        FileData = ReadRawData(fid,12)
        
        
        
        #Get the transduser rotation
        #This is a correction of the true direction of the beams
        transducer_rotation =  FileData.dirz
                    
        
        #Set the directory to where the netcdf should be stored
        os.chdir(directory)
        
            
        #Set the name of the .nc file to the same as the first .raw file                        
        ncfilename=filename[:-4]+'.nc'

        #open new .nc file
        fid = Dataset(ncfilename,'w')

        #Add global attribtues
        addGlobalAttributes(fid,filename)
        
        #Create annotation level
        addAnnotation(fid)
        
        #create environment level
        addEnvironment(fid)
        
        #create platform level
        addPlatform(fid,platform_code, vessel_name, platform_type,f)
        
        #create the provinence group
        addProvenance(fid)
        
        #create sonar data group
        createSonarData(fid)

        #create Vendor specific group
        addVendorSpecificGrp(fid)

        #Get the list of nmea sources according to priority list
        GPSsourceList = getGPSsourcesfromdata(FileData.NMEA_info)
        
        #Write platform data 
        if not GPSsourceList== []: 
            writePlatformData(FileData,GPSsourceList,fid)
        
        #Write environment data
        addEnvironmentData(FileData, fid)

        #Write sonar data        
        addSonarData(FileData,fid,transducer_rotation)
                        
        fid.close()
#        except: 
#            print('Skipped file')